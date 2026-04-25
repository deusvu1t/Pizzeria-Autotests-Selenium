# Pizzeria Autotests Selenium

Pet-project for UI autotests of the Skillbox pizzeria website:
https://pizzeria.skillbox.cc/

The project is at an early stage and will be updated as the test suite grows.

## Tech Stack

- Python
- Pytest
- Selenium WebDriver
- WebDriver Manager
- Allure Pytest
- Pydantic Settings

## Project Structure

```text
.
├── core/                 # Configuration, driver factory, utilities
├── pages/                # Page Object classes and reusable page components
├── tests/                # Test scenarios and pytest fixtures
├── pytest.ini            # Pytest configuration
└── requirements.txt      # Project dependencies
```

## Current Status

- Basic Selenium driver factory is implemented.
- Local browser launch is supported for Chrome and Firefox.
- Remote launch through Selenoid is planned in the configuration.
- Pytest fixtures prepare a fresh browser instance for every test.
- The first smoke test opens Google as a temporary example.

## Installation

Clone the repository:

```bash
git clone https://github.com/deusvu1t/Pizzeria-Autotests-Selenium.git
cd Pizzeria-Autotests-Selenium
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

Run tests with the default settings:

```bash
pytest
```

Run tests in a specific browser:

```bash
pytest --browser chrome
pytest --browser firefox
```

Run tests in headless mode:

```bash
pytest --headless
```

Run tests with Selenoid:

```bash
pytest --run-mode selenoid
```

## Configuration

Default settings are stored in `core/config/settings.py`.

The project supports overriding settings with a `.env` file and pytest CLI options.

Main settings:

- `browser`: `chrome` or `firefox`
- `run_mode`: `local` or `selenoid`
- `headless`: browser headless mode
- `base_url`: tested website URL
- `selenoid_url`: remote WebDriver URL
- `timeout`: implicit wait timeout
- `page_load_timeout`: page load timeout

## Roadmap

- Replace the temporary smoke test with real pizzeria scenarios.
- Add Page Object methods for the main page, product page, and cart.
- Cover product search, add-to-cart flow, cart changes, and checkout.
- Add Allure reporting instructions.
- Add CI workflow for automated test runs.
