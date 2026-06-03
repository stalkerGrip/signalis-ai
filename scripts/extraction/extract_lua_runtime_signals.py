from __future__ import annotations

import argparse, hashlib, json, re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

PIPELINE_CONTRACT = {
    "script_id": "scripts.extraction.extract_lua_runtime_signals",
    "purpose": "Execute lua_syntax_alphabet-declared generic Lua syntax extraction entities against files listed in source_file_manifest.",
    "pipeline_stage": "extraction",
    "input_families": ["source_file_manifest", "lua_syntax_alphabet"],
    "required_input_capabilities": ["source_roots", "source_files", "file_realm_hints", "file_digests", "syntax_extraction_rules"],
    "output_families": ["raw_lua_extraction"],
    "required_output_capabilities": ["source_manifest_reference", "lua_syntax_alphabet_reference", "file_digest_verification", "line_evidence"],
    "output_schemas": ["raw_lua_extraction"],
    "artifact_patterns": ["manifests/extraction/raw_lua_extraction.json", "manifests/extraction/raw_lua_extraction.md"],
    "promotion_role": "intermediate_evidence",
    "canonical_status": "active",
}
SCRIPT_ID="scripts.extraction.extract_lua_runtime_signals"; SCHEMA="raw_lua_extraction"; SCHEMA_VERSION="1"; ARTIFACT_FAMILY="raw_lua_extraction"

@dataclass
class SyntaxContext:
    kind: str
    start_line: int
    label: str|None
    open_function_depth: int

@dataclass
class ArgumentSpan:
    text: str
    start_line: int
    end_line: int

@dataclass
class Alphabet:
    path: str
    artifact_id: str|None
    content_digest: str|None
    regex: dict[str,str]
    regex_flags: dict[str,list[str]]
    syntax_entities: list[dict[str,Any]]
    mechanics: dict[str,Any]
    value_rules: list[dict[str,Any]]
    value_detection: dict[str,str]
    literal_tokens: dict[str,list[str]]
    control_call_words: set[str]
    block_tokens: dict[str,list[str]]


def stable_hash(v: Any)->str:
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode()).hexdigest()

def file_sha256(path: Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def normalize_path(p: Path|str)->str:
    return Path(p).as_posix() if isinstance(p,Path) else str(p).replace('\\','/')

def load_json(path: Path)->dict[str,Any]:
    data=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data,dict): raise ValueError(f"JSON root must be object: {path}")
    return data

def load_alphabet(path: Path)->Alphabet:
    data=load_json(path)
    if data.get('schema')!='lua_syntax_alphabet' or data.get('artifact_family')!='lua_syntax_alphabet':
        raise ValueError(f"Input is not lua_syntax_alphabet: {path}")
    entities=data.get('syntax_entities')
    if not isinstance(entities,list) or not entities:
        raise ValueError('lua_syntax_alphabet.syntax_entities must be a non-empty list')
    return Alphabet(
        path=normalize_path(path), artifact_id=data.get('artifact_id'), content_digest=data.get('content_digest'),
        regex={str(k):str(v) for k,v in data.get('regex',{}).items()},
        regex_flags={str(k):[str(x) for x in v] for k,v in data.get('regex_flags',{}).items()},
        syntax_entities=[dict(x) for x in entities if dict(x).get('enabled', True)],
        mechanics=dict(data.get('mechanics',{})),
        value_rules=[dict(x) for x in data.get('value_classification_rules',[])],
        value_detection={str(k):str(v) for k,v in data.get('value_detection',{}).items()},
        literal_tokens={str(k):[str(x) for x in v] for k,v in data.get('literal_tokens',{}).items()},
        control_call_words={str(x) for x in data.get('control_call_words',[])},
        block_tokens={str(k):[str(x) for x in v] for k,v in data.get('block_tokens',{}).items()},
    )

def compile_patterns(a: Alphabet)->dict[str,re.Pattern[str]]:
    flag_map={'DOTALL':re.DOTALL, 'MULTILINE':re.MULTILINE, 'IGNORECASE':re.IGNORECASE}
    out={}
    for name, pat in a.regex.items():
        flags=0
        for f in a.regex_flags.get(name,[]): flags |= flag_map.get(f,0)
        out[name]=re.compile(pat, flags)
    return out

def entity_by_operation(a: Alphabet, op: str)->list[dict[str,Any]]:
    return [e for e in a.syntax_entities if e.get('parser_operation')==op]

def first_entity(a: Alphabet, op: str)->dict[str,Any]|None:
    xs=entity_by_operation(a,op); return xs[0] if xs else None

def pattern(patterns: dict[str,re.Pattern[str]], name: str)->re.Pattern[str]:
    if name not in patterns: raise ValueError(f"Alphabet regex not found: {name}")
    return patterns[name]

def read_text_lossless(path: Path)->tuple[str,str]:
    raw=path.read_bytes()
    try: return raw.decode('utf-8'), 'utf-8'
    except UnicodeDecodeError: return raw.decode('utf-8', errors='replace'), 'utf-8-replace'

