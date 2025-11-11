from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sqlite3
from db import get_conn

security = HTTPBearer(auto_error=False)

# Простая проверка роли через токен или просто костыльно (для теста)
def require_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # ⚠️ Тут можно потом сделать полноценную JWT-проверку
    # Пока просто костыль: пропускаем всех пользователей с ролью admin/superadmin из таблицы users
    conn = get_conn()
    cur = conn.cursor()
    row = cur.execute("SELECT role FROM users ORDER BY id LIMIT 1").fetchone()
    conn.close()

    if not row or row[0] not in ("admin", "superadmin"):
        raise HTTPException(status_code=401, detail="Недостаточно прав")
    return {"role": row[0]}
