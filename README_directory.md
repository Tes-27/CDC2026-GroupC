# ทำเนียบสมาชิก CDC 2026 — กลุ่ม C

เว็บหน้าเดียว self-contained สำหรับให้เพื่อนในกลุ่มทำความรู้จักกัน + ดูสรุปเวลานัด + อ่านข้อเสนอแนะ
ไม่มี login ไม่มี backend — ข้อมูลฝัง snapshot อยู่ในไฟล์ `index.html` โดยตรง เปิดจากเบราว์เซอร์หรือ GitHub Pages ได้เลย

## ไฟล์
- `index.html` — ตัวเว็บ (3 แท็บ: สมาชิก / นัดเวลา / ข้อเสนอแนะ) **— push ไฟล์นี้ขึ้น GitHub Pages พอ**
- `build_data.py` — สคริปต์อ่าน `CDC2026-GroupC.xlsx` แล้วฝังข้อมูลลง `index.html`
- `CDC2026-GroupC.xlsx` — ข้อมูลดิบจากฟอร์ม (ไม่ต้อง push ก็ได้)

## 3 แท็บ
1. **สมาชิก** — การ์ดแนะนำตัวทุกคน (avatar การ์ตูน + ความรู้ + ความสนใจ + วัน/เวลา) ค้นหา + กรองได้
   (กรองในกลุ่มเดียว = "หรือ", ต่างกลุ่ม = "และ")
