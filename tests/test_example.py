"""
Пример теста pytest + Playwright, размеченного маркером ``testit``.

Запуск:
    TESTIT_URL=https://team-x4ov.testit.software\\
    TESTIT_PRIVATE_TOKEN= WEtRWlFXbWhLUEN4dkF5b3Nh \\
    TESTIT_PROJECT_ID=01a14f77-4896-7bee-9481-74c42030828b\\
    TESTIT_CONFIGURATION_ID=2\\
    pytest -s test_example.py
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.testit(
    external_id="login-page-success-001",
    title="Успешный вход на страницу логина",
    work_item_id=None,  # GUID тест-кейса в TMS, если есть
    steps=[
        "Открыть страницу /login",
        "Заполнить поле email",
        "Заполнить поле пароль",
        "Нажать кнопку 'Войти'",
        "Проверить, что появился элемент навигации",
    ],
)
def test_login_success(page: Page):
    """Проверяет, что пользователь с валидными данными попадает на главную."""
    page.goto("https://www.saucedemo.com")
    page.locator("[data-test=\"username\"]").click()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").dblclick()
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()

    # Если это ожидание  упадёт — увидите пример работы с Failed outcome
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


@pytest.mark.testit(
    external_id="login-page-empty-002",
    title="Валидация пустой формы входа",
    steps=[
        "Открыть страницу /login",
        "Нажать кнопку 'Войти' без заполнения полей",
        "Проверить, что показаны сообщения об ошибках",
    ],
)
def test_login_empty_form_shows_errors(page: Page):
    page.goto("https://www.saucedemo.com")
    page.locator("[data-test=\"login-button\"]").click()

    expect(page.locator("[data-test=\"error\"]")).to_be_visible()

