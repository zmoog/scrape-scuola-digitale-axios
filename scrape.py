from dataclasses import dataclass, asdict
from typing import List
import datetime as dt
import json
import os
import re

from playwright.sync_api import Playwright, sync_playwright

from axios import GradeParser


@dataclass
class Grade:
    date: str
    subject: str
    kind: str
    value: str
    comment: str
    teacher: str


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder for object containing datetime values."""

    def default(self, obj):
        if isinstance(obj, (dt.date, dt.datetime)):
            return obj.isoformat()


def run(playwright: Playwright) -> [str, List[Grade]]:
    browser = playwright.chromium.launch()  # headless=False, slow_mo=100)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://scuoladigitale.axioscloud.it/Pages/SD/SD_Login.aspx")
    page.get_by_placeholder("Inserire il CF Istituto/").click()
    page.get_by_placeholder("Inserire il CF Istituto/").fill(os.environ["AXIOS_CF"])
    page.get_by_placeholder("Codice utente o mail personale").click()
    page.get_by_placeholder("Codice utente o mail personale").fill(os.environ["AXIOS_USERNAME"])
    page.get_by_placeholder("Codice utente o mail personale").press("Tab")
    page.get_by_placeholder("Password").fill(os.environ["AXIOS_PASSWORD"])
    page.get_by_role("button", name="Accedi con Axios").click()
    page.locator("div").filter(has_text=re.compile(r"^Registro$")).locator("i").click()
    page.get_by_role("link", name="VAI ALLE TUE VALUTAZIONI").click()
    page.get_by_label("Visualizza 510152050100Tutti").select_option("-1")
    page.wait_for_load_state("networkidle")

    html = page.inner_html("table#table-voti tbody")
    grades = GradeParser().parse(html)

    # ---------------------
    context.close()
    browser.close()

    return html, grades


with sync_playwright() as playwright:
    html, grades = run(playwright)
    if len(grades) > 0:
        open("grades.html", "w").write(html)
        open("grades.json", "w").write(json.dumps([asdict(grade) for grade in grades], indent=4, cls=DateTimeEncoder))