def strip_line_comment(line: str)->str:
    in_s=in_d=esc=False; i=0
    while i<len(line):
        ch=line[i]; nx=line[i+1] if i+1<len(line) else ''
        if esc: esc=False
        elif ch=='\\' and (in_s or in_d): esc=True
        elif ch=="'" and not in_d: in_s=not in_s
        elif ch=='"' and not in_s: in_d=not in_d
        elif ch=='-' and nx=='-' and not in_s and not in_d: return line[:i]
        i+=1
    return line

def mask_strings(line: str, patterns: dict[str,re.Pattern[str]])->str:
    if 'string_literal' not in patterns: return line
    return patterns['string_literal'].sub(lambda m:m.group('quote')+('_'*len(m.group('value')))+m.group('quote'), line)

def split_params(params: str)->list[str]: return [p.strip() for p in params.split(',') if p.strip()]

def classify_value(value: str, a: Alphabet, patterns: dict[str,re.Pattern[str]])->str:
    s=value.strip().rstrip(',').strip()
    for rule in a.value_rules:
        m=rule.get('match')
        if m=='empty' and s=='': return str(rule['value_kind'])
        if m=='startswith' and s.startswith(str(rule.get('value',''))): return str(rule['value_kind'])
        if m=='token_list' and s in set(a.literal_tokens.get(str(rule.get('tokens')), [])): return str(rule['value_kind'])
        if m=='regex_fullmatch':
            name=str(rule.get('regex'))
            pat=a.value_detection.get(name, a.regex.get(name))
            if pat and re.fullmatch(pat, s): return str(rule['value_kind'])
        if m=='compiled_regex_fullmatch':
            name=str(rule.get('regex'))
            if name in patterns and patterns[name].fullmatch(s): return str(rule['value_kind'])
        if m=='fallback': return str(rule['value_kind'])
    return 'unclassified'

def line_evidence(file_record: dict[str,Any], line_no:int, line:str)->dict[str,Any]:
    return {"file_id":file_record.get('file_id'),"source_root_index":file_record.get('source_root_index'),"relative_path":file_record.get('relative_path'),"absolute_path":file_record.get('absolute_path'),"realm_hint":file_record.get('realm_hint'),"line":line_no,"text":line.rstrip('\n')}

def emit(kind: str, file_record:dict[str,Any], line_no:int, line:str, payload:dict[str,Any])->dict[str,Any]:
    e={"kind":kind,"evidence_id":"raw_lua_evidence:"+stable_hash({"kind":kind,"file_id":file_record.get('file_id'),"line":line_no,"payload":payload,"text":line.rstrip('\n')})[:16],"evidence":line_evidence(file_record,line_no,line)}
    e.update(payload); return e

def symbol_shape(target: str)->dict[str,Any]:
    # Syntax-only symbol shape. For ordinary targets this preserves the old
    # qualified-symbol behavior. For call-selected targets such as
    # client:getChar():getInv():add, keep the full syntactic target while
    # deriving root/leaf/parts from identifier tokens and separators from the
    # punctuation between them.
    parts=re.findall(r"[A-Za-z_][A-Za-z0-9_]*", target)
    seps=[]
    for m in re.finditer(r"[.:]\s*[A-Za-z_][A-Za-z0-9_]*", target):
        seps.append(m.group(0).strip()[0])
    return {"target":target,"root":parts[0] if parts else target,"leaf":parts[-1] if parts else target,"parts":parts,"separators":seps,"uses_method_colon":':' in seps,"uses_table_dot":'.' in seps,"is_call_chain":'()' in target}

def context_path(stack:list[SyntaxContext])->list[dict[str,Any]]:
    return [{"kind":c.kind,"start_line":c.start_line,"label":c.label} for c in stack]

def computed_key_payload(raw_key:str,a:Alphabet)->dict[str,Any]:
    key=raw_key.strip(); mech=a.mechanics
    if key.startswith('[') and key.endswith(']'):
        expr=key[1:-1].strip(); return {"key_syntax":mech.get('key_syntax_computed','computed_key'),"key_text":key,"key_expression":expr,"key_expression_kind":"expression"}
    return {"key_syntax":mech.get('key_syntax_identifier','identifier_key'),"key_text":key,"key_expression":key,"key_expression_kind":mech.get('identifier_key_expression_kind','identifier')}

def tokenized_block_end_line(lines:list[str], start_line:int, a:Alphabet, patterns:dict[str,re.Pattern[str]])->int|None:
    stack=[]; tok_re=patterns.get('block_token');
    if not tok_re: return None
    opens=set(a.block_tokens.get('open',[])); closes=set(a.block_tokens.get('close',[]))
    previous_significant_code=''
    def then_belongs_to_elseif(code:str, token_start:int)->bool:
        before=code[:token_start]
        # Same-line `elseif cond then` does not create a new nested block.
        if re.search(r"\belseif\b[^;]*$", before): return True
        # Split-line style:
        #   elseif cond
        #   then
        stripped_before=before.strip()
        if not stripped_before and re.match(r"^\s*then\b", code[token_start:]):
            return bool(re.match(r"^\s*elseif\b", previous_significant_code))
        return False
    for li in range(start_line-1, len(lines)):
        code=mask_strings(strip_line_comment(lines[li]), patterns)
        for mt in tok_re.finditer(code):
            tok=mt.group(1)
            if tok in opens:
                if tok=='then' and then_belongs_to_elseif(code, mt.start(1)):
                    continue
                stack.append(tok)
            elif tok in closes:
                if tok=='until':
                    for i in range(len(stack)-1,-1,-1):
                        if stack[i]=='repeat': del stack[i:]; break
                elif stack:
                    stack.pop()
                    if not stack: return li+1
        if code.strip(): previous_significant_code=code
    return None

