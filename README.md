# Профили

## Полезные ссылки

[▶ Запуск онлайн-школы на Тильде, Airtable, Collabza, Integromat — No-Code мастер-класс](https://youtu.be/rH6NMEt-LjM)

## Запуск локально

1. Установить [Python](https://www.python.org/downloads/)
2. Создать файл `'.env'` в корневой папке проекта со следующим содержимым
    ```
    AIRTABLE_API_KEY = 'замените на ваше значение'
    AIRTABLE_BASE_ID = 'замените на ваше значение'
    AIRTABLE_TABLE_NAME = 'замените на ваше значение'
    ```

### Windows

3. Запустить файл `start_win.ps1`

## Карточки участников

Данные участников хранятся в базе данных Airtable. Для работы скрипта генерации необходимо в переменных окружения указать

- `base_id` — идентификатор базы данных Airtable
- `table_name` — идентификатор таблицы в базе данных
- `api_key` — API ключ для доступа к базе данных из аккаунта Airtable

Для автоматической генерации нужно настроить Airtable делать запрос для запуска скрипта.

## Описание базы данных

- `zero_utc_timestamp` — временная метка по гринвичу без временной зоны

## Требования к безопасности

- Основные аккаунты на используемых сервисах не должны использоваться, напрямую разработчиками, а поддерживать "доступ для разработчиков" для своих личных аккаунтов и разграничение прав для них
- Ключи не должны быть доступны публично. Если их требует фронтенд нужно спрятать его за API бекенда.