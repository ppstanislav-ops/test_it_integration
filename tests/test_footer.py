import re
import allure
import pytest
import testit
from playwright.sync_api import expect
from pages.footer_page import FooterPage

EPIC = "UI тестирование dvjob.kz"
FEATURE = "Футер"


# ========== Видимость ==========
@pytest.mark.testit(external_id="footer-visible")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Видимость")
@allure.title("Футер отображается на странице")
@allure.severity(allure.severity_level.CRITICAL)
def test_footer_visible(footer: FooterPage):
    """Проверяет видимость футера на главной странице."""
    expect(footer.footer).to_be_visible()


@pytest.mark.testit(external_id="footer-info")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Видимость")
@allure.title("В футере отображается текст с адресом компании")
@allure.severity(allure.severity_level.MINOR)
def test_footer_info(footer: FooterPage):
    """Проверяет наличие текста с адресом компании."""
    expect(footer.address_text).to_be_visible()


# ========== Навигационные ссылки ==========
@pytest.mark.testit(external_id="footer-about")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «О компании» открывает страницу О компании")
@allure.severity(allure.severity_level.CRITICAL)
def test_about(footer: FooterPage):
    """Проверяет переход на страницу «О компании»."""
    with testit.step("Клик по ссылке «О компании»"):
        footer.click_about()
    with testit.step("Проверка: идет переход на страницу «О компании»"):
        expect(footer.page).to_have_url("https://dvjob.kz/ru/about")


@pytest.mark.testit(external_id="footer-terms")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «Соглашение об оказании услуг» открывает эту страницу")
@allure.severity(allure.severity_level.NORMAL)
def test_terms(footer: FooterPage):
    """Проверяет переход на страницу «Соглашение об оказании услуг»."""
    with testit.step("Клик по ссылке «Соглашение об оказании услуг»"):
        footer.click_terms()
    with testit.step("Проверка: идет переход на страницу «Соглашение об оказании услуг»"):
        expect(footer.page).to_have_url("https://dvjob.kz/ru/terms")


@pytest.mark.testit(external_id="footer-privacy")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «Политика конфиденциальности» открывает эту страницу")
@allure.severity(allure.severity_level.NORMAL)
def test_privacy(footer: FooterPage):
    """Проверяет переход на страницу «Политика конфиденциальности»."""
    with testit.step("Клик по ссылке «Политика конфиденциальности»"):
        footer.click_privacy()
    with testit.step("Проверка: идет переход на страницу «Политика конфиденциальности»"):
        expect(footer.page).to_have_url("https://dvjob.kz/ru/privacy")


@pytest.mark.testit(external_id="footer-refund")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «Условия возврата» открывает страницу где описаны условия возврата")
@allure.severity(allure.severity_level.NORMAL)
def test_refund(footer: FooterPage):
    """Проверяет переход на страницу «Условия возврата»."""
    with testit.step("Клик по ссылке «Условия возврата»"):
        footer.click_refund()
    with testit.step("Проверка: идет переход на страницу «Условия возврата»"):
        expect(footer.page).to_have_url("https://dvjob.kz/ru/refund")


@pytest.mark.testit(external_id="footer-contacts")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «Контакты» открывает страницу Контакты")
@allure.severity(allure.severity_level.NORMAL)
def test_contacts(footer: FooterPage):
    """Проверяет переход на страницу «Контакты»."""
    with testit.step("Клик по ссылке «Контакты»"):
        footer.click_contacts()
    with testit.step("Проверка: идет переход на страницу «Контакты»"):
        expect(footer.page).to_have_url("https://dvjob.kz/ru/contacts")


# ========== Контакты ==========
@pytest.mark.testit(external_id="footer-phone")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Контакты")
@allure.title("Телефон в футере: видимый номер и корректная ссылка на номер телефона")
@allure.severity(allure.severity_level.CRITICAL)
def test_footer_phone(footer: FooterPage):
    """Проверяет отображение и корректность ссылки на телефон."""
    with testit.step("Телефон отображается"):
        expect(footer.phone_link).to_be_visible()
    with testit.step("Отображаемый номер содержит +7(777) 8155015"):
        expect(footer.phone_link).to_contain_text("+7(777) 8155015")

