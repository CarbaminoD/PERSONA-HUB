# AGENTS.md — PersonaHub

ไฟล์กลางสำหรับ AI agent ทุกตัว (Codex, Claude Code, Gemini CLI) — `CLAUDE.md` และ `GEMINI.md` แค่ import ไฟล์นี้ แก้กฎที่นี่ที่เดียว

## Commit Messages

Use **Conventional Commits** format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Types

| Type | ใช้เมื่อ |
|------|----------|
| `feat` | เพิ่ม feature ใหม่ |
| `fix` | แก้ bug |
| `refactor` | ปรับโค้ดโดยไม่เปลี่ยน behavior |
| `perf` | ปรับปรุง performance |
| `style` | แก้ formatting, whitespace (ไม่เปลี่ยน logic) |
| `docs` | แก้เอกสาร |
| `test` | เพิ่ม/แก้ test |
| `chore` | งาน maintenance เช่น config, dependencies |

### Scope (optional)

ใส่ชื่อ module หรือ feature ที่เกี่ยวข้อง เช่น `persona`, `character-sheet`, `prompt`, `template`

### Examples

```
feat(character-sheet): add Aiko v1.4 beach variant with chubby build

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

```
fix(prompt): adjust body description wording to pass image-gen guardrails

Remove explicit measurements and trigger words (curvaceous, fleshy)
while preserving the intended character silhouette.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### Rules

- Subject line ไม่เกิน 72 ตัวอักษร
- ใช้ **imperative mood** — "add" ไม่ใช่ "added" หรือ "adds"
- ไม่ต้องจบด้วยจุด (.)
- Body อธิบาย **why** ไม่ใช่ **what**
- **REQUIRED**: Include footer `Co-Authored-By: <AI model ที่ใช้>` เสมอ เช่น `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` เสมอ