def table_literal_end_line(lines:list[str], start_line:int, patterns:dict[str,re.Pattern[str]])->int|None:
    depth=0; seen=False
    for li in range(start_line-1,len(lines)):
        code=mask_strings(strip_line_comment(lines[li]), patterns)
        for ch in code:
            if ch=='{': depth+=1; seen=True
            elif ch=='}' and seen:
                depth-=1
                if depth<=0: return li+1
    return None

def body_span_for_value(lines:list[str], start_line:int, value_kind:str, a:Alphabet, patterns:dict[str,re.Pattern[str]])->dict[str,Any]:
    if value_kind==a.mechanics.get('function_body_value_kind'):
        end=tokenized_block_end_line(lines,start_line,a,patterns)
    elif value_kind==a.mechanics.get('table_body_value_kind'):
        end=table_literal_end_line(lines,start_line,patterns)
    else: end=None
    return {"start_line":start_line,"end_line":end,"complete":end is not None}

def discover_function_ranges(lines:list[str], a:Alphabet, patterns:dict[str,re.Pattern[str]])->list[tuple[int,int]]:
    ranges=[]
    for idx,line in enumerate(lines,1):
        code=strip_line_comment(line)
        for op in ['function_definition','assigned_function','local_assigned_function']:
            ent=first_entity(a,op)
            if ent and pattern(patterns, ent['regex']).match(code):
                end=tokenized_block_end_line(lines,idx,a,patterns)
                if end: ranges.append((idx,end))
        # table field function literal
        ent=first_entity(a,'table_field')
        if ent:
            m=pattern(patterns,ent['regex']).match(code)
            if m and classify_value(m.group('value'),a,patterns)==a.mechanics.get('function_body_value_kind'):
                end=tokenized_block_end_line(lines,idx,a,patterns)
                if end: ranges.append((idx,end))
    return ranges

def function_depth_at(line_no:int, ranges:list[tuple[int,int]])->int:
    return sum(1 for s,e in ranges if s < line_no < e)

def current_table_context(stack:list[SyntaxContext], function_depth:int, same_depth:bool)->SyntaxContext|None:
    for c in reversed(stack):
        if c.kind=='table' and (not same_depth or c.open_function_depth==function_depth): return c
    return None

def close_leading_table_context(code:str, stack:list[SyntaxContext], patterns:dict[str,re.Pattern[str]])->None:
    if mask_strings(code,patterns).strip().startswith('}'):
        for i in range(len(stack)-1,-1,-1):
            if stack[i].kind=='table': del stack[i:]; break

def update_table_context_after_line(code:str,line_no:int,stack:list[SyntaxContext],label:str|None,function_depth:int,a:Alphabet,patterns:dict[str,re.Pattern[str]]):
    masked=mask_strings(code,patterns); stripped=masked.strip(); leading_close=1 if stripped.startswith('}') else 0
    opens=masked.count('{'); closes=max(0, masked.count('}')-leading_close)
    for i in range(opens): stack.append(SyntaxContext(a.mechanics.get('context_kind_table','table'), line_no, label if i==0 else None, function_depth))
    for _ in range(closes):
        for j in range(len(stack)-1,-1,-1):
            if stack[j].kind==a.mechanics.get('context_kind_table','table'): del stack[j:]; break

def split_args_with_spans(args:str, base_line:int, a:Alphabet, patterns:dict[str,re.Pattern[str]])->list[ArgumentSpan]:
    spans=[]; start=0; depth=0; block=0; ins=ind=esc=False; i=0; tok_re=patterns.get('block_token')
    opens=set(a.block_tokens.get('open',[])); closes=set(a.block_tokens.get('close',[]))
    def line_for(o:int)->int: return base_line+args.count('\n',0,max(0,min(o,len(args))))
    def append(s:int,e:int):
        raw=args[s:e]; st=raw.strip()
        if not st: return
        lead=len(raw)-len(raw.lstrip()); trail=len(raw.rstrip()); a0=s+lead; a1=s+trail
        spans.append(ArgumentSpan(st,line_for(a0),line_for(max(a0,a1-1))))
    while i<len(args):
        ch=args[i]
        if esc: esc=False; i+=1; continue
        if ch=='\\' and (ins or ind): esc=True; i+=1; continue
        if ch=="'" and not ind: ins=not ins; i+=1; continue
        if ch=='"' and not ins: ind=not ind; i+=1; continue
        if ins or ind: i+=1; continue
        if tok_re:
            mt=tok_re.match(args,i)
            if mt:
                tok=mt.group(1)
                if tok in opens: block+=1
                elif tok in closes and block>0: block-=1
                i=mt.end(); continue
        if ch in '({[': depth+=1
        elif ch in ')}]' and depth>0: depth-=1
        elif ch==',' and depth==0 and block==0: append(start,i); start=i+1
        i+=1
    append(start,len(args)); return spans

