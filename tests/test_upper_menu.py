import allure
import pytest
import testit
from playwright.sync_api import expect
from pages.home_page import HomePage

EPIC = "UI тестирование dvjob.kz"
FEATURE = "Верхнее меню"

# ========== Меню «Соискателю» ==========
@pytest.mark.testit(external_id="upper-menu-candidates-vacancies")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Каталог вакансий» открывает страницу /ru/vacancies")
@allure.severity(allure.severity_level.CRITICAL)
def test_candidates_menu_vacancies(home: HomePage):
    """Проверяет переход в каталог вакансий из меню соискателя."""
    with testit.step("Клик по пункту «Каталог вакансий»"):
        home.click_vacancies_catalog()
    with testit.step("Проверка URL страницы"):
        expect(home.page).to_have_url("https://dvjob.kz/ru/vacancies")

@pytest.mark.testit(external_id="upper-menu-candidates-sovety")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Советы по прохождению интервью» открывает страницу с правилами интервью")
@allure.severity(allure.severity_level.NORMAL)
def test_candidates_menu_sovety(home: HomePage):
    """Проверяет переход на страницу советов по интервью."""
    with testit.step("Клик по пункту «Советы по прохождению интервью»"):
        home.click_interview_tips()
    with testit.step("Проверка видимости заголовка"):
        expect(home.page.get_by_role("heading", name="правил прохождения интервью")).to_be_visible()

@pytest.mark.testit(external_id="upper-menu-candidates-dogovor")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Заключение договора» открывает форму с заголовком «Заполните данные для заключения договора»")
@allure.severity(allure.severity_level.NORMAL)
def test_candidates_menu_dogovor(home: HomePage):
    """Проверяет открытие формы заключения договора."""
    with testit.step("Клик по пункту «Заключение договора»"):
        home.click_contract()
    with testit.step("Проверка видимости заголовка формы"):
        expect(home.page.get_by_role("heading", name="Заполните данные для заключения договора")).to_be_visible()

@pytest.mark.testit(external_id="upper-menu-candidates-cons-lawyer")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Консультация юриста» перенаправляет на страницу входа /ru/account/sign-in")
@allure.severity(allure.severity_level.NORMAL)
def test_candidates_menu_cons_lawyer(home: HomePage):
    """Проверяет редирект на страницу входа при клике на консультацию юриста."""
    with testit.step("Клик по пункту «Консультация юриста»"):
        home.click_lawyer_consult()
    with testit.step("Проверка URL страницы"):
        expect(home.page).to_have_url("https://dvjob.kz/ru/account/sign-in")

@pytest.mark.testit(external_id="upper-menu-candidates-cons-buh")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Консультация бухгалтера» перенаправляет на страницу входа /ru/account/sign-in")
@allure.severity(allure.severity_level.NORMAL)
def test_candidates_menu_cons_buh(home: HomePage):
    """Проверяет редирект на страницу входа при клике на консультацию бухгалтера."""
    with testit.step("Клик по пункту «Консультация бухгалтера»"):
        home.click_accountant_consult()
    with testit.step("Проверка URL страницы"):
        expect(home.page).to_have_url("https://dvjob.kz/ru/account/sign-in")

# ========== Меню «Работодателю» ==========
@pytest.mark.testit(external_id="upper-menu-employ-resumes")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Работодателю»")
@allure.title("Клик «Каталог резюме» открывает страницу /ru/resumes")
@allure.severity(allure.severity_level.CRITICAL)
def test_employ_menu_resumes(home: HomePage):
    """Проверяет переход в каталог резюме из меню работодателя."""
    with testit.step("Клик по пункту «Каталог резюме»"):
        home.click_resumes_catalog()
    with testit.step("Проверка URL страницы"):
        expect(home.page).to_have_url("https://dvjob.kz/ru/resumes")


