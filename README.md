# Test IT integration

UI-автотесты для платформы **dvjob.kz** на стеке `pytest + Playwright + Allure + testit-adapter-pytest`.
Проект реализует паттерн Page Object, ведёт красивые Allure-отчёты и автоматически
загружает результаты в систему управления тестами **Test IT**.

## Getting started

Чтобы быстро развернуть проект локально, выполните шаги ниже.

### Требования

- Python **>= 3.12**
- [uv](https://docs.astral.sh/uv/)
- Playwright-браузеры (Chromium)

### Установка

```bash
# 1. Клонируем репозиторий
cd existing_repo
git remote add origin https://gitlab.com/ppstanislav/test_it_integration.git
git branch -M main
git push -uf origin main

# 2. Устанавливаем зависимости
uv sync

# 3. Ставим браузеры Playwright
uv run playwright install chromium
```

### Переменные окружения

Перед запуском тестов создайте файл `.env` (по образцу `.env.example`) со
следующими переменными:

```dotenv
# Учётные данные тестовых пользователей
CandidateLogin=...
CandidatePassword=...
EmployerLogin=...
EmployerPassword=...
```

> Файл `.env` и `connection_config.ini` с приватным токеном Test IT добавлены в
> `.gitignore` — не коммитьте их.

## Структура проекта

```
test_it_integration-main/
├── conftest.py                  # фикстуры pytest, метаданные Allure, скриншоты при падении
├── pyproject.toml                # зависимости, маркеры pytest, опции запуска
├── uv.lock                       # зафиксированные версии зависимостей
├── pages/                        # Page Object'ы
│   ├── base_page.py              # родительский класс страницы
│   ├── home_page.py              # главная страница dvjob.kz
│   ├── auth_page.py              # страница авторизации
│   ├── footer_page.py            # футер
│   └── server_validation_page.py # серверная валидация формы логина
├── tests/                        # автотесты
│   ├── test_auth.py              # авторизация соискателя и работодателя
│   ├── test_main_page.py         # главная страница: заголовок, лого, поиск, языки
│   ├── test_upper_menu.py        # верхние меню «Соискателю» / «Работодателю»
│   ├── test_footer.py            # футер: ссылки, контакты, соцсети
│   ├── tests_server_validation.py# серверная валидация поля username
│   └── test_example.py           # пример теста с маркером testit
└── src/
    ├── main.py
    └── testit_project/
```

## Usage

### Запуск всех тестов

```bash
uv run pytest
```

В `pyproject.toml` уже заданы опции по умолчанию:

```
addopts = "-v --alluredir=allure-results --screenshot=only-on-failure --video=retain-on-failure --output=test-results"
```

### Запуск с выгрузкой в Test IT

```bash
TESTIT_URL=https://team-x4ov.testit.software \
TESTIT_PRIVATE_TOKEN=<your_private_token> \
TESTIT_PROJECT_ID=01a14f77-4896-7bee-9481-74c42030828b \
TESTIT_CONFIGURATION_ID=2 \
uv run pytest -s
```

### Запуск подмножества тестов

```bash
# Только тесты авторизации
uv run pytest tests/test_auth.py

# Только тесты с маркером testit
uv run pytest -m testit

# Один конкретный кейс по external_id
uv run pytest -k "test_auth_valid_candidate"
```

### Просмотр Allure-отчёта

```bash
uv run allure serve allure-results
```

В отчёт автоматически подкладываются:

- `environment.properties` — окружение (URL, браузер, стенд, ОС, версия Python);
- `executor.json` — информация о сборке (растёт счётчик в `.build_order`);
- `categories.json` — категории дефектов: «Баги продукта», «Проблемы теста или
  окружения», «Известные проблемы (skipped)»;
- скриншоты, HTML-страницы и URL при падении теста.

## Integrate with your tools

- [Настроить интеграции проекта в GitLab](https://gitlab.com/ppstanislav/test_it_integration/-/settings/integrations)
- [Подключить Test IT через `testit-adapter-pytest`](https://docs.testit.software/)

## Collaborate with your team

- [Пригласить участников в проект](https://docs.gitlab.com/user/project/members/)
- [Создать новый merge request](https://docs.gitlab.com/user/project/merge_requests/creating_merge_requests/)
- [Автоматически закрывать issue из merge request](https://docs.gitlab.com/user/project/issues/managing_issues/#closing-issues-automatically)
- [Включить approval'ы для merge request](https://docs.gitlab.com/user/project/merge_requests/approvals/)

## Test and Deploy

В GitLab доступна встроенная CI/CD:

- [Начало работы с GitLab CI/CD](https://docs.gitlab.com/ci/quick_start/)
- [Анализ кода через SAST](https://docs.gitlab.com/user/application_security/sast/)
- [Авто-деплой в Kubernetes / Amazon EC2 / Amazon ECS](https://docs.gitlab.com/topics/autodevops/requirements/)
- [Protected environments](https://docs.gitlab.com/ci/environments/protected_environments/)

---

# Editing this README

Структура ниже — отправная точка на основе шаблона с [makeareadme.com](https://www.makeareadme.com/).
Можно смело править под свои задачи.

## Name
**Test IT integration** — UI-автотесты платформы dvjob.kz с интеграцией в Test IT.

## Description
Проект автоматизирует UI-тестирование сайта [dvjob.kz](https://dvjob.kz) и
выгрузку результатов в систему управления тестами Test IT.

Что умеет:

- Авторизация под ролью **соискатель** и **работодатель** (валидные / невалидные данные).
- Проверки главной страницы: заголовок, логотип, переключение языков (RU / KZ / EN),
  поиск вакансий и резюме, виджет чата поддержки, блок акций, изображения услуг.
- Верхние меню «Соискателю» и «Работодателю»: каталоги, советы по интервью,
  формы договоров, консультации юриста и бухгалтера.
- Футер: видимость, адрес, телефон, e-mail, навигационные и юридические ссылки,
  соцсети, отсутствие пустых ссылок.
- Серверная валидация поля `username` на эндпоинте `/v1/accounts/sign-in`:
  невалидные email, омоглифы, SQL-инъекции, XSS-payload, превышение длины, пустые
  значения, а также известная уязвимость **null byte injection** (через `@xfail`).

Технологии:

- `pytest >= 9.2`
- `pytest-playwright >= 0.10` + `playwright >= 1.65`
- `allure-pytest >= 2.16` — структура отчётов и аттачи
- `python-dotenv >= 1.2` — переменные окружения из `.env`
- `testit-adapter-pytest >= 5.2` — выгрузка в Test IT

## Badges
При желании можно добавить бейджи через [shields.io](https://shields.io/):
процент успешных тестов, статус CI, версию Python и т. д.

## Visuals
Запустите `uv run allure serve allure-results` — в отчёт автоматически попадают
скриншоты при падениях, HTML-снапшоты и URL страницы.

## Installation
См. раздел [Getting started](#getting-started).

## Usage
См. раздел [Usage](#usage).

## Support
Вопросы и баги — в issue трекера GitLab-проекта:
`https://gitlab.com/ppstanislav/test_it_integration/-/issues`.
Для оперативного обсуждения — чат команды.

## Roadmap
- [ ] Параллельный запуск тестов через `pytest-xdist`
- [ ] Запуск в CI/CD GitLab с генерацией Allure-отчёта как артефакта
- [ ] Расширение покрытия: личный кабинет соискателя и работодателя
- [ ] Снятие `@xfail` с теста `test_sign_in_null_byte_vulnerability` после фикса бэкенда
- [ ] Добавление API-тестов

## Contributing
Контрибуции приветствуются. Перед мержем:

1. Поднимите отдельную ветку от `main`.
2. Проверьте, что `uv run pytest` проходит локально.
3. Добавьте `allure.step` / `testit.step` в новые шаги теста.
4. Для новых тест-кейсов обязательно указывайте `@pytest.mark.testit(external_id=...)`
   с уникальным `external_id`.
5. Не коммитьте `.env` и `connection_config.ini` — они уже в `.gitignore`.

## Authors and acknowledgment
- **ppstanislav-ops** — автор и мейнтейнер (`ppstanislav@gmail.com`)
- Спасибо команде DV Jobs за тестовый стенд и аккаунты

## License
Проект распространяется под лицензией MIT. См. файл `LICENSE`.

## Project status
Проект в активной разработке. Автотесты дополняются по мере доработки продукта.