def extract_call_arguments(code_line:str, call_start:int)->tuple[str,bool]:
    oi=code_line.find('(',call_start)
    if oi<0: return '',False
    depth=0; ins=ind=esc=False
    for idx in range(oi,len(code_line)):
        ch=code_line[idx]
        if esc: esc=False; continue
        if ch=='\\' and (ins or ind): esc=True; continue
        if ch=="'" and not ind: ins=not ins; continue
        if ch=='"' and not ins: ind=not ind; continue
        if ins or ind: continue
        if ch=='(': depth+=1
        elif ch==')':
            depth-=1
            if depth==0: return code_line[oi+1:idx], True
    return code_line[oi+1:], False

def find_call_close_index(code_line:str, call_start:int)->int|None:
    oi=code_line.find('(',call_start)
    if oi<0: return None
    depth=0; ins=ind=esc=False
    for idx in range(oi,len(code_line)):
        ch=code_line[idx]
        if esc: esc=False; continue
        if ch=='\\' and (ins or ind): esc=True; continue
        if ch=="'" and not ind: ins=not ins; continue
        if ch=='"' and not ins: ind=not ind; continue
        if ins or ind: continue
        if ch=='(': depth+=1
        elif ch==')':
            depth-=1
            if depth==0: return idx
    return None

def call_target_with_result_suffix(previous_target:str, sep:str, leaf:str)->str:
    # The target is syntax evidence for callable selection from a previous call
    # result. It does not classify runtime meaning.
    return f"{previous_target}(){sep}{leaf}"

def is_single_assignment_operator(code:str, pos:int)->bool:
    if pos < 0 or pos >= len(code) or code[pos] != '=': return False
    prev = code[pos-1] if pos > 0 else ''
    nxt = code[pos+1] if pos+1 < len(code) else ''
    return prev not in '<>~=' and nxt != '='

def statement_boundary_start(masked_left:str, a:Alphabet)->int:
    # Generic Lua/GLua statement boundary. This is syntax-only: inline statements
    # such as `if cond then x = y end` own the assignment after `then`, not the
    # full control statement prefix.
    boundary = -1
    for m in re.finditer(r";", masked_left): boundary = max(boundary, m.end()-1)
    for word in a.mechanics.get('inline_assignment_left_boundary_tokens', ['then','do']):
        for m in re.finditer(rf"\b{re.escape(str(word))}\b", masked_left):
            boundary = max(boundary, m.end())
    return boundary + 1

def statement_boundary_end(masked_right:str, a:Alphabet)->int:
    depth=0; ins=ind=esc=False; i=0
    right_boundary_tokens={str(x) for x in a.mechanics.get('inline_assignment_right_boundary_tokens', ['end','elseif','else'])}
    while i < len(masked_right):
        ch=masked_right[i]
        if esc: esc=False; i+=1; continue
        if ch=='\\' and (ins or ind): esc=True; i+=1; continue
        if ch=="'" and not ind: ins=not ins; i+=1; continue
        if ch=='"' and not ins: ind=not ind; i+=1; continue
        if ins or ind: i+=1; continue
        if ch in '({[': depth+=1; i+=1; continue
        if ch in ')}]' and depth>0: depth-=1; i+=1; continue
        if depth==0 and ch==';': return i
        if depth==0:
            m=re.match(r"\b([A-Za-z_][A-Za-z0-9_]*)\b", masked_right[i:])
            if m and m.group(1) in right_boundary_tokens:
                before=masked_right[i-1] if i>0 else ' '
                if before.isspace() or before in ';': return i
        i+=1
    return len(masked_right)

def assignment_lhs_is_syntax(lhs:str, a:Alphabet)->bool:
    lhs=lhs.strip()
    if not lhs: return False
    q=a.regex.get('qualified_symbol', r'[A-Za-z_][A-Za-z0-9_]*(?:(?:\.|:)[A-Za-z_][A-Za-z0-9_]*)*')
    return bool(re.fullmatch(rf"(?:{q})(?:\[[^\]]+\])?", lhs))

def extract_assignment_candidates(code:str, a:Alphabet, patterns:dict[str,re.Pattern[str]])->list[tuple[bool,str,str]]:
    masked=mask_strings(code,patterns)
    out=[]
    for m in re.finditer(r"=", masked):
        eq=m.start()
        if not is_single_assignment_operator(masked, eq): continue
        left_start=statement_boundary_start(masked[:eq], a)
        raw_left=code[left_start:eq].strip()
        masked_left=masked[left_start:eq].strip()
        is_local=False
        if re.match(r"^local\s+", masked_left):
            is_local=True
            raw_left=re.sub(r"^local\s+", "", raw_left, count=1).strip()
            # Generic single-name local extraction for this syntax layer.
            if ',' in raw_left: continue
        lhs=raw_left.strip()
        if not assignment_lhs_is_syntax(lhs,a): continue
        right_raw=code[eq+1:]
        right_masked=masked[eq+1:]
        rend=statement_boundary_end(right_masked,a)
        rhs=right_raw[:rend].strip()
        if not rhs: continue
        out.append((is_local,lhs,rhs))
    return out

