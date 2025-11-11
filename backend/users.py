import sqlite3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from db import get_conn, now_iso

router = APIRouter(prefix="/api/users", tags=["users"])


# === Модели ===
class UserCreate(BaseModel):
    tg_id: int
    tg_username: str = ""
    first_name: str = ""
    role: str = "manager"  # manager | assistant | admin


class LinkAssistant(BaseModel):
    manager_id: int
    assistant_id: int


# === Инициализация таблицы ===
def init_users_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE,
            tg_username TEXT,
            first_name TEXT,
            role TEXT,
            manager_id INTEGER,
            group_tag TEXT,
            region TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()



# === Добавить пользователя ===
@router.post("/")
def add_user(data: UserCreate):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO users (tg_id, tg_username, first_name, role, created_at) VALUES (?,?,?,?,?)",
        (data.tg_id, data.tg_username, data.first_name, data.role, now_iso()),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


# === Список пользователей ===
@router.get("/")
def list_users():
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return {"ok": True, "users": [dict(r) for r in rows]}


# === Привязать помощника к менеджеру ===
@router.post("/link-assistant")
def link_assistant(data: LinkAssistant):
    conn = get_conn()
    cur = conn.cursor()
    # Проверяем, что оба пользователя есть
    mgr = cur.execute("SELECT * FROM users WHERE id=?", (data.manager_id,)).fetchone()
    asst = cur.execute("SELECT * FROM users WHERE id=?", (data.assistant_id,)).fetchone()

    if not mgr or not asst:
        conn.close()
        raise HTTPException(status_code=404, detail="Manager or Assistant not found")

    cur.execute("UPDATE users SET manager_id=? WHERE id=?", (data.manager_id, data.assistant_id))
    conn.commit()
    conn.close()
    return {"ok": True, "msg": "Assistant linked to manager"}


# === Получить помощников по менеджеру ===
@router.get("/assistants/{manager_id}")
def get_assistants(manager_id: int):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM users WHERE manager_id=?", (manager_id,)).fetchall()
    conn.close()
    return {"ok": True, "assistants": [dict(r) for r in rows]}
from fastapi import Depends
from backend.auth import require_admin  # ⚠️ если функция require_admin в main.py — оставь так

# === Обновить пользователя (роль, группа, менеджер, регион) ===
@router.patch("/{user_id}")
def update_user(user_id: int, data: dict, user=Depends(require_admin)):
    conn = get_conn()
    cur = conn.cursor()

    exists = cur.execute("SELECT id FROM users WHERE id=?", (user_id,)).fetchone()
    if not exists:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    cur.execute(
        """
        UPDATE users
        SET role = COALESCE(:role, role),
            group_tag = COALESCE(:group_tag, group_tag),
            manager_id = COALESCE(:manager_id, manager_id),
            region = COALESCE(:region, region)
        WHERE id = :user_id
        """,
        {**data, "user_id": user_id},
    )
    conn.commit()
    conn.close()
    return {"ok": True, "message": "✅ Пользователь обновлён"}


# === Удалить пользователя ===
@router.delete("/{user_id}")
def delete_user(user_id: int, user=Depends(require_admin)):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return {"ok": True, "message": "🗑 Пользователь удалён"}


# === Защитить список пользователей (только для админов) ===
@router.get("/", include_in_schema=False)
def list_users_admin(user=Depends(require_admin)):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return {"ok": True, "users": [dict(r) for r in rows]}

# === Telegram WebApp Авторизация ===
from jose import jwt
from datetime import timedelta

SECRET_KEY = "supersecretkey"  # потом можно вынести в .env
ALGORITHM = "HS256"

@router.post("/auth/telegram")
def auth_telegram(user: dict):
    """
    Принимает объект user от Telegram WebApp
    Возвращает JWT токен
    """
    tg_id = user.get("id")
    username = user.get("username", "")
    first_name = user.get("first_name", "")

    if not tg_id:
        raise HTTPException(status_code=400, detail="Missing Telegram user ID")

    # 1️⃣ Создаём или обновляем пользователя в БД
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO users (tg_id, tg_username, first_name, role, created_at) VALUES (?,?,?,?,?)",
        (tg_id, username, first_name, "manager", now_iso()),
    )
    conn.commit()
    conn.close()

    # 2️⃣ Генерируем JWT токен
    payload = {
        "sub": str(tg_id),
        "role": "manager",
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"ok": True, "token": token, "user": {"tg_id": tg_id, "username": username}}
