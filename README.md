# Pizzeria Autotests Selenium

Пет-проект с UI-автотестами для сайта пиццерии Skillbox:
https://pizzeria.skillbox.cc/

Проект находится на ранней стадии разработки и будет постепенно обновляться по мере добавления новых тестов, страниц и инфраструктуры.

## Стек

- Python
- Pytest
- Selenium WebDriver
- WebDriver Manager
- Allure Pytest

## Структура проекта

```text
.
├── src/                  # Исходный код тестового фреймворка
├── src/browser/          # Фабрика драйверов и browser options
├── src/pages/            # Page Object классы
├── src/pages/components/ # Переиспользуемые компоненты страниц
├── src/fixtures/         # Pytest-фикстуры
├── tests/                # Тестовые сценарии и pytest-фикстуры
├── docs/                 # Тест-кейсы и проектная документация
├── pytest.ini            # Конфигурация pytest
└── requirements.txt      # Зависимости проекта
```

## Текущее состояние

- Реализована базовая фабрика Selenium-драйвера.
- Поддержан локальный запуск браузеров Chrome и Firefox.
- Pytest-фикстуры подготавливают новый браузер для каждого теста.
- Добавлены базовые Page Object и Component Object классы.
- Подключены логи и Allure-отчёты.
- Добавлены UI-тесты главной страницы и слайдера с пиццами.
- Подготовлены тест-кейсы основного пользовательского флоу.

## Установка

Склонировать репозиторий:

```bash
git clone https://github.com/deusvu1t/Pizzeria-Autotests-Selenium.git
cd Pizzeria-Autotests-Selenium
```

Создать и активировать виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

## Запуск тестов

Запуск тестов с настройками по умолчанию:

```bash
pytest
```

Если `pytest` не доступен как отдельная команда, запустить через Python из виртуального окружения:

```bash
python -m pytest
```

Запуск в конкретном браузере:

```bash
pytest --browser chrome
pytest --browser firefox
```

Запуск в headless-режиме:

```bash
pytest --headless
```

После запуска тестов логи сохраняются в:

- `reports/logs/test_run.log`

Allure results сохраняются в:

- `reports/allure-results`

Открыть Allure-отчёт:

```bash
allure serve reports/allure-results
```

## Конфигурация

Настройки по умолчанию находятся в `src/config/settings.py`.

Проект использует простой dataclass `Settings` и поддерживает переопределение браузера и headless-режима через CLI-опции pytest.

Основные настройки:

- `browser`: `chrome` или `firefox`
- `headless`: запуск браузера в headless-режиме
- `base_url`: URL тестируемого сайта

## Roadmap

- Стабилизировать ожидания для анимаций слайдера.
- Расширить Page Object методы для страницы товара и корзины.
- Покрыть корзину, регистрацию, оформление заказа и основной end-to-end флоу.
- Закрепить версии зависимостей для воспроизводимых локальных и CI-запусков.

