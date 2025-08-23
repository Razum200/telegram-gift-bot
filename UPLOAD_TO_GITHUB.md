# 📤 Инструкция по загрузке в GitHub репозиторий

## ⚠️ ВАЖНО: НЕ ЗАГРУЖАЙТЕ ЛИЧНЫЕ ФАЙЛЫ!

### 🚫 НИКОГДА не загружайте эти файлы:
- ❌ `.env` - содержит ваши API ключи Telegram
- ❌ `budgets.json` - содержит ваши реальные бюджеты
- ❌ `finalV2.session` - содержит вашу сессию Telegram
- ❌ `finalV2.session-journal` - журнал сессии
- ❌ `purchase_log.txt` - содержит историю ваших покупок
- ❌ `seen_gifts.json` - содержит просмотренные подарки

---

## ✅ Файлы для загрузки в репозиторий:

### 📚 Основные файлы:
```
✅ monitor_multi_advanced.py          # Основной скрипт бота
✅ monitor_multi_advanced_backup.py   # Резервная версия
✅ config.py                          # Настройки бота
✅ helpers.py                         # Вспомогательные функции
✅ requirements.txt                   # Список зависимостей
✅ .gitignore                         # Исключения для Git
✅ start_bot.bat                      # Скрипт запуска Windows
✅ start_bot.sh                       # Скрипт запуска macOS
```

### 📖 Документация:
```
✅ README.md                          # Подробная инструкция
✅ FAQ.md                             # Часто задаваемые вопросы
✅ SETUP_TELEGRAM_API.md              # Настройка API ключей
✅ CREATE_REPO_GUIDE.md               # Создание репозитория
✅ BUDGET_GUIDE.md                    # Руководство по бюджетам
✅ GIFT_ANALYSIS.md                   # Анализ подарков
```

### 📊 Примеры (ВМЕСТО реальных файлов):
```
✅ budgets.example.json               # Примеры бюджетов
✅ budgets_unlim.example.json         # Примеры безлимитных
✅ budgets.simple.json                # Простой пример
✅ env.example                        # Пример настроек
```

---

## 🚀 Способы загрузки в репозиторий:

### Способ 1: Через GitHub Desktop (самый простой)

1. **Скачайте GitHub Desktop**: https://desktop.github.com
2. **Установите и войдите** в аккаунт
3. **Добавьте репозиторий**:
   - File → Add local repository
   - Выберите папку с проектом
   - Выберите ваш репозиторий https://github.com/Razum200/telegram-gift-bot.git
4. **Выберите файлы для загрузки**:
   - Отметьте ✅ все файлы из списка выше
   - НЕ отмечайте ❌ личные файлы
5. **Нажмите "Commit to main"**
6. **Нажмите "Push origin"**

### Способ 2: Через командную строку

```bash
# Перейдите в папку с проектом
cd /путь/к/папке/telegram-gift-bot

# Инициализируйте git (если не делали)
git init

# Добавьте репозиторий
git remote add origin https://github.com/Razum200/telegram-gift-bot.git

# Добавьте нужные файлы
git add monitor_multi_advanced.py
git add monitor_multi_advanced_backup.py
git add config.py
git add helpers.py
git add requirements.txt
git add .gitignore
git add start_bot.bat
git add start_bot.sh
git add README.md
git add FAQ.md
git add SETUP_TELEGRAM_API.md
git add CREATE_REPO_GUIDE.md
git add BUDGET_GUIDE.md
git add GIFT_ANALYSIS.md
git add budgets.example.json
git add budgets_unlim.example.json
git add budgets.simple.json
git add env.example

# Проверьте, что добавлено
git status

# Создайте коммит
git commit -m "Initial commit: Telegram Gift Bot with examples"

# Загрузите в репозиторий
git push -u origin main
```

### Способ 3: Через GitHub Web интерфейс

1. **Зайдите в репозиторий**: https://github.com/Razum200/telegram-gift-bot.git
2. **Нажмите "Add file"** → **"Upload files"**
3. **Перетащите файлы** из списка выше
4. **Нажмите "Commit changes"**

---

## 🔍 Проверка загруженных файлов:

После загрузки проверьте в репозитории:

### ✅ Должны быть загружены:
- [ ] monitor_multi_advanced.py
- [ ] README.md (с подробной инструкцией)
- [ ] budgets.example.json (примеры бюджетов)
- [ ] env.example (пример настроек)
- [ ] Все остальные файлы из списка выше

### ❌ НЕ должны быть загружены:
- [ ] .env (личные API ключи)
- [ ] budgets.json (реальные бюджеты)
- [ ] finalV2.session (сессия Telegram)
- [ ] purchase_log.txt (история покупок)
- [ ] Любые другие личные файлы

---

## 📝 Добавление новых файлов:

### Если хотите добавить файл:
```bash
git add новый_файл.txt
git commit -m "Добавлен новый файл"
git push
```

### Если хотите обновить существующий файл:
```bash
git add README.md
git commit -m "Обновлена инструкция"
git push
```

---

## 🛡️ Защита личных данных:

### В .gitignore уже добавлены:
```
.env
*.session
*.session-journal
budgets.json
budgets_unlim.json
purchase_log.txt
seen_gifts.json
```

### Дополнительная безопасность:
1. **Никогда не коммитьте** файлы с ключами
2. **Проверяйте перед push** командой `git status`
3. **Используйте .gitignore** для автоматического исключения

---

## 🎯 Итог:

После загрузки ваш репозиторий будет содержать:
- ✅ Полную документацию для пользователей
- ✅ Примеры всех настроек
- ✅ Готовые скрипты запуска
- ✅ Подробные инструкции
- ❌ Никаких личных данных

**Теперь любой человек сможет скачать ваш репозиторий и запустить бота за 10-15 минут!** 🚀

**Проверьте, что все файлы загружены правильно и нет личных данных!** 🔒
