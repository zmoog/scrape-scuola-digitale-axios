import re

import datetime as dt
from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup

@dataclass
class Grade:
    date: str
    subject: str
    kind: str
    value: float
    comment: str
    teacher: str


class GradeParser:
    def parse(self, html: str):
        grades = []
        soup = BeautifulSoup(html, "html.parser")

        rows = soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")

            # skip rows without a span element
            if cols[3].span is None:
                continue

            # extract the value from an attribute named "data-original-title"
            data = cols[3].span.attrs["data-original-title"]

            # extract "Valore: 7,75" from the string "Voto: 7,75 <small>(scritto)</small><br>Valore: 7,75"
            # using regex and convert it to a float.
            value = float(re.search(r"Valore: ([\d,.]+)", data).group(1).replace(",", "."))

            grades.append(Grade(
                date=dt.datetime.strptime(cols[0].text.strip(), "%d/%m/%Y"),
                subject=cols[1].text.strip(),
                kind=cols[2].text.strip(),
                value=value,
                comment=cols[5].text.strip(),
                teacher=cols[6].text.strip(),
            ))
        
        return grades
