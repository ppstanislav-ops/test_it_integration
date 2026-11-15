import allure
import pytest
import testit
from playwright.sync_api import expect
from pages.home_page import HomePage

EPIC = "UI тестирование dvjob.kz"
FEATURE = "Главная страница"

# ========== Заголовок и логотип ==========
@pytest.mark.testit(external_id="main-title")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Заголовок и логотип")
@allure.title("Заголовок страницы — «Международная платформа по поиску работы»")
@allure.severity(allure.severity_level.NORMAL)
def test_title(home: HomePage):
    """Проверяет заголовок страницы."""
    with testit.step("Проверка title страницы"):
        expect(home.page).to_have_title("Международная платформа по поиску работы")

@pytest.mark.testit(external_id="main-logo")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Заголовок и логотип")
@allure.title("Клик по логотипу открывает главную страницу /ru")
@allure.severity(allure.severity_level.NORMAL)
def test_logo(home: HomePage):
    """Проверяет переход на главную страницу по клику на логотип."""
    with testit.step("Клик по логотипу"):
        home.click_logo()
    with testit.step("Проверка: после клика отображается главная страница"):
        expect(home.page).to_have_url("https://dvjob.kz/ru")

# ========== Навигационные элементы ==========
@pytest.mark.testit(external_id="main-dipcoin")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные элементы")
@allure.title("Клик «Dipcoin» открывает страницу дипкойна")
@allure.severity(allure.severity_level.NORMAL)
def test_dipcoin(home: HomePage):
    """Проверяет переход на страницу дипкойна."""
    with testit.step("Клик по кнопке «Dipcoin»"):
        home.click_dipcoin()
    with testit.step("Проверка: после клика идет переход на страницу дипкойна"):
        expect(home.page).to_have_url("https://dvjob.kz/ru/dipcoin")

@pytest.mark.testit(external_id="main-lang-kz")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Языки")
@allure.title("Переключение языка на казахский открывает /kz")
@allure.severity(allure.severity_level.NORMAL)
def test_language_link_kz(home: HomePage):
    """Проверяет переключение на казахский язык."""
    with testit.step("Переключение на язык KZ"):
        home.select_kz_language()
    with testit.step("Проверка: идет переход на страницу KZ"):
        expect(home.page).to_have_url("https://dvjob.kz/kz")

@pytest.mark.testit(external_id="main-lang-en")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Языки")
@allure.title("Переключение языка на английский открывает /en")
@allure.severity(allure.severity_level.NORMAL)
def test_language_link_en(home: HomePage):
    """Проверяет переключение на английский язык."""
    with testit.step("Переключение на язык EN"):
        home.select_en_language()
    with testit.step("Проверка: идет переход на страницу EN"):
        expect(home.page).to_have_url("https://dvjob.kz/en")

# ========== Поиск ==========
@pytest.mark.testit(external_id="main-click-find-job")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Клик «Найти работу» открывает страницу вакансий")
@allure.severity(allure.severity_level.BLOCKER)
def test_click_find_job(home: HomePage):
    """Проверяет переход на страницу вакансий."""
    with testit.step("Клик по кнопке «Найти работу»"):
        home.click_find_job()
    with testit.step("Проверка: идет переход на страницу с вакансиями"):
        expect(home.page).to_have_url("https://dvjob.kz/ru/vacancies")

@pytest.mark.testit(external_id="main-click-find-employ")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Клик «Найти сотрудника» открывает страницу резюме")
@allure.severity(allure.severity_level.BLOCKER)
def test_click_find_employ(home: HomePage):
    """Проверяет переход на страницу резюме."""
    with testit.step("Клик по кнопке «Найти сотрудника»"):
        home.click_find_employee()
    with testit.step("Проверка: идет переход на страницу с резюме"):
        expect(home.page).to_have_url("https://dvjob.kz/ru/resumes")

@pytest.mark.testit(external_id="main-click-new-resume")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Клик «Новое резюме» открывает страницу создания резюме /ru/resumes/new")
@allure.severity(allure.severity_level.NORMAL)
def test_click_new_resume(home: HomePage):
    """Проверяет переход на страницу создания нового резюме."""
    with testit.step("Клик по кнопке «Новое резюме»"):
        home.click_new_resumes()
    with testit.step("Проверка: идет переход на страницу размещения нового резюме"):
        expect(home.page).to_have_url("https://dvjob.kz/ru/resumes/new")

@pytest.mark.testit(external_id="main-search-vacancies")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Поиск вакансий по запросу «Менеджер» возвращает результаты")
@allure.severity(allure.severity_level.BLOCKER)
def test_search_vacancies(home: HomePage):
    """Проверяет поиск вакансий."""
    query = "Менеджер"
    with testit.step(f"Ввод запроса '{query}' и запуск поиска"):
        home.search_vacancies(query)
    with testit.step("Проверка: идет переход на страницу с вакансиями Менеджер"):
        expect(home.vacancy_results.first).to_be_visible(timeout=30_000)

@pytest.mark.testit(external_id="main-search-resumes")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Поиск резюме по запросу «Менеджер» возвращает результаты")
@allure.severity(allure.severity_level.BLOCKER)
def test_search_resumes(home: HomePage):
    """Проверяет поиск резюме."""
    with testit.step("Ввод запроса 'Менеджер' и запуск поиска резюме"):
        home.search_resumes("Менеджер")
    with testit.step("Проверка: идет переход на страницу с резюме Менеджер"):
        expect(home.resume_results.first).to_be_visible(timeout=30_000)

# ========== Визуальные элементы ==========
@pytest.mark.testit(external_id="main-images-visible")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Визуальные элементы")
@allure.title("Изображения блока услуг отображаются на странице")
@allure.severity(allure.severity_level.MINOR)
def test_images_to_be_visible(home: HomePage):
    """Проверяет видимость изображений блока услуг."""
    with testit.step("Проверка видимости изображений"):
        home.check_services_images()

# ========== Промо и виджеты ==========
@pytest.mark.testit(external_id="main-promotions")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Промо и виджеты")
@allure.title("Клик «Акции» открывает страницу с акциями")
@allure.severity(allure.severity_level.NORMAL)
def test_promotions(home: HomePage):
    """Проверяет переход на страницу акций."""
    with testit.step("Клик по кнопке «Акции»"):
        home.click_promotions()
    with testit.step("Проверка: идет переход на страницу с акциями"):
        expect(home.page).to_have_url('https://dvjob.kz/ru/promotions', timeout=30_000)

@pytest.mark.testit(external_id="main-chat-widget")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Промо и виджеты")
@allure.title("Чат поддержки открывается и отображается виджет")
@allure.severity(allure.severity_level.NORMAL)
def test_chat_widget(home: HomePage):
    """Проверяет открытие чата поддержки."""
    with testit.step("Открытие чата поддержки"):
        home.open_chat_support()
    with testit.step("Проверка: отображается чат поддержки"):
        expect(home.chat_widget_container).to_be_visible(timeout=5000)

