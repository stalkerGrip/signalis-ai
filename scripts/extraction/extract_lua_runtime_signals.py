from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


PIPELINE_CONTRACT = {
    "script_id": "scripts.extraction.extract_lua_runtime_signals",
    "purpose": "Extract generic raw Lua syntax evidence from files listed in source_file_manifest without project-specific or runtime semantic assumptions.",
    "pipeline_stage": "extraction",
    "input_families": ["source_file_manifest"],
    "required_input_capabilities": [
        "source_roots",
        "source_files",
        "file_realm_hints",
        "file_digests",
    ],
    "output_families": ["raw_lua_extraction"],
    "required_output_capabilities": [
        "source_manifest_reference",
        "file_digest_verification",
        "lua_assignments",
        "lua_table_fields",
        "lua_literal_values",
        "lua_function_definitions",
        "lua_function_assignments",
        "lua_anonymous_functions",
        "lua_call_expressions",
        "lua_method_call_expressions",
        "lua_call_arguments",
        "lua_function_body_spans",
        "line_evidence",
    ],
    "output_schemas": ["raw_lua_extraction"],
    "artifact_patterns": [
        "manifests/extraction/raw_lua_extraction.json",
        "manifests/extraction/raw_lua_extraction.md",
    ],
    "promotion_role": "intermediate_evidence",
    "canonical_status": "active",
}

SCRIPT_ID = "scripts.extraction.extract_lua_runtime_signals"
SCHEMA = "raw_lua_extraction"
SCHEMA_VERSION = "1"
ARTIFACT_FAMILY = "raw_lua_extraction"
REQUIRED_CAPABILITIES = PIPELINE_CONTRACT["required_output_capabilities"]

IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
QUALIFIED = rf"{IDENT}(?:(?:\.|:){IDENT})*"

FUNCTION_RE = re.compile(rf"^\s*(?:(local)\s+)?function\s+({QUALIFIED})\s*\(([^)]*)\)")
ASSIGNED_FUNCTION_RE = re.compile(rf"^\s*({QUALIFIED}(?:\[[^\]]+\])?)\s*=\s*function\s*\(([^)]*)\)")
LOCAL_ASSIGNED_FUNCTION_RE = re.compile(rf"^\s*local\s+({IDENT})\s*=\s*function\s*\(([^)]*)\)")
LOCAL_ASSIGNMENT_RE = re.compile(rf"^\s*local\s+(?P<lhs>{IDENT})\s*=\s*(?P<rhs>.+?)\s*$")
ASSIGNMENT_RE = re.compile(r"^\s*(?P<lhs>[^=~<>]+?)\s*=\s*(?P<rhs>.+?)\s*$")
TABLE_FIELD_RE = re.compile(rf"^\s*(?P<key>{IDENT}|\[[^\]]+\])\s*=\s*(?P<value>.+?)(?:,)?\s*$")
CALL_RE = re.compile(rf"(?<![\w.:'\"])(?P<target>{QUALIFIED})\s*\(")
STRING_RE = re.compile(r"(?P<quote>['\"])(?P<value>(?:\\.|(?!\1).)*)(?P=quote)")
LONG_STRING_RE = re.compile(r"\[(=*)\[(.*?)\]\1\]", re.DOTALL)
TOKEN_RE = re.compile(r"\b(function|then|do|repeat|end|until)\b")

CONTROL_CALL_WORDS = {
    "if",
    "for",
    "while",
    "repeat",
    "until",
    "return",
    "function",
    "local",
    "elseif",
}


@dataclass
class SyntaxContext:
    kind: str
    start_line: int
    label: str | None = None


@dataclass
class ArgumentSpan:
    text: str
    start_line: int
    end_line: int


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_path(path: Path | str) -> str:
    return Path(path).as_posix() if isinstance(path, Path) else str(path).replace("\\", "/")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def validate_manifest(manifest: dict[str, Any], manifest_path: Path) -> None:
    if manifest.get("schema") != "source_file_manifest":
        raise ValueError(f"Input is not a source_file_manifest: {manifest_path}")
    if manifest.get("artifact_family") != "source_file_manifest":
        raise ValueError(f"Input artifact family is not source_file_manifest: {manifest_path}")
    if not isinstance(manifest.get("source_files"), list):
        raise ValueError(f"source_file_manifest.source_files must be a list: {manifest_path}")


