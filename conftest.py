import json
import os
import platform
import sys
from pathlib import Path

import allure
import pytest
import testit
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.footer_page import FooterPage
from pages.auth_page import AuthPage
from pages.server_validation_page import ServerValidationAuthPage

BASE_URL = "https://dvjob.kz"
BUILD_ORDER_FILE = ".build_order"


# -------------------- Фикстуры --------------------

@pytest.fixture(autouse=True)
def setup_page(page: Page):
    """Общие настройки для всех тестов (без навигации)."""
    page.set_default_navigation_timeout(60_000)
    yield page


@pytest.fixture
def home(page: Page) -> HomePage:
    page.goto(f"{BASE_URL}/ru", wait_until="domcontentloaded")
    return HomePage(page)


@pytest.fixture
def footer(page: Page) -> FooterPage:
    page.goto(f"{BASE_URL}/ru", wait_until="domcontentloaded")
    return FooterPage(page)


@pytest.fixture
def auth(page: Page) -> AuthPage:
    page.goto(f"{BASE_URL}/ru/account/sign-in", wait_until="domcontentloaded")
    return AuthPage(page)


@pytest.fixture
def validation_page(page: Page) -> ServerValidationAuthPage:
    vp = ServerValidationAuthPage(page)
    vp.page.goto(f"{BASE_URL}/ru/account/sign-in", wait_until="load")
    return vp


# -------------------- Allure: окружение и метаданные --------------------

def _next_build_order() -> int:
    order = 0
    if os.path.exists(BUILD_ORDER_FILE):
        try:
            # Используем with open для безопасного чтения и закрытия файла
            with open(BUILD_ORDER_FILE, encoding="utf-8") as f:
                order = int(f.read().strip())
        except ValueError:
            order = 0
    order += 1
    with open(BUILD_ORDER_FILE, "w", encoding="utf-8") as f:
        f.write(str(order))
    return order


def pytest_sessionfinish(session, exitstatus):
    """Пишет environment.properties, executor.json и categories.json в Allure."""
    allure_dir = getattr(session.config.option, "allure_report_dir", None)
    if not allure_dir:
        return

    environment = {
        "Base URL": BASE_URL,
        "Browser": "Chromium (Playwright)",
        "Stand": "production",
        "Python": sys.version.split()[0],
        "OS": platform.platform(),
    }
    with open(os.path.join(allure_dir, "environment.properties"), "w", encoding="utf-8") as f:
        for key, value in environment.items():
            f.write(f"{key}={value}\n")

    executor = {
        "name": "Local run",
        "type": "local",
        "buildName": "dvjob-ui-tests",
        "buildOrder": _next_build_order(),
    }
    with open(os.path.join(allure_dir, "executor.json"), "w", encoding="utf-8") as f:
        json.dump(executor, f, ensure_ascii=False, indent=2)

    categories = [
        {"name": "Баги продукта", "matchedStatuses": ["failed"]},
        {"name": "Проблемы теста или окружения", "matchedStatuses": ["broken"]},
        {"name": "Известные проблемы (skipped)", "matchedStatuses": ["skipped"]},
    ]
    with open(os.path.join(allure_dir, "categories.json"), "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)


# -------------------- Скриншоты при падении --------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняем статус, чтобы фикстура ниже понимала, был ли фейл."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    """При падении теста прикладываем скриншот и HTML в Allure и Test IT."""
    yield
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call is not None and rep_call.failed:
        try:
            # 1. Сохраняем в Allure (для локальных отчетов)
            allure.attach(
                page.screenshot(full_page=True),
                name="Скриншот на месте падения",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(page.content(), name="HTML страницы", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.url, name="URL страницы")

            # 2. Сохраняем в файл и отправляем в Test IT
            artifacts_dir = Path("test-results")
            artifacts_dir.mkdir(exist_ok=True)

            # Формируем безопасное имя файла (убираем спецсимволы из имени теста)
            safe_name = request.node.name.replace("::", "_").replace("/", "_").replace("[", "_").replace("]", "_")
            screenshot_path = artifacts_dir / f"{safe_name}_failure.png"

            # Делаем скриншот и сохраняем на диск
            page.screenshot(path=str(screenshot_path), full_page=True)

            # Прикрепляем файл в Test IT
            testit.addAttachments(str(screenshot_path))

        except Exception as exc:
            # Выводим ошибку в консоль, чтобы не скрывать проблемы с фикстурой
            print(f"\n[Warning] Не удалось прикрепить скриншот: {exc}")


# -------------------- Регистрация маркера --------------------

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "testit(external_id, title, description=None, work_item_id=None, steps=None): "
        "передаёт метаданные в testit-adapter-pytest",
    )

