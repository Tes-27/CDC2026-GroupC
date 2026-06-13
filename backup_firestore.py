#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ดึงข้อมูลทั้งหมดจาก Firestore (posts / articles / meetups) มาเซฟเป็นไฟล์ JSON สำรอง

วิธีใช้:
    python3 backup_firestore.py

- อ่าน apiKey / projectId จาก index.html อัตโนมัติ (ไม่ต้องกรอกเอง)
- ใช้ Firestore REST API + กฎที่เปิดให้อ่าน (allow read) จึงไม่ต้องล็อกอิน
- ได้ไฟล์ชื่อ backup-firestore-YYYYMMDD-HHMM.json ในโฟลเดอร์นี้
- รันบ่อยแค่ไหนก็ได้ แต่ละครั้งได้ไฟล์ใหม่ (ไม่ทับของเก่า)
"""
import json, re, sys, urllib.request, datetime
from pathlib import Path

ROOT = Path(__file__).parent
HTML = ROOT / "index.html"
COLLECTIONS = ["posts", "articles", "meetups"]

def read_config():
    """ดึง apiKey + projectId จากบล็อก window.FIREBASE_CONFIG ใน index.html"""
    txt = HTML.read_text(encoding="utf-8")
    # ดึงค่าจริง โดยข้าม placeholder ในคอมเมนต์ตัวอย่าง (apiKey มี "...", projectId เป็น "xxx")
    apis = [a for a in re.findall(r'apiKey\s*:\s*"([^"]+)"', txt) if "..." not in a]
    projs = [p for p in re.findall(r'projectId\s*:\s*"([^"]+)"', txt) if p != "xxx"]
    if not apis or not projs:
        sys.exit("อ่าน apiKey/projectId จริงไม่ได้ (เจอแต่ค่าตัวอย่าง)")
    return apis[0], projs[0]

def conv(v):
    """แปลงค่ารูปแบบ Firestore REST -> ค่า Python ปกติ"""
    if "stringValue" in v:    return v["stringValue"]
    if "integerValue" in v:   return int(v["integerValue"])
    if "doubleValue" in v:    return v["doubleValue"]
    if "booleanValue" in v:   return v["booleanValue"]
    if "timestampValue" in v: return v["timestampValue"]
    if "nullValue" in v:      return None
    if "arrayValue" in v:     return [conv(x) for x in v["arrayValue"].get("values", [])]
    if "mapValue" in v:       return {k: conv(val) for k, val in v["mapValue"].get("fields", {}).items()}
    return v  # เผื่อชนิดอื่น

def fetch(collection, project, key):
    """ดึงทุก document ในคอลเลกชัน (รองรับหลายหน้าด้วย pageToken)"""
    docs, token = [], None
    while True:
        url = (f"https://firestore.googleapis.com/v1/projects/{project}"
               f"/databases/(default)/documents/{collection}?key={key}&pageSize=300")
        if token:
            url += f"&pageToken={token}"
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read().decode("utf-8"))
        for d in data.get("documents", []):
            row = {"id": d["name"].split("/")[-1]}
            row.update({k: conv(v) for k, v in d.get("fields", {}).items()})
            docs.append(row)
        token = data.get("nextPageToken")
        if not token:
            break
    return docs

def main():
    key, project = read_config()
    print(f"กำลัง backup จากโปรเจกต์: {project}")
    out = {"project": project, "collections": {}}
    for c in COLLECTIONS:
        rows = fetch(c, project, key)
        out["collections"][c] = rows
        print(f"  {c}: {len(rows)} รายการ")
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    fn = ROOT / f"backup-firestore-{stamp}.json"
    fn.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ เซฟแล้ว: {fn.name}")

if __name__ == "__main__":
    main()
