"""Playwright: form üzerinden dört işlem + sıfıra bölme UI."""

import re

import pytest
from playwright.sync_api import Page, expect


def _fill_and_submit(page: Page, first: str, operation: str, second: str) -> None:
    page.locator("#first_number").fill(first)
    page.locator("#operation").select_option(operation)
    page.locator("#second_number").fill(second)
    page.get_by_role("button", name="Hesapla").click()


@pytest.mark.ui
def test_page_loads_calculator_form(page: Page) -> None:
    page.goto("/")
    expect(page.locator("h1")).to_have_text("Hesap Makinesi")
    expect(page.locator("#first_number")).to_be_visible()
    expect(page.locator("#operation")).to_be_visible()
    expect(page.locator("#second_number")).to_be_visible()


@pytest.mark.ui
def test_addition_displays_result(page: Page) -> None:
    page.goto("/")
    _fill_and_submit(page, "10", "add", "5")
    expect(page.locator(".result h3")).to_have_text("Sonuç")
    expect(page.locator(".result p")).to_have_text(re.compile(r"10\s*\+\s*5\s*=\s*15"))


@pytest.mark.ui
def test_subtraction_displays_result(page: Page) -> None:
    page.goto("/")
    _fill_and_submit(page, "10", "subtract", "4")
    expect(page.locator(".result p")).to_have_text(re.compile(r"10\s*-\s*4\s*=\s*6"))


@pytest.mark.ui
def test_multiplication_displays_result(page: Page) -> None:
    page.goto("/")
    _fill_and_submit(page, "4", "multiply", "5")
    expect(page.locator(".result p")).to_have_text(re.compile(r"4\s*\*\s*5\s*=\s*20"))


@pytest.mark.ui
def test_division_displays_result(page: Page) -> None:
    page.goto("/")
    _fill_and_submit(page, "10", "divide", "2")
    expect(page.locator(".result p")).to_have_text(re.compile(r"10\s*/\s*2\s*=\s*5"))


@pytest.mark.ui
def test_division_by_zero_shows_error(page: Page) -> None:
    page.goto("/")
    _fill_and_submit(page, "10", "divide", "0")
    expect(page.locator(".error")).to_contain_text("Sıfıra bölme")
