# External Authorities

## SIGNALIS AI Repository

https://github.com/stalkerGrip/signalis-ai

Primary source for:

- doctrine
- subsystem docs
- investigations
- semantic artifacts
- pipeline architecture

Use when repository context is required.

---

## NutScript

https://github.com/NutScript/NutScript

Authoritative reference for:

- NutScript lifecycle
- character system
- inventory system
- plugin loading
- netstream behavior
- framework hooks

Use when determining baseline framework behavior.

Do not assume SIGNALIS follows NutScript exactly.

SIGNALIS overrides may exist.

---

## Facepunch Wiki

https://wiki.facepunch.com/gmod/

Authoritative reference for:

- GLua language behavior
- hook system
- timer system
- net library
- entity lifecycle
- rendering
- realm behavior

Use when validating Garry's Mod engine semantics.

---

## Authority Order

For SIGNALIS-specific behavior:

SIGNALIS topology
→ SIGNALIS doctrine
→ SIGNALIS subsystem docs
→ SIGNALIS source code
→ human validation
→ NutScript
→ Facepunch Wiki

For engine behavior:

Facepunch Wiki
→ source validation

For framework behavior:

NutScript
→ source validation

Do not use Facepunch or NutScript to override confirmed SIGNALIS behavior.