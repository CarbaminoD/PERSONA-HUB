# AGENTS.md — PersonaHub

ไฟล์กลางสำหรับ AI agent ทุกตัว (Codex, Claude Code, Gemini CLI) — `CLAUDE.md` และ `GEMINI.md` แค่ import ไฟล์นี้ แก้กฎที่นี่ที่เดียว

## Git Workflow

- ทำงานและ commit บน `main` ได้ ถ้าแตก branch ให้ขึ้นต้นด้วย `feature/`, `fix/`, `refactor/` ตาม type ของงาน
- merge ข้าม branch ทุกครั้งต้องใช้ `git merge --no-ff` ห้าม fast-forward (ทั้ง branch งาน → `main` และ `main` → branch งาน) การ `git pull` branch เดียวกันจาก origin ไม่นับ
- ห้าม commit ข้อมูลลับ (`.env*`, token, key)

## Conventions

- อัปเดตไฟล์นี้ทุกครั้งที่โครงสร้าง repo หรือวิธีทำงานเปลี่ยน
- commit เล็กๆ โดยเน้นทีละเรื่อง พร้อมข้อความที่ชัดเจน

## Commit Messages

ตาม [Conventional Commits](https://www.conventionalcommits.org/) — **type/scope เป็นภาษาอังกฤษเท่านั้น**
ส่วน description ใช้ไทยหรืออังกฤษก็ได้

format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Types

| Type | ใช้เมื่อ |
|------|----------|
| `feat` | เพิ่ม feature หรือเนื้อหาใหม่ |
| `fix` | แก้ bug หรือแก้เนื้อหาที่ผิด |
| `refactor` | ปรับโครงสร้าง/ย้าย/เปลี่ยนชื่อ โดยผลลัพธ์ไม่เปลี่ยน |
| `perf` | ปรับปรุง performance |
| `style` | แก้ formatting, whitespace (ไม่เปลี่ยน logic) |
| `docs` | แก้เอกสาร |
| `test` | เพิ่ม/แก้ test |
| `chore` | งาน maintenance เช่น config, dependencies, `.gitignore` |

### Scope (optional)

ใส่ชื่อ module หรือ feature ที่เกี่ยวข้อง เช่น `persona`, `character-sheet`, `prompt`, `template`, `image-gen`
(ใช้ `image-gen` แบบขีดกลาง ไม่ใช้ `image_gen`)
ถ้าแก้หลายเรื่องพร้อมกันหรือเป็นงานทั่วไป ไม่ต้องใส่ scope

### Examples

```
feat(persona): add new persona profile

Co-Authored-By: <ชื่อโมเดลที่ใช้จริง> <noreply email ของผู้ให้บริการ>
```

```
refactor(template): rename template folders to one naming pattern

Mixed naming made it hard to find the matching template.

Co-Authored-By: <ชื่อโมเดลที่ใช้จริง> <noreply email ของผู้ให้บริการ>
```

### Rules

- Subject line ไม่เกิน 72 ตัวอักษร
- ใช้ **imperative mood** — "add" ไม่ใช่ "added" หรือ "adds"
- ไม่ต้องจบด้วยจุด (.)
- Body อธิบาย **why** ไม่ใช่ **what**
- **REQUIRED**: commit ที่ AI agent ช่วยเขียน ต้องใส่ footer `Co-Authored-By` ตามโมเดลที่รันอยู่จริง ห้ามคัดลอกจากตัวอย่าง ถ้าไม่แน่ใจให้ถามก่อน
  - Claude: `Co-Authored-By: Claude <ชื่อ model ปัจจุบัน> <noreply@anthropic.com>`
  - agent อื่น: ใส่ชื่อ agent/model ของตัวเองตามจริง
  - ⚠️ **ห้าม hardcode ชื่อ version** ไว้ในไฟล์กฎ เพราะ model เปลี่ยนไปเรื่อย ๆ
- agent commit / push เฉพาะเมื่อ user สั่ง และ stage **เฉพาะไฟล์ที่เกี่ยวกับงานนั้น** ห้าม `git add -A` / `git add .`
