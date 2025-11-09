import sqlite3
import csv
from pathlib import Path
from datetime import datetime, timedelta

# Пути к файлам
DB_PATH = Path(__file__).resolve().parent / "data.sqlite3"
SKUS_PATH = Path(__file__).resolve().parent / "skus.csv"

# === Новый надёжный парсер CSV ===
def load_skus():
    """Парсим CSV в формате: Коллекция, Тип, Артикул"""
    items = []
    if not SKUS_PATH.exists():
        return items

    with open(SKUS_PATH, newline="", encoding="utf-8-sig") as f:
        try:
            reader = csv.DictReader(f)
            for row in reader:
                sku = (row.get("Артикулы") or "").strip()
                if not sku:
                    continue
                collection = (row.get("Коллекция") or "").strip()
                type_ = (row.get("Тип (клей/замок)") or "").strip().lower()
                if type_ not in ("клей", "замок"):
                    continue
                items.append({
                    "sku": sku,
                    "collection": collection,
                    "type": type_
                })
            if items:
                return items
        except Exception:
            pass

        f.seek(0)
        reader = list(csv.reader(f))
        if not reader:
            return items

        maxw = max(len(r) for r in reader)
        norm = []
        for r in reader:
            r = list(r)
            if len(r) < maxw:
                r.extend([""] * (maxw - len(r)))
            norm.append(r)

        collections = [c.strip() for c in norm[0]]
        raw_types = [t.strip() for t in norm[1]]

        def normalize_type(t: str) -> str:
            tl = t.lower()
            if "кле" in tl:
                return "клей"
            if "зам" in tl:
                return "замок"
            return t.strip()

        types = [normalize_type(t) for t in raw_types]

        seen = set()
        for row in norm[2:]:
            for col_idx, cell in enumerate(row):
                sku = cell.strip()
                if not sku:
                    continue
                coll = collections[col_idx].strip()
                tp = types[col_idx].strip()
                key = (sku, coll, tp)
                if key in seen:
                    continue
                seen.add(key)
                items.append({
                    "sku": sku,
                    "collection": coll,
                    "type": tp
                })

    items.sort(key=lambda x: (x["sku"], x["collection"] or "", x["type"] or ""))
    return items

# === Подключение и работа с базой ===
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # --- Protections ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS protections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manager TEXT NOT NULL,
            client TEXT,
            partner TEXT,
            partner_city TEXT,
            sku TEXT,
            area_m2 REAL,
            last4 TEXT,
            object_city TEXT,
            address TEXT,
            comment TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            closed_at TEXT
        )
    """)

    # --- Users ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE NOT NULL,
            tg_username TEXT,
            first_name TEXT,
            role TEXT DEFAULT 'manager',
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

def add_days(dt_iso: str, days: int) -> str:
    dt = datetime.fromisoformat(dt_iso.replace("Z", ""))
    return (dt + timedelta(days=days)).isoformat(timespec="seconds") + "Z"

