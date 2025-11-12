// frontend/src/TelegramLoginButton.jsx
export default function TelegramLoginButton() {
    const BACKEND_URL = "https://projectguard-backend.onrender.com";
  
    const handleLogin = async () => {
      const payload = {
        id: 426188469,
        username: "messiah_66",
        first_name: "Messiah",
      };
  
      try {
        const res = await fetch(`${BACKEND_URL}/api/users/auth/telegram`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
  
        const data = await res.json();
        console.log("✅ AUTH RESPONSE:", data);
  
        if (!data.ok || !data.token) {
          alert("Ошибка авторизации на сервере");
          return;
        }
  
        localStorage.setItem("jwt_token", data.token);
        localStorage.setItem("role", data.user?.role || "manager");
        alert(`Добро пожаловать, ${data.user?.username || "пользователь"}!`);
        window.location.reload(); // Перезагружаем, чтобы App.jsx подхватил токен
      } catch (err) {
        console.error(err);
        alert("Ошибка при авторизации");
      }
    };
  
    return (
      <div
        onClick={handleLogin}
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          background: "#229ED9",
          color: "white",
          padding: "10px 16px",
          borderRadius: 12,
          fontSize: 16,
          fontWeight: 600,
          cursor: "pointer",
          width: "fit-content",
          margin: "0 auto",
        }}
      >
        <img
          src="https://telegram.org/img/t_logo.svg"
          alt="Telegram"
          style={{ width: 24, height: 24 }}
        />
        Войти как 😌
      </div>
    );
  }
  