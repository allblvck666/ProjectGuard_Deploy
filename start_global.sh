#!/bin/bash
echo "🚀 Запуск ProjectGuard (global доступ) ..."

# === Активируем виртуальное окружение ===
source venv/bin/activate

# === Запуск backend ===
echo "▶️  Запуск backend..."
cd backend
python3 -m uvicorn main:app --reload --port 8010 --app-dir .
cd ..

# === Запуск frontend ===
echo "▶️  Запуск frontend..."
cd frontend
npm run dev -- --port 5180 &
cd ..

# === Подключаем ngrok ===
echo "🌐 Подключаем ngrok для FRONTEND и BACKEND..."
ngrok start --all --config ~/.ngrok2/ngrok.yml &

echo ""
echo "✅ Всё запущено!"
echo "-----------------------------------------"
echo "Frontend: (автоматически появится ниже)"
echo "Backend:  (автоматически появится ниже)"
echo "-----------------------------------------"


