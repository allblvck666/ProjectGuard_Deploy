#!/bin/bash
echo "🚀 Запуск ProjectGuard (global доступ) ..."

# === Активируем виртуальное окружение ===
if [ -d "venv" ]; then
  source venv/bin/activate
else
  echo "❌ venv не найден. Проверь путь."
  exit 1
fi

# === Останавливаем старые процессы ===
echo "🧹 Останавливаем старые процессы..."
pkill -f uvicorn
pkill -f node
pkill ngrok
sleep 1

# === Запуск backend ===
echo "▶️  Запуск backend..."
cd backend || exit
nohup uvicorn main:app --reload --port 8010 > ../backend.log 2>&1 &
cd ..

# === Запуск frontend ===
echo "▶️  Запуск frontend..."
cd frontend || exit
nohup npm run dev > ../frontend.log 2>&1 &
cd ..

# === Подключаем ngrok ===
echo "🌐 Подключаем ngrok для FRONTEND и BACKEND..."
nohup ngrok http 8010 > ngrok_backend.log 2>&1 &
nohup ngrok http 5173 > ngrok_frontend.log 2>&1 &

sleep 6

# === Дожидаемся запуска ngrok (иногда он стартует медленно) ===
echo "⏳ Ожидаем запуск ngrok туннелей..."
for i in {1..10}; do
  TUNNELS=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels | length')
  if [ "$TUNNELS" != "0" ]; then
    break
  fi
  sleep 2
done

# === Показываем активные туннели ===
echo ""
echo "🌍 Текущие публичные ссылки ngrok:"
curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[] | "• \(.config.addr) → \(.public_url)"'

# === Проверяем работу API ===
BACKEND_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[] | select(.config.addr=="http://localhost:8010") | .public_url')
if [ -n "$BACKEND_URL" ]; then
  STATUS=$(curl -s "$BACKEND_URL/api/ping" | jq -r '.ok')
  if [ "$STATUS" == "true" ]; then
    echo "✅ Backend API отвечает по: $BACKEND_URL/api/ping"
  else
    echo "⚠️  Backend запущен, но /api/ping не отвечает."
  fi
else
  echo "❌ Не удалось определить ссылку backend-а."
fi

echo ""
echo "✅ Всё запущено!"
echo "-----------------------------------------"
echo "Чтобы остановить всё, введи:"
echo "pkill -f uvicorn && pkill -f node && pkill ngrok"
echo "-----------------------------------------"

