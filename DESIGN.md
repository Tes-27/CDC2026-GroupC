# Design Language — CDC 2026 กลุ่ม C

เอกสารสรุป "ภาษาดีไซน์" ของ `index.html` เพื่อนำไปใช้ซ้ำกับเว็บอื่น (เช่น เว็บอธิบาย indicator แบบ visual) ให้หน้าตา/สีสัน/รูปทรงเป็นชุดเดียวกัน

> สไตล์โดยรวม: **พรีเมียม fintech** — สะอาด โปร่ง น่าเชื่อถือ โทน navy เข้ม + teal เป็น accent + gold เน้นจุดสำคัญ บนพื้นเทาอ่อน การ์ดขอบมน เงานุ่ม

---

## 1. สี (Color Palette)

| ตัวแปร | ค่า | ใช้ทำอะไร |
|--------|------|-----------|
| `--bg` | `#f4f6fb` | พื้นหลังหน้า (เทา-ฟ้าอ่อนมาก) |
| `--card` | `#ffffff` | พื้นการ์ด/กล่อง |
| `--ink` | `#0f1f3d` | ตัวอักษรหลัก (navy เกือบดำ) |
| `--ink-soft` | `#5b6781` | ตัวอักษรรอง/คำอธิบาย (เทา-น้ำเงิน) |
| `--line` | `#e6eaf2` | เส้นขอบ/เส้นคั่น (อ่อนมาก) |
| `--navy` | `#13294b` | สีหลักเข้ม — header, ปุ่มหลัก, หัวข้อ |
| `--navy-2` | `#1d3a66` | navy อ่อนกว่า — ไล่เฉด, hover |
| `--accent` | `#0ea5a4` | **teal** — สีเน้นหลัก (เส้น, ไฮไลต์, โฟกัส) |
| `--accent-soft` | `#e3f6f5` | teal อ่อน — พื้นหลัง chip/แท็ก |
| `--gold` | `#c79a3a` | **ทอง** — แบรนด์/เน้นพิเศษ ("มาแรง", badge) |
| `--skill` / `--skill-bg` | `#1d3a66` / `#eaf0fb` | แท็กกลุ่มน้ำเงิน (ตัว/พื้น) |
| `--int` / `--int-bg` | `#0e7f7e` / `#e3f6f5` | แท็กกลุ่มเขียว-teal (ตัว/พื้น) |

**หลักการใช้สี**
- พื้นเทาอ่อน (`--bg`) + การ์ดขาว = ความรู้สึกโปร่ง สะอาด
- navy = โครงสร้าง/ความหนักแน่น · teal = การกระทำ/มีชีวิต · gold = จุดที่อยากให้สะดุดตา (ใช้น้อย ๆ)
- ตัวอักษรใช้ 2 ระดับเท่านั้น: `--ink` (หลัก) กับ `--ink-soft` (รอง)
- ไล่เฉดเด่น ๆ: `linear-gradient(135deg, var(--navy), var(--navy-2))` (header) และ `linear-gradient(90deg, var(--navy-2), var(--accent))` (แถบกราฟ — navy→teal)

**สำหรับเว็บ indicator (แนะนำ mapping สี):**
- เส้นราคา/แกน = `--ink` หรือ `--navy`
- เส้น indicator หลัก / สัญญาณ = `--accent` (teal)
- ไฮไลต์จุดสำคัญ / โซนพิเศษ = `--gold`
- สัญญาณซื้อ-ขาย ถ้าต้องการแดง-เขียว ใช้ `#0e7f7e` (เขียว, = `--int`) กับ `#c0392b` (แดง, = สีปุ่มลบ) จะเข้าชุดกัน

---

## 2. ตัวอักษร (Typography)

- ฟอนต์: **IBM Plex Sans Thai** (รองรับไทยสวย อ่านง่ายบนมือถือ) โหลดจาก Google Fonts
  ```html
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&display=swap" rel="stylesheet" />
  ```
  ```css
  font-family:"IBM Plex Sans Thai", system-ui, sans-serif;
  ```
