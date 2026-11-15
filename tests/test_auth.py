import os
import dotenv
import allure
import pytest
from playwright.sync_api import expect
from pages.auth_page import AuthPage
import testit  # Импортируем модуль testit для шагов

dotenv.load_dotenv()

EPIC = "UI тестирование dvjob.kz"
FEATURE = "Авторизация"


# ========== Соискатель ==========
@pytest.mark.testit(external_id="auth-valid-candidate")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Авторизация соискателя")
@allure.title("Авторизация соискателя с валидными данными открывает страницу резюме")
@allure.severity(allure.severity_level.BLOCKER)
def test_auth_valid_candidate(auth: AuthPage):
    """Проверяет успешный вход в систему под ролью Соискатель с валидными кредами из .env."""
    login = os.getenv("CandidateLogin")
    password = os.getenv("CandidatePassword")
    with testit.step("Ввод логина и пароля"):  # <-- Заменили allure.step на testit.step
        auth.login_as_candidate(login, password)
    with testit.step("Проверка перехода на страницу резюме"):  # <-- Заменили
        expect(auth.page).to_have_url("https://dvjob.kz/ru/my/resumes", timeout=15_000)


@pytest.mark.testit(external_id="auth-not-valid-candidate")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Авторизация соискателя")
@allure.title("Авторизация соискателя с невалидным паролем показывает ошибку «Аккаунт недействителен»")
@allure.severity(allure.severity_level.NORMAL)
def test_auth_not_valid_candidate(auth: AuthPage):
    """Проверяет отображение сообщения об ошибке при неверных данных."""
    with testit.step("Ввод неверных данных"):  # <-- Заменили
        auth.login_as_candidate("test25@mail.ru", "225445111")
    with testit.step("Проверка текста ошибки"):  # <-- Заменили
        expect(auth.error_message).to_contain_text("Аккаунт не найден", timeout=15_000)


# ========== Работодатель ==========
@pytest.mark.testit(external_id="auth-valid-employer")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Авторизация работодателя")
@allure.title("Авторизация работодателя с валидными данными открывает страницу вакансий")
@allure.severity(allure.severity_level.BLOCKER)
def test_auth_valid_employer(auth: AuthPage):
    """Проверяет успешный вход в систему под ролью Работодатель с валидными кредами из .env."""
    login = os.getenv("EmployerLogin")
    password = os.getenv("EmployerPassword")
    with testit.step("Ввод логина и пароля"):
        auth.login_as_employer(login, password)
    with testit.step("Проверка перехода на страницу вакансий"):
        expect(auth.page).to_have_url("https://dvjob.kz/ru/my/vacancies", timeout=15_000)


@pytest.mark.testit(external_id="auth-not-valid-employer")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Авторизация работодателя")
@allure.title("Авторизация работодателя с невалидным паролем показывает сообщение об ошибке")
@allure.severity(allure.severity_level.NORMAL)
def test_auth_not_valid_employer(auth: AuthPage):
    """Проверяет отображение сообщения об ошибке при неверных данных работодателя."""
    with testit.step("Ввод неверных данных"):
        auth.login_as_employer("test@test.com", "1025889056")
    with testit.step("Проверка видимости ошибки"):  # <-- Заменили
        expect(auth.error_message).to_be_visible(timeout=15_000)