2. **กระดานสนทนา** — โพสต์/ไลก์/คอมเมนต์ สไตล์ Facebook ไม่มี login (เลือก "คุณคือใคร" จากรายชื่อสมาชิก) + **แนบรูป** + **แก้ไข/ลบโพสต์ของตัวเอง** (ลบมี modal ยืนยัน)
3. **คลังความรู้** — ใครก็เขียนบทความได้ มีหัวข้อ/**แนบรูปได้หลายรูป** + **เลือกแท็กจาก chip** (อ้างอิงความรู้ของสมาชิก + TradingView) หรือ **เพิ่มแท็กเอง** + อ่านต่อ-ย่อ + **ค้นหา/กรองแท็ก** + **แก้ไข/ลบบทความของตัวเอง**

> รูปภาพ: ย่อในเครื่อง (กว้างสุด ~1200px) แล้วเก็บฝังลง Firestore โดยตรง — ไม่ต้องเปิด Firebase Storage/ผูกบัตร ใช้ได้บน Spark ฟรี เหมาะกับภาพประกอบทั่วไป ถ้าอนาคตอยากลงรูปเยอะ/ใหญ่มากค่อยย้ายไป Storage
4. **นัดเวลา** — **เพิ่มการนัดใหม่ + โหวตวัน-เวลา** (เลือกได้หลายช่อง, แสดงผลโหวต+ช่องมาแรง, ลบนัดของตัวเอง) ต่อด้วยสรุปภาพรวมวัน/เวลาจากแบบฟอร์ม + heatmap
5. **ข้อเสนอแนะ** — สรุปประเด็นเด่น + ข้อเสนอแนะดิบทุกข้อ **แบบไม่ระบุตัวผู้เขียน + สุ่มลำดับ**

## ⚠️ ที่เก็บข้อมูลของ กระดานสนทนา + คลังความรู้
2 แท็บนี้รองรับ 2 โหมด สลับด้วยตัวแปร `window.FIREBASE_CONFIG` บนสุดของ `<script>` ใน `index.html`:
- **`null` (ค่าเริ่มต้นตอนนี้)** → เก็บใน **localStorage** = ในเครื่องตัวเองเท่านั้น **ไม่แชร์ข้ามเครื่อง** (เหมาะแค่ลองใช้)
- **ใส่ config** → ใช้ **Firebase Firestore** = แชร์จริง realtime ทุกคนเห็นโพสต์เด้งทันที

> สมาชิก/นัดเวลา/ข้อเสนอแนะ ไม่เกี่ยวกับส่วนนี้ — ยังเป็น snapshot ฝังในไฟล์ตามเดิม

## ตั้ง Firebase ให้ 2 แท็บแชร์ข้ามเครื่อง (realtime)
ทำครั้งเดียว ฟรี (Spark plan พอเหลือเฟือสำหรับ ~26 คน):

**1. สร้างโปรเจกต์**
- ไป https://console.firebase.google.com → Add project → ตั้งชื่อ (เช่น `cdc-group-c`) → ปิด Google Analytics ได้ → Create

**2. เปิด Firestore Database**
- เมนูซ้าย Build → Firestore Database → Create database → เลือก location (เช่น `asia-southeast1`) → เริ่มแบบ Production mode

**3. วางกฎความปลอดภัย** (แท็บ Rules ใน Firestore → วางทับ → Publish)
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /posts/{id}    { allow read, create, update, delete: if true; }
    match /articles/{id} { allow read, create, update, delete: if true; }
    match /meetups/{id}  { allow read, create, update, delete: if true; }
  }
}
```
> กฎนี้ให้ทุกคน "อ่าน + เพิ่ม + ไลก์/คอมเมนต์ + ลบ" ได้
> หน้าเว็บโชว์ปุ่มลบเฉพาะของตัวเอง (เช็คจากชื่อที่เลือก) — แต่เพราะไม่มี login จริง ระบบเป็นแบบ "ให้เกียรติกัน" (honor system) เหมือนการโพสต์ในนามคนอื่นก็ทำได้
> เหมาะกับกลุ่มปิด+ลิงก์ไม่เปิดเผย ถ้าต้องการแน่นกว่านี้ค่อยเพิ่ม passcode/App Check ทีหลัง

**4. เอา config มาใส่**
- Project settings (เฟือง) → ส่วน "Your apps" → กดไอคอน `</>` (Web) → ตั้งชื่อ app → จะได้ออบเจ็กต์ `firebaseConfig`
- เปิด `index.html` หาบรรทัด `window.FIREBASE_CONFIG = null;` แล้วแทนด้วย:
```js
window.FIREBASE_CONFIG = {
  apiKey:"AIza...", authDomain:"cdc-group-c.firebaseapp.com", projectId:"cdc-group-c",
  storageBucket:"cdc-group-c.appspot.com", messagingSenderId:"123...", appId:"1:123...:web:abc..."
};
```
> ค่าพวกนี้ไม่ใช่ความลับ — Firebase ออกแบบให้อยู่ในโค้ดฝั่งเว็บได้ ความปลอดภัยอยู่ที่ "กฎ" ในข้อ 3

**5. push `index.html` ขึ้น GitHub** → เสร็จ ทุกคนเห็นโพสต์/บทความเดียวกันแบบ realtime

โครงสร้างข้อมูลใน Firestore (สร้างอัตโนมัติเมื่อมีคนโพสต์):
- `posts/{id}` : `{ author, text, ts, likes:[], comments:[{author,text,ts}] }`
- `articles/{id}` : `{ author, title, body, tags:[], ts }`

## อัปเดตข้อมูลเมื่อมีคนกรอกเพิ่ม
1. โหลด Google Sheet เป็น `.xlsx` มาทับไฟล์ `CDC2026-GroupC.xlsx`
2. รัน:
   ```bash
   python3 build_data.py
   ```
3. commit + push `index.html`

## รูปโปรไฟล์
ค่าเริ่มต้นเป็น **emoji สัตว์น่ารัก** สุ่มแบบคงที่จากชื่อ (คนเดิมได้สัตว์+สีพื้นหลังเดิมเสมอ) วาดในไฟล์เลย ไม่พึ่ง CDN
อยากเปลี่ยนชุดสัตว์/สี แก้ตัวแปร `ANIMALS` ใน `index.html` ได้

ใส่รูปจริงแทน (ออปชั่น): แต่ละสมาชิกมีฟิลด์ `"avatar": ""` ใน data ของ `index.html` — ใส่ URL รูปลงไปจะแสดงรูปนั้นแทน emoji
(ถ้าจะให้คงค่าเวลารัน `build_data.py` ใหม่ ต้องเพิ่ม logic เก็บ avatar เดิม — ปัจจุบัน build จะรีเซ็ตเป็นค่าว่าง)

## ความเป็นส่วนตัว
- ใส่ `<meta name="robots" content="noindex,nofollow">` กัน Google เก็บ index แล้ว
- การ์ดสมาชิก **ไม่แสดงคอลัมน์ข้อเสนอแนะ** และข้อเสนอแนะถูกตัดขาดจากตัวบุคคล (สุ่มลำดับ) ในขั้น build