def extract_multiline_call_arguments(lines:list[str], start_line:int, col:int, a:Alphabet, patterns:dict[str,re.Pattern[str]])->tuple[str,bool,list[ArgumentSpan]]:
    first=strip_line_comment(lines[start_line-1]); oi=first.find('(',col-1)
    if oi<0: return '',False,[]
    chunks=[]; depth=0; started=False; ins=ind=esc=False
    for ln in range(start_line,len(lines)+1):
        code=strip_line_comment(lines[ln-1]); i=oi if ln==start_line else 0
        while i<len(code):
            ch=code[i]
            if esc: esc=False; chunks.append(ch) if started else None; i+=1; continue
            if ch=='\\' and (ins or ind): esc=True; chunks.append(ch) if started else None; i+=1; continue
            if ch=="'" and not ind: ins=not ins; chunks.append(ch) if started else None; i+=1; continue
            if ch=='"' and not ins: ind=not ind; chunks.append(ch) if started else None; i+=1; continue
            if ins or ind: chunks.append(ch) if started else None; i+=1; continue
            if ch=='(':
                depth+=1
                if started: chunks.append(ch)
                else: started=True
                i+=1; continue
            if ch==')':
                depth-=1
                if depth==0 and started:
                    txt=''.join(chunks); return txt, True, split_args_with_spans(txt,start_line,a,patterns)
                if started: chunks.append(ch)
                i+=1; continue
            if started: chunks.append(ch)
            i+=1
        if started: chunks.append('\n')
    txt=''.join(chunks); return txt, False, split_args_with_spans(txt,start_line,a,patterns)

def emit_call_argument(items:list[dict[str,Any]], file_record:dict[str,Any], line_no:int, source_line:str, parent:dict[str,Any], arg_index:int, arg_text:str, start_line:int, end_line:int, lines:list[str], a:Alphabet, patterns:dict[str,re.Pattern[str]])->dict[str,Any]:
    ent_id = parent.get('_argument_entity_id') or 'lua_call_argument'
    kind=classify_value(arg_text,a,patterns)
    payload={"parent_call_evidence_id":parent['evidence_id'],"parent_call_symbol":parent.get('symbol'),"argument_index":arg_index,"argument_kind":kind,"argument_preview":arg_text[:240],"argument_truncated":len(arg_text)>240,"argument_start_line":start_line,"argument_end_line":end_line}
    if kind==a.mechanics.get('function_body_value_kind'):
        payload['anonymous_function_body_span']=body_span_for_value(lines,start_line,kind,a,patterns)
    ev=emit(ent_id,file_record,line_no,source_line,payload); items.append(ev)
    # attached anonymous function evidence from alphabet entity
    anon=first_entity(a,'anonymous_function')
    if anon and kind==a.mechanics.get('function_body_value_kind') and a.mechanics.get('anonymous_function_arguments_attach_to_parent_call_argument', True):
        mm=re.search(r"function\s*\(([^)]*)\)", arg_text)
        items.append(emit(anon['id'], file_record, start_line, source_line, {"parameters":split_params(mm.group(1)) if mm else [],"body_span":body_span_for_value(lines,start_line,kind,a,patterns),"parent_call_evidence_id":parent['evidence_id'],"parent_call_argument_evidence_id":ev['evidence_id'],"parent_call_argument_index":arg_index}))
    return ev

def count_by(items:Iterable[dict[str,Any]], key:str)->dict[str,int]:
    d={}
    for it in items:
        v=str(it.get(key,'unknown')); d[v]=d.get(v,0)+1
    return dict(sorted(d.items()))

