// frontend/src/TelegramLoginButton.jsx
export default function TelegramLoginButton() {
    const BOT_NAME = "ProjectGuardBot"; // твой username бота без @
    const BACKEND_URL = "https://projectguard-deploy.onrender.com"; // твой Render backend
  
    const handleLogin = () => {
      const url = `https://t.me/${BOT_NAME}?start=login`;
      window.Telegram?.LoginWidget
        ? window.Telegram.LoginWidget.init({ bot_id: BOT_NAME })
        : (window.location.href = `${BACKEND_URL}/api/auth/telegram`);
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
  