import os
import re
import allure
import dotenv
import pytest
import testit
from playwright.sync_api import expect
from pages.server_validation_page import ServerValidationAuthPage

dotenv.load_dotenv()

EPIC = "UI тестирование dvjob.kz"
FEATURE = "Серверная валидация"

ROLE_CONFIG = {
    "candidate": {
        "story": "Валидация поля username при авторизации соискателя",
        "login_method": "login_candidate_and_capture_response",
        "success_url_pattern": re.compile(r"/my/resumes"),
        "default_email_attr": "DEFAULT_EMAIL",
        "env_email_var": "CandidateLogin",
    },
    "employer": {
        "story": "Валидация поля username при авторизации работодателя",
        "login_method": "login_employer_and_capture_response",
        "success_url_pattern": re.compile(r"/my/vacancies"),
        "default_email_attr": "DEFAULT_EMPLOYER_EMAIL",
        "env_email_var": "EmployerLogin",
    },
}

@pytest.mark.testit(external_id="server-validation-sign-in")
@pytest.mark.parametrize("role", ["candidate", "employer"])
@pytest.mark.parametrize(
    "bad_username, expected_status, expected_error_code",
    [
        ("Tyyyuail.ru", 404, "account_not_found"),
        ("not_an_email", 404, "account_not_found"),
        ("user@", 404, "account_not_found"),
        ("@example.com", 404, "account_not_found"),
        ("Εmail@test.com", 404, "account_not_found"),
        ("' OR 1=1 --", 404, "account_not_found"),
        ("<script>alert(1)</script>", 404, "account_not_found"),
        ("a" * 10_000, 404, "account_not_found"),
        ("", 422, "validation_error"),
        ("   ", 422, "validation_error"),
    ],
    ids=[
        "несуществующий", "без_собаки", "без_домена", "без_локальной_части",
        "омоглифы", "sql_injection", "xss_payload", "превышение_длины",
        "пустой", "только_пробелы",
    ],
)
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.severity(allure.severity_level.CRITICAL)
def test_sign_in_server_validation(
    validation_page: ServerValidationAuthPage,
    role: str,
    bad_username: str,
    expected_status: int,
    expected_error_code: str,
):
    """Проверяет серверную валидацию поля username при авторизации."""
    config = ROLE_CONFIG[role]
    allure.dynamic.story(config["story"])
    allure.dynamic.title(f"[{role}] Сервер отклоняет username={bad_username!r} со статусом {expected_status} ({expected_error_code})")
    allure.dynamic.label("role", role)
    allure.dynamic.label("bad_username", bad_username)

    with testit.step(f"Установка перехвата с подменой username={bad_username!r}"):
        validation_page.setup_username_interception(bad_username, original_email=getattr(validation_page, config["default_email_attr"]))

    with testit.step("Выполнение авторизации и перехват ответа API"):
        response = getattr(validation_page, config["login_method"])()

    body = response.json()

    with testit.step("Проверка: токен не выдаётся ни при каких условиях"):
        assert body.get("success") is not True, f"СЕРЬЁЗНО: сервер принял '{bad_username}' как валидный username! status={response.status}, body={response.text()}"
        data = body.get("data")
        assert not (isinstance(data, dict) and "token" in data), f"СЕРЬЁЗНО: сервер выдал токен для '{bad_username}'! body={response.text()}"

    with testit.step(f"Проверка: HTTP-статус = {expected_status}"):
        assert response.status == expected_status, f"Ожидали статус {expected_status}, получили {response.status}: {response.text()}"

    with testit.step(f"Проверка: error_code = {expected_error_code}"):
        assert body.get("error_code") == expected_error_code, f"Ожидали error_code={expected_error_code!r}, получили {body.get('error_code')!r}: {response.text()}"

    with testit.step("Проверка: фронт остаётся на странице логина"):
        expect(validation_page.page).not_to_have_url(config["success_url_pattern"], timeout=5_000)
        expect(validation_page.page).to_have_url(re.compile(r"/account/sign-in"), timeout=5_000)

@pytest.mark.testit(external_id="server-validation-null-byte")
@pytest.mark.parametrize("role", ["candidate", "employer"])
@pytest.mark.xfail(
    strict=True,
    reason="ИЗВЕСТНАЯ УЯЗВИМОСТЬ: null byte injection. Сервер обрезает валидный email с \\x00 по нулевому байту."
)
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Известные уязвимости")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("уязвимость", "null-byte-injection")
def test_sign_in_null_byte_vulnerability(validation_page: ServerValidationAuthPage, role: str):
    """Проверяет наличие уязвимости null byte injection."""
    config = ROLE_CONFIG[role]
    valid_email = os.getenv(config["env_email_var"])
    bad_username = f"{valid_email}\x00"

    allure.dynamic.title(f"[{role}] Null byte в username не должен приводить к авторизации (уязвимость)")
    allure.dynamic.label("role", role)

    with testit.step(f"Установка перехвата с подменой username={bad_username!r}"):
        validation_page.setup_username_interception(bad_username, original_email=getattr(validation_page, config["default_email_attr"]))

    with testit.step("Выполнение авторизации и перехват ответа API"):
        response = getattr(validation_page, config["login_method"])()

    body = response.json()

    with testit.step("Проверка: сервер должен отклонить запрос"):
        assert body.get("success") is not True, "Уязвимость null byte всё ещё воспроизводится — убедись, что фикс бэкенда задеплоен, и сними @xfail."