def extract_from_file(file_record:dict[str,Any], max_string_length:int, a:Alphabet, patterns:dict[str,re.Pattern[str]])->tuple[list[dict[str,Any]],dict[str,Any]]:
    path=Path(str(file_record['absolute_path'])); expected=str(file_record.get('sha256','')); actual=file_sha256(path)
    text,enc=read_text_lossless(path); lines=text.splitlines(); ranges=discover_function_ranges(lines,a,patterns)
    items=[]; stack=[]
    for idx,raw in enumerate(lines,1):
        code=strip_line_comment(raw)
        if not code.strip(): continue
        fdepth=function_depth_at(idx,ranges)
        close_leading_table_context(code,stack,patterns)
        table_label_to_open=None; suppressed=set(); declaration_line=False
        # table field first if declared
        for ent in entity_by_operation(a,'table_field'):
            ctx=current_table_context(stack, fdepth, bool(ent.get('requires_same_function_depth_as_table')))
            if not ctx: continue
            m=pattern(patterns,ent['regex']).match(code)
            if not m: continue
            val=m.group('value').strip(); vk=classify_value(val,a,patterns); kp=computed_key_payload(m.group('key'),a)
            payload={**kp,"value_kind":vk,"value_preview":val[:240],"value_truncated":len(val)>240,"table_depth":len([c for c in stack if c.kind==a.mechanics.get('context_kind_table','table')]),"context_path":context_path(stack)}
            if vk in set(a.mechanics.get('body_span_value_kinds',[])): payload['value_body_span']=body_span_for_value(lines,idx,vk,a,patterns)
            items.append(emit(ent['id'],file_record,idx,raw,payload)); suppressed.update(ent.get('suppresses',[]))
            if vk==a.mechanics.get('table_body_value_kind'): table_label_to_open=kp['key_text']
            break
        # assignments
        assignment_ent_by_local = {
            True: first_entity(a,'local_assignment'),
            False: first_entity(a,'assignment'),
        }
        for is_local,lhs,rhs in extract_assignment_candidates(code,a,patterns):
            ent=assignment_ent_by_local.get(is_local)
            if not ent or ent['id'] in suppressed: continue
            rk=classify_value(rhs,a,patterns)
            payload={"lhs":lhs,"is_local":is_local,"rhs_kind":rk,"rhs_preview":rhs[:240],"rhs_truncated":len(rhs)>240}
            if rk in set(a.mechanics.get('body_span_value_kinds',[])): payload['rhs_body_span']=body_span_for_value(lines,idx,rk,a,patterns)
            items.append(emit(ent['id'],file_record,idx,raw,payload))
            if rk==ent.get('opens_table_context_when_value_kind'): table_label_to_open=lhs
            suppressed.add(ent['id'])
            break
        # function declarations / assignments
        owned_function_literal_line=False
        for it in items:
            if it.get('evidence',{}).get('file_id')==file_record.get('file_id') and it.get('evidence',{}).get('line')==idx:
                if it.get('rhs_kind')==a.mechanics.get('function_body_value_kind') or it.get('value_kind')==a.mechanics.get('function_body_value_kind'):
                    owned_function_literal_line=True
        for op in ['function_definition','assigned_function','local_assigned_function']:
            for ent in entity_by_operation(a,op):
                if ent['id'] in suppressed: continue
                if owned_function_literal_line and ent.get('suppressed_when_assignment_rhs_is_function_literal', False): continue
                m=pattern(patterns,ent['regex']).match(code)
                if not m: continue
                declaration_line=True; owned_function_literal_line=True
                if op=='function_definition':
                    local_marker,name,params=m.groups(); payload={"definition_form":a.mechanics.get('definition_form_function_statement','function_statement'),"is_local":bool(local_marker),"symbol":symbol_shape(name),"parameters":split_params(params),"body_span":body_span_for_value(lines,idx,a.mechanics.get('function_body_value_kind'),a,patterns)}
                elif op=='assigned_function':
                    lhs,params=m.groups(); payload={"is_local":False,"lhs":lhs,"symbol":symbol_shape(lhs) if re.fullmatch(a.regex.get('qualified_symbol','.*'),lhs) else {"target":lhs},"parameters":split_params(params),"body_span":body_span_for_value(lines,idx,a.mechanics.get('function_body_value_kind'),a,patterns)}
                else:
                    lhs,params=m.groups(); payload={"is_local":True,"lhs":lhs,"symbol":symbol_shape(lhs),"parameters":split_params(params),"body_span":body_span_for_value(lines,idx,a.mechanics.get('function_body_value_kind'),a,patterns)}
                items.append(emit(ent['id'],file_record,idx,raw,payload))
        # inline anonymous function not already declaration and not call-argument attached.
        # Owned function literals are governed by their owner evidence unless the
        # alphabet explicitly allows standalone anonymous evidence for them.
        anon=first_entity(a,'anonymous_function')
        emit_owned_anon=bool(a.mechanics.get('owned_function_literals_emit_anonymous_function_evidence', False))
        if anon and 'function' in code and not declaration_line and (emit_owned_anon or not owned_function_literal_line):
            for mm in re.finditer(r"function\s*\(([^)]*)\)", code):
                items.append(emit(anon['id'],file_record,idx,raw,{"parameters":split_params(mm.group(1)),"column":mm.start()+1,"body_span":body_span_for_value(lines,idx,a.mechanics.get('function_body_value_kind'),a,patterns),"context_path":context_path(stack)}))
        # calls
        call_ent=first_entity(a,'call_expression')
        if call_ent and not (declaration_line and a.mechanics.get('function_definition_lines_are_not_call_expression_lines', True)):
            close_to_target:dict[int,str]={}
            close_to_evidence:dict[int,dict[str,Any]]={}
            emitted_call_spans:set[tuple[int,int]]=set()
            def emit_call_from_match(target:str, col0:int, ent:dict[str,Any], parent_ev:dict[str,Any]|None=None):
                argtxt,complete=extract_call_arguments(code,col0)
                argspans=split_args_with_spans(argtxt,idx,a,patterns) if complete else []
                kind=ent.get('method_kind_id') if ':' in target and ent.get('method_kind_id') else ent['id']
                payload={"symbol":symbol_shape(target),"column":col0+1,"arguments_preview":argtxt[:240],"arguments_truncated":len(argtxt)>240,"arguments_complete_on_line":complete,"argument_count_on_line":len(argspans),"argument_kinds_on_line":[classify_value(sx.text,a,patterns) for sx in argspans]}
                if parent_ev is not None:
                    payload['call_chain_parent_evidence_id']=parent_ev.get('evidence_id')
                    payload['call_chain_parent_symbol']=parent_ev.get('symbol')
                ev=emit(str(kind),file_record,idx,raw,payload)
                ev['_argument_entity_id']=ent.get('argument_entity_id')
                items.append(ev)
                if not complete:
                    matxt,mcomp,argspans=extract_multiline_call_arguments(lines,idx,col0+1,a,patterns)
                    ev.update({"arguments_complete_multiline":mcomp,"argument_count_multiline":len(argspans),"argument_kinds_multiline":[classify_value(sx.text,a,patterns) for sx in argspans],"arguments_multiline_preview":matxt[:240],"arguments_multiline_truncated":len(matxt)>240})
                for ai,sp in enumerate(argspans): emit_call_argument(items,file_record,sp.start_line,lines[sp.start_line-1],ev,ai,sp.text,sp.start_line,sp.end_line,lines,a,patterns)
                ev.pop('_argument_entity_id',None)
                close_idx=find_call_close_index(code,col0)
                if close_idx is not None:
                    close_to_target[close_idx]=target
                    close_to_evidence[close_idx]=ev
                emitted_call_spans.add((col0, close_idx if close_idx is not None else col0))
                return ev
            for cm in pattern(patterns,call_ent['regex']).finditer(code):
                target=cm.group('target')
                if target in a.control_call_words: continue
                emit_call_from_match(target,cm.start('target'),call_ent)
            for chain_ent in entity_by_operation(a,'call_after_call_result'):
                if not a.mechanics.get('call_after_call_result_enabled', True): continue
                for cm in pattern(patterns,chain_ent['regex']).finditer(code):
                    previous_target=close_to_target.get(cm.start())
                    if not previous_target: continue
                    sep=cm.groupdict().get('sep') or ':'
                    leaf=cm.groupdict().get('leaf') or ''
                    target=call_target_with_result_suffix(previous_target,sep,leaf)
                    parent_ev=close_to_evidence.get(cm.start())
                    emit_call_from_match(target,cm.start('leaf'),chain_ent,parent_ev)
        # quoted string literals
        lit=first_entity(a,'quoted_string_literal')
        if lit:
            for sm in pattern(patterns,lit['regex']).finditer(code):
                val=sm.group('value'); items.append(emit(lit['id'],file_record,idx,raw,{"literal_kind":lit.get('literal_kind'),"literal_form":lit.get('literal_form'),"quote":sm.group('quote'),"value":val[:max_string_length],"value_truncated":len(val)>max_string_length,"length":len(val),"column":sm.start()+1}))
        update_table_context_after_line(code,idx,stack,table_label_to_open,fdepth,a,patterns)
    long_lit=first_entity(a,'long_bracket_string_literal')
    if long_lit:
        for lm in pattern(patterns,long_lit['regex']).finditer(text):
            line_no=text.count('\n',0,lm.start())+1; val=lm.group(2); src=lines[line_no-1] if line_no-1<len(lines) else ''
            items.append(emit(long_lit['id'],file_record,line_no,src,{"literal_kind":long_lit.get('literal_kind'),"literal_form":long_lit.get('literal_form'),"equals_depth":len(lm.group(1)),"value":val[:max_string_length],"value_truncated":len(val)>max_string_length,"length":len(val),"column":1}))
    summary={"file_id":file_record.get('file_id'),"relative_path":file_record.get('relative_path'),"absolute_path":file_record.get('absolute_path'),"realm_hint":file_record.get('realm_hint'),"expected_sha256":expected,"actual_sha256":actual,"digest_status":"match" if actual==expected else "mismatch","encoding":enc,"line_count":len(lines),"evidence_total":len(items),"evidence_kind_counts":count_by(items,'kind')}
    return items,summary