@pytest.mark.testit(external_id="footer-email")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Контакты")
@allure.title("E-mail в футере: текст ссылки и mailto:-href")
@allure.severity(allure.severity_level.NORMAL)
def test_footer_email(footer: FooterPage):
    """Проверяет корректность e-mail ссылки."""
    with testit.step("E-mail отображается"):
        expect(footer.email_link).to_be_visible()
    with testit.step("Текст ссылки — info@dvjob.kz"):
        expect(footer.email_link).to_contain_text("info@dvjob.kz")
    with testit.step("ссылка — mailto:info@dvjob.kz"):
        expect(footer.email_link).to_have_attribute("href", "mailto:info@dvjob.kz")


# ========== Текстовый контент ==========
@pytest.mark.testit(external_id="footer-address-full")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Текстовый контент")
@allure.title("В футере указан полный адрес: г.Алматы, пр. Достык 202, оф. 202")
@allure.severity(allure.severity_level.MINOR)
def test_footer_address_full(footer: FooterPage):
    """Проверяет наличие полного адреса в футере."""
    with testit.step("Проверка текста адреса"):
        expect(footer.footer).to_contain_text("г.Алматы, пр. Достык 202, оф. 202")


@pytest.mark.testit(external_id="footer-copyright")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Текстовый контент")
@allure.title("Отображается блок копирайта")
@allure.severity(allure.severity_level.TRIVIAL)
def test_footer_copyright(footer: FooterPage):
    """Проверяет видимость блока копирайта."""
    with testit.step("Проверка видимости копирайта"):
        expect(footer.copyright_text).to_be_visible()


@pytest.mark.testit(external_id="footer-legal-notice")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Текстовый контент")
@allure.title("Отображается юридическое уведомление")
@allure.severity(allure.severity_level.TRIVIAL)
def test_footer_legal_notice(footer: FooterPage):
    """Проверяет видимость юридического уведомления."""
    with testit.step("Проверка видимости уведомления"):
        expect(footer.legal_notice_text).to_be_visible()


# ========== Соцсети ==========
@pytest.mark.testit(external_id="footer-social-links")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Соцсети")
@allure.title("Отображается иконка соцсети: {href}")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.parametrize("href", [
    "https://t.me/allsetpro",
    "https://wa.me/77778155015",
    "https://www.instagram.com/dvjob.kz",
])
def test_footer_social_links(footer: FooterPage, href: str):
    """Проверяет видимость иконок социальных сетей."""
    with testit.step(f"Проверка видимости иконки {href}"):
        expect(footer.get_social_link(href)).to_be_visible()


# ========== Юридические ссылки (href) ==========
@pytest.mark.testit(external_id="footer-legal-links-href")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Юридические ссылки")
@allure.title("Ссылка «{name}» ведёт на URL по маске {href_re}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("name, href_re", [
    ("О компании", r"/ru/about/?$"),
    ("Соглашение об оказании услуг", r"/ru/terms/?$"),
    ("Политика конфиденциальности", r"/ru/privacy/?$"),
    ("Условия возврата", r"/ru/refund/?$"),
    ("Контакты", r"/ru/contacts/?$"),
])
def test_footer_legal_links_href(footer: FooterPage, name: str, href_re: str):
    """Проверяет корректность href у юридических ссылок."""
    with testit.step(f"Найти и проверить видимость ссылки «{name}»"):
        link = footer.get_legal_link_by_name(name)
        expect(link).to_be_visible()
    with testit.step("Ссылка соответствует ожидаемому шаблону"):
        expect(link).to_have_attribute("href", re.compile(href_re))


# ========== Пустые ссылки ==========
@pytest.mark.testit(external_id="footer-no-empty-links")
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Пустые ссылки")
@allure.title("В футере нет пустых ссылок")
@allure.severity(allure.severity_level.MINOR)
def test_footer_has_no_empty_links(footer: FooterPage):
    """Проверяет отсутствие пустых ссылок в футере."""
    with testit.step("Проверка количества пустых ссылок (должно быть 0)"):
        expect(footer.empty_links).to_have_count(0)