def read_text_lossless(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace"), "utf-8-replace"


def strip_line_comment(line: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    i = 0
    while i < len(line):
        ch = line[i]
        nxt = line[i + 1] if i + 1 < len(line) else ""
        if escaped:
            escaped = False
        elif ch == "\\" and (in_single or in_double):
            escaped = True
        elif ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "-" and nxt == "-" and not in_single and not in_double:
            return line[:i]
        i += 1
    return line


def mask_strings(line: str) -> str:
    return STRING_RE.sub(lambda m: m.group("quote") + ("_" * len(m.group("value"))) + m.group("quote"), line)


def split_params(params: str) -> list[str]:
    return [part.strip() for part in params.split(",") if part.strip()]


def split_args(args: str) -> list[str]:
    return [span.text for span in split_args_with_spans(args, 1)]


def split_args_with_spans(args: str, base_line: int) -> list[ArgumentSpan]:
    spans: list[ArgumentSpan] = []
    start = 0
    depth = 0
    block_depth = 0
    in_single = False
    in_double = False
    escaped = False
    i = 0

    def line_for_offset(offset: int) -> int:
        return base_line + args.count("\n", 0, max(0, min(offset, len(args))))

    def append_span(raw_start: int, raw_end: int) -> None:
        raw = args[raw_start:raw_end]
        stripped = raw.strip()
        if not stripped:
            return
        leading_ws = len(raw) - len(raw.lstrip())
        trailing_ws = len(raw.rstrip())
        actual_start = raw_start + leading_ws
        actual_end = raw_start + trailing_ws
        spans.append(
            ArgumentSpan(
                text=stripped,
                start_line=line_for_offset(actual_start),
                end_line=line_for_offset(max(actual_start, actual_end - 1)),
            )
        )

    def consume_word(pos: int) -> tuple[str | None, int]:
        m = TOKEN_RE.match(args, pos)
        if not m:
            return None, pos
        return m.group(1), m.end()

    while i < len(args):
        ch = args[i]
        if escaped:
            escaped = False
            i += 1
            continue
        if ch == "\\" and (in_single or in_double):
            escaped = True
            i += 1
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            i += 1
            continue
        if in_single or in_double:
            i += 1
            continue
        if ch.isalpha() or ch == "_":
            token, end_pos = consume_word(i)
            if token:
                if token in {"function", "then", "do", "repeat"}:
                    block_depth += 1
                elif token in {"end", "until"} and block_depth > 0:
                    block_depth -= 1
                i = end_pos
                continue
        if ch in "({[":
            depth += 1
        elif ch in ")}]" and depth > 0:
            depth -= 1
        elif ch == "," and depth == 0 and block_depth == 0:
            append_span(start, i)
            start = i + 1
        i += 1
    append_span(start, len(args))
    return spans

def classify_value(value: str) -> str:
    stripped = value.strip().rstrip(",").strip()
    if stripped == "":
        return "empty"
    if stripped.startswith("{"):
        return "table_literal"
    if stripped.startswith("function"):
        return "function_literal"
    if stripped in {"true", "false"}:
        return "boolean_literal"
    if stripped == "nil":
        return "nil_literal"
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", stripped):
        return "number_literal"
    if STRING_RE.fullmatch(stripped) or LONG_STRING_RE.fullmatch(stripped):
        return "string_literal"
    if re.fullmatch(QUALIFIED, stripped):
        return "symbol_reference"
    return "expression"


def symbol_shape(target: str) -> dict[str, Any]:
    separators = [ch for ch in target if ch in ".:"]
    parts = re.split(r"[.:]", target)
    return {
        "target": target,
        "root": parts[0] if parts else target,
        "leaf": parts[-1] if parts else target,
        "parts": parts,
        "separators": separators,
        "uses_method_colon": ":" in separators,
        "uses_table_dot": "." in separators,
    }


def line_evidence(file_record: dict[str, Any], line_no: int, line: str) -> dict[str, Any]:
    return {
        "file_id": file_record.get("file_id"),
        "source_root_index": file_record.get("source_root_index"),
        "relative_path": file_record.get("relative_path"),
        "absolute_path": file_record.get("absolute_path"),
        "realm_hint": file_record.get("realm_hint"),
        "line": line_no,
        "text": line.rstrip("\n"),
    }


def emit_evidence(kind: str, file_record: dict[str, Any], line_no: int, line: str, payload: dict[str, Any]) -> dict[str, Any]:
    base = {
        "kind": kind,
        "evidence_id": "raw_lua_evidence:"
        + stable_hash(
            {
                "kind": kind,
                "file_id": file_record.get("file_id"),
                "line": line_no,
                "payload": payload,
                "text": line.rstrip("\n"),
            }
        )[:16],
        "evidence": line_evidence(file_record, line_no, line),
    }
    base.update(payload)
    return base


def current_table_depth(context_stack: list[SyntaxContext]) -> int:
    return sum(1 for ctx in context_stack if ctx.kind == "table")


def context_path(context_stack: list[SyntaxContext]) -> list[dict[str, Any]]:
    return [{"kind": ctx.kind, "start_line": ctx.start_line, "label": ctx.label} for ctx in context_stack]


def computed_key_payload(raw_key: str) -> dict[str, Any]:
    key = raw_key.strip()
    if key.startswith("[") and key.endswith("]"):
        expr = key[1:-1].strip()
        return {
            "key_syntax": "computed_key",
            "key_text": key,
            "key_expression": expr,
            "key_expression_kind": classify_value(expr),
        }
    return {
        "key_syntax": "identifier_key",
        "key_text": key,
        "key_expression": key,
        "key_expression_kind": "identifier",
    }


def extract_call_arguments(code_line: str, call_start: int) -> tuple[str, bool]:
    open_index = code_line.find("(", call_start)
    if open_index == -1:
        return "", False
    depth = 0
    in_single = False
    in_double = False
    escaped = False
    for index in range(open_index, len(code_line)):
        ch = code_line[index]
        if escaped:
            escaped = False
            continue
        if ch == "\\" and (in_single or in_double):
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            continue
        if in_single or in_double:
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return code_line[open_index + 1 : index], True
    return code_line[open_index + 1 :], False


def extract_multiline_call_arguments(lines: list[str], start_line: int, call_start_column: int) -> tuple[str, bool, list[ArgumentSpan]]:
    first = strip_line_comment(lines[start_line - 1])
    open_index = first.find("(", call_start_column - 1)
    if open_index == -1:
        return "", False, []

    chunks: list[str] = []
    depth = 0
    started = False
    in_single = False
    in_double = False
    escaped = False

    for line_no in range(start_line, len(lines) + 1):
        code = strip_line_comment(lines[line_no - 1])
        begin = open_index if line_no == start_line else 0
        i = begin
        while i < len(code):
            ch = code[i]
            if escaped:
                escaped = False
                if started:
                    chunks.append(ch)
                i += 1
                continue
            if ch == "\\" and (in_single or in_double):
                escaped = True
                if started:
                    chunks.append(ch)
                i += 1
                continue
            if ch == "'" and not in_double:
                in_single = not in_single
                if started:
                    chunks.append(ch)
                i += 1
                continue
            if ch == '"' and not in_single:
                in_double = not in_double
                if started:
                    chunks.append(ch)
                i += 1
                continue
            if in_single or in_double:
                if started:
                    chunks.append(ch)
                i += 1
                continue
            if ch == "(":
                depth += 1
                if started:
                    chunks.append(ch)
                else:
                    started = True
                i += 1
                continue
            if ch == ")":
                depth -= 1
                if depth == 0 and started:
                    args_text = "".join(chunks)
                    return args_text, True, split_args_with_spans(args_text, start_line)
                if started:
                    chunks.append(ch)
                i += 1
                continue
            if started:
                chunks.append(ch)
            i += 1
        if started:
            chunks.append("\n")
    args_text = "".join(chunks)
    return args_text, False, split_args_with_spans(args_text, start_line)


def close_leading_table_context(code_line: str, context_stack: list[SyntaxContext]) -> None:
    stripped = mask_strings(code_line).strip()
    if not stripped.startswith("}"):
        return
    for i in range(len(context_stack) - 1, -1, -1):
        if context_stack[i].kind == "table":
            del context_stack[i:]
            break


def update_context_stack_after_line(code_line: str, line_no: int, context_stack: list[SyntaxContext], table_label: str | None) -> None:
    masked = mask_strings(code_line)
    stripped = masked.strip()
    leading_close = 1 if stripped.startswith("}") else 0
    open_count = masked.count("{")
    close_count = max(0, masked.count("}") - leading_close)

    for open_index in range(open_count):
        label = table_label if open_index == 0 else None
        context_stack.append(SyntaxContext(kind="table", start_line=line_no, label=label))
    for _ in range(close_count):
        for i in range(len(context_stack) - 1, -1, -1):
            if context_stack[i].kind == "table":
                del context_stack[i:]
                break


def tokenized_block_end_line(lines: list[str], start_line: int) -> int | None:
    stack: list[str] = []
    for line_index in range(start_line - 1, len(lines)):
        code = mask_strings(strip_line_comment(lines[line_index]))
        for token in TOKEN_RE.findall(code):
            if token in {"function", "then", "do", "repeat"}:
                stack.append(token)
            elif token == "until":
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i] == "repeat":
                        del stack[i:]
                        break
            elif token == "end":
                if stack:
                    stack.pop()
                    if not stack:
                        return line_index + 1
    return None


def table_literal_end_line(lines: list[str], start_line: int) -> int | None:
    depth = 0
    seen_open = False
    for line_index in range(start_line - 1, len(lines)):
        code = mask_strings(strip_line_comment(lines[line_index]))
        for ch in code:
            if ch == "{":
                depth += 1
                seen_open = True
            elif ch == "}" and seen_open:
                depth -= 1
                if depth <= 0:
                    return line_index + 1
    return None


def body_span_for_value(lines: list[str], start_line: int, value_kind: str) -> dict[str, Any]:
    if value_kind == "function_literal":
        end_line = tokenized_block_end_line(lines, start_line)
    elif value_kind == "table_literal":
        end_line = table_literal_end_line(lines, start_line)
    else:
        end_line = None
    return {"start_line": start_line, "end_line": end_line, "complete": end_line is not None}


def emit_call_argument_evidence(
    evidence_items: list[dict[str, Any]],
    file_record: dict[str, Any],
    line_no: int,
    source_line: str,
    parent_call: dict[str, Any],
    argument_index: int,
    argument_text: str,
    argument_start_line: int,
    argument_end_line: int,
    lines: list[str],
) -> None:
    argument_kind = classify_value(argument_text)
    payload: dict[str, Any] = {
        "parent_call_evidence_id": parent_call["evidence_id"],
        "parent_call_symbol": parent_call.get("symbol"),
        "argument_index": argument_index,
        "argument_kind": argument_kind,
        "argument_preview": argument_text[:240],
        "argument_truncated": len(argument_text) > 240,
        "argument_start_line": argument_start_line,
        "argument_end_line": argument_end_line,
    }
    if argument_kind == "function_literal":
        payload["anonymous_function_body_span"] = body_span_for_value(lines, argument_start_line, "function_literal")
    evidence_items.append(emit_evidence("lua_call_argument", file_record, line_no, source_line, payload))


def extract_from_file(file_record: dict[str, Any], max_string_length: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    path = Path(str(file_record["absolute_path"]))
    expected_sha = str(file_record.get("sha256", ""))
    actual_sha = file_sha256(path)
    text, encoding = read_text_lossless(path)

    digest_status = "match" if actual_sha == expected_sha else "mismatch"
    evidence_items: list[dict[str, Any]] = []
    context_stack: list[SyntaxContext] = []

    lines = text.splitlines()
    for index, raw_line in enumerate(lines, start=1):
        code_line = strip_line_comment(raw_line)
        if not code_line.strip():
            continue

        close_leading_table_context(code_line, context_stack)
        table_depth_before = current_table_depth(context_stack)
        in_table_before = table_depth_before > 0
        table_label_to_open: str | None = None

        table_match = TABLE_FIELD_RE.match(code_line)
        if table_match and in_table_before:
            value = table_match.group("value").strip()
            value_kind = classify_value(value)
            key_payload = computed_key_payload(table_match.group("key"))
            payload = {
                **key_payload,
                "value_kind": value_kind,
                "value_preview": value[:240],
                "value_truncated": len(value) > 240,
                "table_depth": table_depth_before,
                "context_path": context_path(context_stack),
            }
            if value_kind in {"table_literal", "function_literal"}:
                payload["value_body_span"] = body_span_for_value(lines, index, value_kind)
            evidence_items.append(emit_evidence("lua_table_field", file_record, index, raw_line, payload))
            if value_kind == "table_literal":
                table_label_to_open = key_payload["key_text"]
        else:
            local_m = LOCAL_ASSIGNMENT_RE.match(code_line)
            if local_m:
                lhs = local_m.group("lhs").strip()
                rhs = local_m.group("rhs").strip()
                rhs_kind = classify_value(rhs)
                payload = {
                    "lhs": lhs,
                    "is_local": True,
                    "rhs_kind": rhs_kind,
                    "rhs_preview": rhs[:240],
                    "rhs_truncated": len(rhs) > 240,
                }
                if rhs_kind in {"table_literal", "function_literal"}:
                    payload["rhs_body_span"] = body_span_for_value(lines, index, rhs_kind)
                evidence_items.append(emit_evidence("lua_assignment", file_record, index, raw_line, payload))
                if rhs_kind == "table_literal":
                    table_label_to_open = lhs
            else:
                m = ASSIGNMENT_RE.match(code_line)
                if m and not re.search(r"(?<![<>=~])={2,}|~=|<=|>=", code_line):
                    lhs = m.group("lhs").strip()
                    rhs = m.group("rhs").strip()
                    rhs_kind = classify_value(rhs)
                    payload = {
                        "lhs": lhs,
                        "is_local": False,
                        "rhs_kind": rhs_kind,
                        "rhs_preview": rhs[:240],
                        "rhs_truncated": len(rhs) > 240,
                    }
                    if rhs_kind in {"table_literal", "function_literal"}:
                        payload["rhs_body_span"] = body_span_for_value(lines, index, rhs_kind)
                    evidence_items.append(emit_evidence("lua_assignment", file_record, index, raw_line, payload))
                    if rhs_kind == "table_literal":
                        table_label_to_open = lhs

        m = FUNCTION_RE.match(code_line)
        if m:
            local_marker, name, params = m.groups()
            evidence_items.append(
                emit_evidence(
                    "lua_function_definition",
                    file_record,
                    index,
                    raw_line,
                    {
                        "definition_form": "function_statement",
                        "is_local": bool(local_marker),
                        "symbol": symbol_shape(name),
                        "parameters": split_params(params),
                        "body_span": body_span_for_value(lines, index, "function_literal"),
                    },
                )
            )

        m = ASSIGNED_FUNCTION_RE.match(code_line)
        if m and not (in_table_before and table_match):
            lhs, params = m.groups()
            evidence_items.append(
                emit_evidence(
                    "lua_function_assignment",
                    file_record,
                    index,
                    raw_line,
                    {
                        "is_local": False,
                        "lhs": lhs,
                        "symbol": symbol_shape(lhs) if re.fullmatch(QUALIFIED, lhs) else {"target": lhs},
                        "parameters": split_params(params),
                        "body_span": body_span_for_value(lines, index, "function_literal"),
                    },
                )
            )

        m = LOCAL_ASSIGNED_FUNCTION_RE.match(code_line)
        if m:
            lhs, params = m.groups()
            evidence_items.append(
                emit_evidence(
                    "lua_function_assignment",
                    file_record,
                    index,
                    raw_line,
                    {
                        "is_local": True,
                        "lhs": lhs,
                        "symbol": symbol_shape(lhs),
                        "parameters": split_params(params),
                        "body_span": body_span_for_value(lines, index, "function_literal"),
                    },
                )
            )

        if "function" in code_line and not FUNCTION_RE.match(code_line) and not ASSIGNED_FUNCTION_RE.match(code_line) and not LOCAL_ASSIGNED_FUNCTION_RE.match(code_line):
            for anon in re.finditer(r"function\s*\(([^)]*)\)", code_line):
                evidence_items.append(
                    emit_evidence(
                        "lua_anonymous_function",
                        file_record,
                        index,
                        raw_line,
                        {
                            "parameters": split_params(anon.group(1)),
                            "column": anon.start() + 1,
                            "body_span": body_span_for_value(lines, index, "function_literal"),
                            "context_path": context_path(context_stack),
                        },
                    )
                )

        for call in CALL_RE.finditer(code_line):
            target = call.group("target")
            if target in CONTROL_CALL_WORDS:
                continue
            args_text, args_complete = extract_call_arguments(code_line, call.start("target"))
            args = split_args(args_text) if args_complete else []
            kind = "lua_method_call_expression" if ":" in target else "lua_call_expression"
            call_item = emit_evidence(
                kind,
                file_record,
                index,
                raw_line,
                {
                    "symbol": symbol_shape(target),
                    "column": call.start("target") + 1,
                    "arguments_preview": args_text[:240],
                    "arguments_truncated": len(args_text) > 240,
                    "arguments_complete_on_line": args_complete,
                    "argument_count_on_line": len(args),
                    "argument_kinds_on_line": [classify_value(arg) for arg in args],
                },
            )
            evidence_items.append(call_item)

            if args_complete:
                for arg_index, arg_text in enumerate(args):
                    emit_call_argument_evidence(
                        evidence_items,
                        file_record,
                        index,
                        raw_line,
                        call_item,
                        arg_index,
                        arg_text,
                        index,
                        index,
                        lines,
                    )
            else:
                multi_args_text, multi_complete, arg_spans = extract_multiline_call_arguments(lines, index, call.start("target") + 1)
                call_item["arguments_complete_multiline"] = multi_complete
                call_item["argument_count_multiline"] = len(arg_spans)
                call_item["argument_kinds_multiline"] = [classify_value(span.text) for span in arg_spans]
                call_item["arguments_multiline_preview"] = multi_args_text[:240]
                call_item["arguments_multiline_truncated"] = len(multi_args_text) > 240
                for arg_index, span in enumerate(arg_spans):
                    emit_call_argument_evidence(
                        evidence_items,
                        file_record,
                        span.start_line,
                        lines[span.start_line - 1],
                        call_item,
                        arg_index,
                        span.text,
                        span.start_line,
                        span.end_line,
                        lines,
                    )

        for s in STRING_RE.finditer(code_line):
            value = s.group("value")
            evidence_items.append(
                emit_evidence(
                    "lua_literal_value",
                    file_record,
                    index,
                    raw_line,
                    {
                        "literal_kind": "string_literal",
                        "literal_form": "quoted_string",
                        "quote": s.group("quote"),
                        "value": value[:max_string_length],
                        "value_truncated": len(value) > max_string_length,
                        "length": len(value),
                        "column": s.start() + 1,
                    },
                )
            )

        update_context_stack_after_line(code_line, index, context_stack, table_label_to_open)

    for long_string in LONG_STRING_RE.finditer(text):
        start_line = text.count("\n", 0, long_string.start()) + 1
        value = long_string.group(2)
        source_line = lines[start_line - 1] if start_line - 1 < len(lines) else ""
        evidence_items.append(
            emit_evidence(
                "lua_literal_value",
                file_record,
                start_line,
                source_line,
                {
                    "literal_kind": "string_literal",
                    "literal_form": "long_bracket_string",
                    "equals_depth": len(long_string.group(1)),
                    "value": value[:max_string_length],
                    "value_truncated": len(value) > max_string_length,
                    "length": len(value),
                    "column": 1,
                },
            )
        )

    file_summary = {
        "file_id": file_record.get("file_id"),
        "relative_path": file_record.get("relative_path"),
        "absolute_path": file_record.get("absolute_path"),
        "realm_hint": file_record.get("realm_hint"),
        "expected_sha256": expected_sha,
        "actual_sha256": actual_sha,
        "digest_status": digest_status,
        "encoding": encoding,
        "line_count": len(lines),
        "evidence_total": len(evidence_items),
        "evidence_kind_counts": count_by(evidence_items, "kind"),
    }
    return evidence_items, file_summary


def count_by(items: Iterable[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key, "unknown"))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def build_artifact(
    workspace: Path,
    input_manifest_path: Path,
    max_string_length: int,
    fail_on_digest_mismatch: bool,
) -> dict[str, Any]:
    manifest = load_json(input_manifest_path)
    validate_manifest(manifest, input_manifest_path)

    source_files = manifest["source_files"]
    evidence_items: list[dict[str, Any]] = []
    file_summaries: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for file_record in source_files:
        try:
            file_evidence, file_summary = extract_from_file(file_record, max_string_length)
            evidence_items.extend(file_evidence)
            file_summaries.append(file_summary)
        except Exception as exc:  # noqa: BLE001 - artifact should preserve per-file extraction errors.
            errors.append(
                {
                    "file_id": file_record.get("file_id"),
                    "relative_path": file_record.get("relative_path"),
                    "absolute_path": file_record.get("absolute_path"),
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )

    digest_mismatches = [item for item in file_summaries if item["digest_status"] != "match"]
    if fail_on_digest_mismatch and digest_mismatches:
        examples = ", ".join(str(item["relative_path"]) for item in digest_mismatches[:5])
        raise ValueError(f"Digest mismatch in {len(digest_mismatches)} files: {examples}")

    content_digest = stable_hash(
        {
            "input_manifest_artifact_id": manifest.get("artifact_id"),
            "input_manifest_content_digest": manifest.get("content_digest"),
            "file_summaries": [
                {
                    "file_id": item["file_id"],
                    "actual_sha256": item["actual_sha256"],
                    "evidence_total": item["evidence_total"],
                    "evidence_kind_counts": item["evidence_kind_counts"],
                    "digest_status": item["digest_status"],
                }
                for item in file_summaries
            ],
            "errors": errors,
            "evidence_items": [
                {
                    "evidence_id": item["evidence_id"],
                    "kind": item["kind"],
                    "file_id": item["evidence"]["file_id"],
                    "line": item["evidence"]["line"],
                }
                for item in evidence_items
            ],
        }
    )

    artifact_id = f"{ARTIFACT_FAMILY}:{content_digest[:16]}"

    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "artifact_family": ARTIFACT_FAMILY,
        "artifact_id": artifact_id,
        "producer_script": SCRIPT_ID,
        "pipeline_stage": "extraction",
        "canonical_status": "intermediate",
        "promotion_role": "intermediate_evidence",
        "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "required_capabilities": REQUIRED_CAPABILITIES,
        "content_digest": content_digest,
        "workspace": normalize_path(workspace),
        "source_manifest": {
            "path": normalize_path(input_manifest_path),
            "artifact_id": manifest.get("artifact_id"),
            "content_digest": manifest.get("content_digest"),
            "schema": manifest.get("schema"),
            "schema_version": manifest.get("schema_version"),
        },
        "summary": {
            "files_total": len(source_files),
            "files_extracted": len(file_summaries),
            "files_failed": len(errors),
            "digest_mismatch_files": len(digest_mismatches),
            "evidence_total": len(evidence_items),
            "evidence_kind_counts": count_by(evidence_items, "kind"),
            "realm_hint_counts": count_by(file_summaries, "realm_hint"),
        },
        "file_summaries": file_summaries,
        "evidence_items": evidence_items,
        "errors": errors,
        "lineage": {
            "input_kind": "pipeline_artifact",
            "input_artifacts": [normalize_path(input_manifest_path)],
            "parent_artifact_id": manifest.get("artifact_id"),
            "regenerates": None,
            "regeneration_inputs": {
                "producer_script": SCRIPT_ID,
                "schema": SCHEMA,
                "schema_version": SCHEMA_VERSION,
                "source_file_manifest": normalize_path(input_manifest_path),
                "source_file_manifest_artifact_id": manifest.get("artifact_id"),
                "source_file_manifest_content_digest": manifest.get("content_digest"),
                "max_string_length": max_string_length,
            },
        },
    }


def write_json(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Raw Lua Extraction")
    lines.append("")
    lines.append(f"- Artifact family: `{artifact['artifact_family']}`")
    lines.append(f"- Artifact ID: `{artifact['artifact_id']}`")
    lines.append(f"- Producer: `{artifact['producer_script']}`")
    lines.append(f"- Generated at: `{artifact['generated_at']}`")
    lines.append(f"- Workspace: `{artifact['workspace']}`")
    lines.append(f"- Source manifest: `{artifact['source_manifest']['path']}`")
    lines.append(f"- Source manifest artifact ID: `{artifact['source_manifest']['artifact_id']}`")
    lines.append("")
    lines.append("## Required Capabilities")
    lines.append("")
    for capability in artifact["required_capabilities"]:
        lines.append(f"- `{capability}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    for key, value in artifact["summary"].items():
        if isinstance(value, dict):
            lines.append(f"- `{key}`:")
            for sub_key, sub_value in value.items():
                lines.append(f"  - `{sub_key}`: `{sub_value}`")
        else:
            lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Largest Files by Extracted Evidence")
    lines.append("")
    largest = sorted(artifact["file_summaries"], key=lambda item: item.get("evidence_total", 0), reverse=True)[:50]
    lines.append("| Evidence | Realm | Digest | File |")
    lines.append("|---:|---|---|---|")
    for item in largest:
        lines.append(
            f"| `{item['evidence_total']}` | `{item.get('realm_hint')}` | `{item.get('digest_status')}` | `{item.get('relative_path')}` |"
        )
    if artifact["errors"]:
        lines.append("")
        lines.append("## Errors")
        lines.append("")
        lines.append("| File | Error | Message |")
        lines.append("|---|---|---|")
        for error in artifact["errors"][:100]:
            message = str(error.get("message", "")).replace("|", "\\|")
            lines.append(f"| `{error.get('relative_path')}` | `{error.get('error_type')}` | {message} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract generic raw Lua syntax evidence from source_file_manifest.")
    parser.add_argument("--workspace", required=True, help="Workspace root, e.g. E:/signalis_ai")
    parser.add_argument(
        "--input-manifest",
        default=None,
        help="Input source_file_manifest JSON. Defaults to manifests/extraction/source_file_manifest.json.",
    )
    parser.add_argument(
        "--out-json",
        default=None,
        help="Output JSON path. Defaults to manifests/extraction/raw_lua_extraction.json.",
    )
    parser.add_argument(
        "--out-md",
        default=None,
        help="Output Markdown path. Defaults to manifests/extraction/raw_lua_extraction.md.",
    )
    parser.add_argument(
        "--max-string-length",
        type=int,
        default=500,
        help="Maximum stored string literal preview length. Defaults to 500.",
    )
    parser.add_argument(
        "--fail-on-digest-mismatch",
        action="store_true",
        help="Fail if any source file digest differs from the source_file_manifest digest.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    if not workspace.exists():
        raise FileNotFoundError(f"Workspace does not exist: {workspace}")
    if not workspace.is_dir():
        raise NotADirectoryError(f"Workspace is not a directory: {workspace}")

    input_manifest = Path(args.input_manifest) if args.input_manifest else workspace / "manifests" / "extraction" / "source_file_manifest.json"
    if not input_manifest.is_absolute():
        input_manifest = workspace / input_manifest
    input_manifest = input_manifest.resolve()
    if not input_manifest.exists():
        raise FileNotFoundError(f"Input manifest does not exist: {input_manifest}")

    artifact = build_artifact(
        workspace=workspace,
        input_manifest_path=input_manifest,
        max_string_length=args.max_string_length,
        fail_on_digest_mismatch=args.fail_on_digest_mismatch,
    )

    out_json = Path(args.out_json) if args.out_json else workspace / "manifests" / "extraction" / "raw_lua_extraction.json"
    out_md = Path(args.out_md) if args.out_md else workspace / "manifests" / "extraction" / "raw_lua_extraction.md"
    if not out_json.is_absolute():
        out_json = workspace / out_json
    if not out_md.is_absolute():
        out_md = workspace / out_md

    write_json(out_json, artifact)
    write_md(out_md, artifact)

    print(f"Raw Lua evidence: {artifact['summary']['evidence_total']}")
    print(f"Files extracted: {artifact['summary']['files_extracted']}")
    print(f"Digest mismatches: {artifact['summary']['digest_mismatch_files']}")
    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD: {out_md}")


if __name__ == "__main__":
    main()