def validate_manifest(manifest:dict[str,Any], path:Path):
    if manifest.get('schema')!='source_file_manifest' or manifest.get('artifact_family')!='source_file_manifest': raise ValueError(f"Input is not source_file_manifest: {path}")
    if not isinstance(manifest.get('source_files'),list): raise ValueError('source_files must be list')

def build_artifact(workspace:Path,input_manifest_path:Path,alphabet_path:Path,max_string_length:int,fail_on_digest_mismatch:bool)->dict[str,Any]:
    manifest=load_json(input_manifest_path); validate_manifest(manifest,input_manifest_path)
    a=load_alphabet(alphabet_path); patterns=compile_patterns(a)
    items=[]; summaries=[]; errors=[]
    for rec in manifest['source_files']:
        try:
            ev,sm=extract_from_file(rec,max_string_length,a,patterns); items.extend(ev); summaries.append(sm)
        except Exception as ex:
            errors.append({"file_id":rec.get('file_id'),"relative_path":rec.get('relative_path'),"absolute_path":rec.get('absolute_path'),"error_type":type(ex).__name__,"message":str(ex)})
    mism=[x for x in summaries if x['digest_status']!='match']
    if fail_on_digest_mismatch and mism: raise ValueError(f"Digest mismatch in {len(mism)} files")
    content_digest=stable_hash({"source_manifest":manifest.get('artifact_id'),"lua_syntax_alphabet":a.artifact_id,"file_summaries":[{"file_id":x['file_id'],"actual_sha256":x['actual_sha256'],"evidence_total":x['evidence_total'],"evidence_kind_counts":x['evidence_kind_counts'],"digest_status":x['digest_status']} for x in summaries],"errors":errors,"evidence_items":[{"evidence_id":x['evidence_id'],"kind":x['kind'],"file_id":x['evidence']['file_id'],"line":x['evidence']['line']} for x in items]})
    return {"schema":SCHEMA,"schema_version":SCHEMA_VERSION,"artifact_family":ARTIFACT_FAMILY,"artifact_id":f"{ARTIFACT_FAMILY}:{content_digest[:16]}","producer_script":SCRIPT_ID,"pipeline_stage":"extraction","canonical_status":"intermediate","promotion_role":"intermediate_evidence","generated_at":datetime.utcnow().replace(microsecond=0).isoformat()+"Z","required_capabilities":PIPELINE_CONTRACT['required_output_capabilities'],"content_digest":content_digest,"workspace":normalize_path(workspace),"source_manifest":{"path":normalize_path(input_manifest_path),"artifact_id":manifest.get('artifact_id'),"content_digest":manifest.get('content_digest'),"schema":manifest.get('schema'),"schema_version":manifest.get('schema_version')},"lua_syntax_alphabet":{"path":a.path,"artifact_id":a.artifact_id,"content_digest":a.content_digest},"summary":{"files_total":len(manifest['source_files']),"files_extracted":len(summaries),"files_failed":len(errors),"digest_mismatch_files":len(mism),"evidence_total":len(items),"evidence_kind_counts":count_by(items,'kind'),"realm_hint_counts":count_by(summaries,'realm_hint')},"file_summaries":summaries,"evidence_items":items,"errors":errors,"lineage":{"input_kind":"pipeline_artifact","input_artifacts":[normalize_path(input_manifest_path),normalize_path(alphabet_path)],"parent_artifact_id":manifest.get('artifact_id'),"regenerates":None,"regeneration_inputs":{"producer_script":SCRIPT_ID,"schema":SCHEMA,"schema_version":SCHEMA_VERSION,"source_file_manifest":normalize_path(input_manifest_path),"source_file_manifest_artifact_id":manifest.get('artifact_id'),"lua_syntax_alphabet":normalize_path(alphabet_path),"lua_syntax_alphabet_artifact_id":a.artifact_id,"max_string_length":max_string_length}}}

