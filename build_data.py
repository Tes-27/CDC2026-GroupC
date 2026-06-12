#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
อ่าน CDC2026-GroupC.xlsx แล้วฝังข้อมูล snapshot ลงใน index.html
ระหว่างเครื่องหมาย /*DATA_START*/ ... /*DATA_END*/

วิธีใช้: เมื่อมีคนกรอกเพิ่ม ให้โหลด Google Sheet เป็น .xlsx ทับไฟล์เดิม แล้วรัน:
    python3 build_data.py

- ความเป็นส่วนตัว: ข้อเสนอแนะถูกแยกออกจากตัวบุคคล + สุ่มลำดับ ทำให้ไล่ย้อนกลับไปหาเจ้าของไม่ได้
"""
import json, random, re, sys, unicodedata
from pathlib import Path
import openpyxl

ROOT = Path(__file__).parent
XLSX = ROOT / "CDC2026-GroupC.xlsx"
HTML = ROOT / "index.html"

def clean(v):
    """รวมทุก whitespace (รวม \\n \\r \\t และ U+2028/U+2029) ให้เป็นช่องว่างเดียว
    สำคัญ: U+2028/U+2029 ถูกต้องใน JSON แต่ทำให้ JavaScript string literal เป็น SyntaxError
    str.split() (ไม่ระบุ sep) ตัดทุกอักขระ whitespace ตาม Unicode รวมสองตัวนี้ด้วย"""
    if v is None:
        return ""
    return " ".join(str(v).split()).strip()

def split_tags(v):
    if not v:
        return []
    return [clean(t) for t in str(v).split(",") if clean(t)]

def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb["สมาชิก"]
    rows = list(ws.iter_rows(values_only=True))[1:]  # ข้าม header

    members = []
    suggestions = []
    for r in rows:
        line = clean(r[1])
        name = clean(r[2])
        if not line and not name:
            continue  # แถวว่าง
        members.append({
            "line": line,
            "name": name,
            "days": split_tags(r[3]),
            "times": split_tags(r[4]),
            "skills": split_tags(r[5]),
            "interests": split_tags(r[6]),
            "about": clean(r[7]),
            "avatar": "",  # ใส่ URL รูปจริงเองได้ภายหลัง
        })
        sug = clean(r[8])
        if sug:
            suggestions.append(sug)

    # สุ่มลำดับข้อเสนอแนะ (seed คงที่ -> ผลเหมือนเดิมทุกครั้ง แต่ไล่กลับหาเจ้าของไม่ได้)
    random.seed(2026)
    random.shuffle(suggestions)

    data = {"members": members, "suggestions": suggestions, "count": len(members)}
    blob = json.dumps(data, ensure_ascii=False, indent=2)
    # กันเหนียว: escape อักขระคั่นบรรทัด U+2028/U+2029 ที่ json อาจปล่อยผ่านแต่ JS ไม่รับ
    blob = blob.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

    html = HTML.read_text(encoding="utf-8")
    new = re.sub(
        r"/\*DATA_START\*/.*?/\*DATA_END\*/",
        lambda _: "/*DATA_START*/" + blob + "/*DATA_END*/",
        html,
        flags=re.DOTALL,
    )
    HTML.write_text(new, encoding="utf-8")
    print(f"✓ ฝังข้อมูล {len(members)} คน, ข้อเสนอแนะ {len(suggestions)} ข้อ ลง index.html แล้ว")

if __name__ == "__main__":
    if not XLSX.exists():
        sys.exit(f"ไม่พบไฟล์ {XLSX}")
    main()