- น้ำหนัก: 400 (ปกติ) · 500 (เน้นเบา/ปุ่ม) · 600 (หัวข้อ/ชื่อ) · 700 (badge/ตัวเลขเด่น)
- `line-height: 1.5` (เนื้อหา), 1.2 (หัวข้อ)
- สเกลขนาดที่ใช้จริง: หัวข้อใหญ่ ~18–19px · ชื่อการ์ด 16.5px · เนื้อหา 14.5px · รอง/แท็ก 12.5–13.5px · เล็กสุด 11.5–12px
- `-webkit-font-smoothing:antialiased` เปิดไว้ให้ตัวอักษรคมขึ้น

---

## 3. รูปทรง & เงา (Shape & Elevation)

- **ขอบมน (border-radius)** — เป็นเอกลักษณ์หลัก:
  - การ์ด/กล่องใหญ่: `--r` = **16px**
  - ปุ่ม/อินพุต: **11–12px**
  - แท็ก: **8px** · chip (เม็ดกลม): **20px** (pill) · badge เล็ก: 6px
  - modal: **18px**
- **เงา** (นุ่ม ฟุ้งต่ำ ไม่ดำจัด):
  ```css
  --shadow: 0 1px 2px rgba(16,31,61,.04), 0 8px 24px rgba(16,31,61,.06);
  ```
  modal เงาเข้มกว่า: `0 20px 60px rgba(16,31,61,.3)`
- ขอบบาง 1px สี `--line` รอบการ์ด/อินพุต (ไม่ใช้เงาอย่างเดียว)
- เส้นคั่นภายใน: `1px dashed var(--line)` (เส้นประ) สำหรับแบ่งโซนในการ์ด

---

## 4. ระยะห่าง (Spacing)

- คอนเทนต์กว้างสุด: `max-width: 1080px` กลางจอ, padding ข้าง 16px
- ช่องไฟในการ์ด: padding 16–18px, gap ระหว่าง element 10–14px
- grid การ์ด: `repeat(auto-fill, minmax(300px, 1fr))` gap 14px (responsive อัตโนมัติ)
- ปุ่ม padding: `10px 20px` (หลัก), `10px 16px` (ghost)

---

## 5. คอมโพเนนต์ (Components) — ก๊อปไปใช้ได้

### Header (แถบหัว navy ไล่เฉด + เส้นทอง)
```css
header{ background:linear-gradient(135deg,var(--navy),var(--navy-2));
  color:#fff; padding:26px 0 18px; border-bottom:3px solid var(--gold); }
```

### Badge (ป้ายแบรนด์ทอง)
```css
.badge{ background:var(--gold); color:#1a1a1a; font-weight:700;
  border-radius:10px; padding:6px 12px; font-size:15px; letter-spacing:.5px; }
```

### การ์ด (Card)
```css
.card{ background:var(--card); border:1px solid var(--line); border-radius:var(--r);
  padding:16px; box-shadow:var(--shadow); display:flex; flex-direction:column; gap:11px; }
```

### Chip (เม็ดกลมเลือกได้ — toggle)
```css
.chip{ border:1px solid var(--line); background:#fff; color:var(--ink); cursor:pointer;
  border-radius:20px; padding:6px 13px; font-size:13.5px; transition:.12s; }
.chip:hover{ border-color:var(--accent); }
.chip.selected{ background:var(--navy); color:#fff; border-color:var(--navy); }  /* หรือ var(--int) สำหรับกลุ่มเขียว */
```

### Tag (ป้ายข้อมูลสองโทน)
```css
.tag{ font-size:12.5px; padding:4px 10px; border-radius:8px; font-weight:500; }
.tag.blue{ background:var(--skill-bg); color:var(--skill); }   /* น้ำเงิน */
.tag.teal{ background:var(--int-bg);   color:var(--int);   }   /* เขียว-teal */
```

### ปุ่ม (Buttons)
```css
.btn-primary{ background:var(--navy); color:#fff; border:0; border-radius:11px;
  padding:10px 20px; font-weight:600; font-size:14.5px; cursor:pointer; transition:.15s; }
.btn-primary:hover{ background:var(--navy-2); }
.btn-ghost{ background:#fff; color:var(--ink-soft); border:1px solid var(--line);
  border-radius:11px; padding:10px 16px; font-size:14px; cursor:pointer; }
.btn-danger{ background:#c0392b; color:#fff; border:0; border-radius:11px;
  padding:10px 20px; font-weight:600; }
```

