// frontend/src/LoginPage.jsx
import { useState } from "react";
import { api } from "./api";

export default function LoginPage({ onLogin }) {
  const [tgId, setTgId] = useState("");
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setErr("");
    if (!tgId) {
      setErr("Введите Telegram ID (числом)");
      return;
    }

    // бекенд ждёт вот такой json: { id, username, first_name, ... }
    const payload = {
      id: Number(tgId),
      username: username || "",
      first_name: firstName || "",
      // hash он у тебя проверяет, но мы сейчас локально — поэтому уберём
      // а в бекенде verify_telegram_auth можно временно ослабить
    };

    try {
      setLoading(true);
      const res = await api.post("/api/auth/telegram", payload);
      const { token, role } = res.data;
      localStorage.setItem("jwt_token", token);
      localStorage.setItem("role", role);
      if (onLogin) onLogin(role);
      else window.location.href = "/";
    } catch (e) {
      console.error(e);
      setErr(e.response?.data?.detail || "Ошибка авторизации");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: 420, marginTop: 40 }}>
      <h2>Вход</h2>
      <p className="small" style={{ opacity: 0.7 }}>
        Пока что ручной вход. Потом можно прикрутить настоящую Telegram-auth.
      </p>
      <form onSubmit={submit} className="card" style={{ gap: 8, display: "flex", flexDirection: "column" }}>
        <label>
          Telegram ID
          <input
            className="input"
            value={tgId}
            onChange={(e) => setTgId(e.target.value)}
            placeholder="426188469"
          />
        </label>
        <label>
          Username
          <input
            className="input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="@username"
          />
        </label>
        <label>
          Имя
          <input
            className="input"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            placeholder="Дмитрий"
          />
        </label>
        {err && <div style={{ color: "tomato" }}>{err}</div>}
        <button className="btn" type="submit" disabled={loading}>
          {loading ? "Входим..." : "Войти"}
        </button>
      </form>
    </div>
  );
}

