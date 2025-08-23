#!/bin/bash

echo "====================================="
echo "   🎁 Telegram Gift Bot - Запуск"
echo "====================================="
echo

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден!"
    echo "📥 Установите Python3:"
    echo "   macOS: brew install python"
    echo "   Ubuntu: sudo apt install python3-pip"
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

# Проверка зависимостей
echo "🔍 Проверка зависимостей..."
python3 -c "import telethon" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Установка зависимостей..."
    pip3 install -r requirements.txt
fi

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден!"
    echo "📋 Скопируйте env.example в .env:"
    echo "   cp env.example .env"
    echo "   И заполните API ключи"
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

# Проверка бюджетов
if [ ! -f "budgets.json" ]; then
    echo "⚠️  Файл budgets.json не найден!"
    echo "📋 Скопируйте budgets.example.json в budgets.json:"
    echo "   cp budgets.example.json budgets.json"
    echo "   И настройте свои каналы"
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

echo "✅ Все проверки пройдены!"
echo "🚀 Запуск бота..."
echo

python3 monitor_multi_advanced.py

echo
echo "🛑 Бот остановлен"
read -p "Нажмите Enter для выхода..."
