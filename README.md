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
- Pydantic Settings

## Структура проекта

```text
.
├── core/                 # Конфигурация, фабрика драйверов, утилиты
├── pages/                # Page Object классы и переиспользуемые компоненты страниц
├── tests/                # Тестовые сценарии и pytest-фикстуры
├── pytest.ini            # Конфигурация pytest
└── requirements.txt      # Зависимости проекта
```

## Текущее состояние

- Реализована базовая фабрика Selenium-драйвера.
- Поддержан локальный запуск браузеров Chrome и Firefox.
- В конфигурации заложена возможность запуска через Selenoid.
- Pytest-фикстуры подготавливают новый браузер для каждого теста.
- Первый smoke-тест пока открывает Google как временный пример.

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

Запуск в конкретном браузере:

```bash
pytest --browser chrome
pytest --browser firefox
```

Запуск в headless-режиме:

```bash
pytest --headless
```

Запуск через Selenoid:

```bash
pytest --run-mode selenoid
```

## Конфигурация

Настройки по умолчанию находятся в `core/config/settings.py`.

Проект поддерживает переопределение настроек через `.env` файл и CLI-опции pytest.

Основные настройки:

- `browser`: `chrome` или `firefox`
- `run_mode`: `local` или `selenoid`
- `headless`: запуск браузера в headless-режиме
- `base_url`: URL тестируемого сайта
- `selenoid_url`: URL удалённого WebDriver
- `timeout`: implicit wait
- `page_load_timeout`: таймаут загрузки страницы

## Roadmap

- Заменить временный smoke-тест на реальные сценарии сайта пиццерии.
- Добавить Page Object методы для главной страницы, страницы товара и корзины.
- Покрыть поиск товара, добавление в корзину, изменение корзины и оформление заказа.
- Добавить инструкцию по Allure-отчётам.
- Добавить CI workflow для автоматического запуска тестов.