def write_json(path:Path, artifact:dict[str,Any]): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(artifact,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def write_md(path:Path, artifact:dict[str,Any]):
    path.parent.mkdir(parents=True,exist_ok=True); lines=["# Raw Lua Extraction","",f"- Artifact ID: `{artifact['artifact_id']}`",f"- Producer: `{artifact['producer_script']}`",f"- Source manifest: `{artifact['source_manifest']['path']}`",f"- Lua syntax alphabet: `{artifact['lua_syntax_alphabet']['path']}`","","## Summary"]
    for k,v in artifact['summary'].items(): lines.append(f"- `{k}`: `{v}`")
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def parse_args():
    p=argparse.ArgumentParser(description='Execute lua_syntax_alphabet-declared Lua syntax extraction rules.')
    p.add_argument('--workspace',required=True); p.add_argument('--input-manifest'); p.add_argument('--lua-syntax-alphabet'); p.add_argument('--out-json'); p.add_argument('--out-md'); p.add_argument('--max-string-length',type=int,default=500); p.add_argument('--fail-on-digest-mismatch',action='store_true')
    return p.parse_args()

def main():
    args=parse_args(); ws=Path(args.workspace).resolve()
    if not ws.is_dir(): raise NotADirectoryError(f"Workspace is not a directory: {ws}")
    im=Path(args.input_manifest) if args.input_manifest else ws/'manifests'/'extraction'/'source_file_manifest.json'; im=(ws/im).resolve() if not im.is_absolute() else im.resolve()
    al=Path(args.lua_syntax_alphabet) if args.lua_syntax_alphabet else ws/'manifests'/'alphabet'/'lua_syntax_alphabet.json'; al=(ws/al).resolve() if not al.is_absolute() else al.resolve()
    art=build_artifact(ws,im,al,args.max_string_length,args.fail_on_digest_mismatch)
    oj=Path(args.out_json) if args.out_json else ws/'manifests'/'extraction'/'raw_lua_extraction.json'; oj=(ws/oj).resolve() if not oj.is_absolute() else oj.resolve()
    om=Path(args.out_md) if args.out_md else ws/'manifests'/'extraction'/'raw_lua_extraction.md'; om=(ws/om).resolve() if not om.is_absolute() else om.resolve()
    write_json(oj,art); write_md(om,art)
    print(f"Raw Lua evidence: {art['summary']['evidence_total']}"); print(f"Files extracted: {art['summary']['files_extracted']}"); print(f"Digest mismatches: {art['summary']['digest_mismatch_files']}"); print(f"Wrote JSON: {oj}"); print(f"Wrote MD: {om}")
if __name__=='__main__': main()