### แถบสัดส่วน/กราฟ (Bar — navy→teal)
```css
.track{ background:#eef1f7; border-radius:8px; height:22px; overflow:hidden; }
.fill{ height:100%; border-radius:8px;
  background:linear-gradient(90deg,var(--navy-2),var(--accent)); transition:width .5s; }
```
> เหมาะมากกับเว็บ indicator — เอาไปทำแถบความแรง/ค่า oscillator ได้เลย

### Modal (กล่องป๊อปอัป)
```css
.modal-overlay{ position:fixed; inset:0; background:rgba(16,31,61,.45);
  display:flex; align-items:center; justify-content:center; backdrop-filter:blur(2px); }
.modal{ background:#fff; border-radius:18px; padding:24px; max-width:380px;
  box-shadow:0 20px 60px rgba(16,31,61,.3); animation:pop .15s ease; }
```

### Heatmap cell (โทน teal ไล่ความเข้มตามค่า)
```css
/* ความเข้มแปรตามค่า: alpha = 0.18 + 0.82 * (value/max) */
background: rgba(14,127,126, <alpha>);  color:#fff;
```
> ใช้ทำตารางความถี่/ความแรงของสัญญาณได้

---

## 6. การเคลื่อนไหว (Motion)

- transition ทั่วไป: **0.12–0.15s** (hover ปุ่ม/chip), แถบกราฟ 0.5s
- เข้าหน้า/แท็บ: fade ขึ้นเบา ๆ
  ```css
  @keyframes fade{ from{opacity:0; transform:translateY(6px)} to{opacity:1; transform:none} }   /* .25s ease */
  ```
- modal เด้ง:
  ```css
  @keyframes pop{ from{transform:scale(.94); opacity:0} to{transform:scale(1); opacity:1} }      /* .15s ease */
  ```
- หลักการ: เคลื่อนไหวสั้น นุ่ม ไม่เด้งแรง — เน้นความ "พรีเมียม สงบ"

---

## 7. บล็อกเริ่มต้น (ก๊อปวางหัวไฟล์เว็บใหม่ได้เลย)

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
  :root{
    --bg:#f4f6fb; --card:#ffffff; --ink:#0f1f3d; --ink-soft:#5b6781;
    --line:#e6eaf2; --navy:#13294b; --navy-2:#1d3a66;
    --accent:#0ea5a4; --accent-soft:#e3f6f5; --gold:#c79a3a;
    --skill:#1d3a66; --skill-bg:#eaf0fb; --int:#0e7f7e; --int-bg:#e3f6f5;
    --danger:#c0392b;
    --shadow:0 1px 2px rgba(16,31,61,.04),0 8px 24px rgba(16,31,61,.06);
    --r:16px;
  }
  *{box-sizing:border-box}
  html,body{margin:0}
  body{ font-family:"IBM Plex Sans Thai",system-ui,sans-serif;
    background:var(--bg); color:var(--ink); line-height:1.5; -webkit-font-smoothing:antialiased; }
  .wrap{ max-width:1080px; margin:0 auto; padding:0 16px 80px; }
</style>
```

---

## 8. เช็กลิสต์ให้เว็บใหม่ "เข้าชุด" กับเว็บนี้
- [ ] พื้น `--bg` เทาอ่อน + การ์ดขาวขอบมน 16px เงานุ่ม
- [ ] ฟอนต์ IBM Plex Sans Thai, ตัวอักษร 2 ระดับ (ink / ink-soft)
- [ ] navy เป็นโครง, teal เป็น accent, gold เน้นจุดเดียวที่อยากให้เด่น
- [ ] ปุ่มหลัก navy ขอบมน 11px, hover เป็น navy-2
- [ ] กราฟ/แถบใช้ไล่เฉด navy→teal
- [ ] เส้นขอบบาง `--line` + เส้นคั่นเป็นเส้นประ
- [ ] motion สั้น 0.12–0.25s นุ่ม ๆ
- [ ] mobile-first (grid auto-fill, max-width 1080px)

> 💡 เคล็ดสำหรับเว็บ indicator: ส่งไฟล์นี้ให้ Claude พร้อมบอกว่า "ใช้ design language ตาม DESIGN.md นี้" แล้วโฟกัสเนื้อหา indicator — สี/รูปทรงจะออกมาเป็นชุดเดียวกับเว็บกลุ่ม C อัตโนมัติ
