from datetime import datetime

import pandas as pd
import robobrowser


class CovidStats:

    def __init__(self, url="https://pl.wikipedia.org/wiki/Pandemia_COVID-19_w_Polsce#Statystyki"):
        self.url_link = url
        self.table_name = None

    def get_data(self):
        robot = robobrowser.RoboBrowser()
        robot.open(self.url_link)
        if robot.response.status_code == 403:
            raise ConnectionError("Forbidden")
        df = self._extract_table(soup=robot.parsed)
        return df

    @staticmethod
    def _extract_table(soup, class_name="wikitable", year="2020"):
        result = []
        region_names = []

        table = soup.find('table', attrs={'class': class_name})
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        regions = rows[2].find_all('th')

        for row in regions:
            region_names.append(row.text.replace('\n', '').strip())

        for row in rows[3+13:-3]:  # remove 3 first and 13 without full dataset
            try:
                date = row.find_all('th')[0].text.replace('\n', '').strip()
            except ValueError:
                # end of table
                break

            data = []
            row = row.find_all('td')
            for i, r in enumerate(row[3:-1]):
                r = r.text.replace('[e]', '').strip()
                r = ''.join([s for s in r if len(s.strip()) > 0])
                if r == '–':
                    r = 0
                else:
                    r = int(r)
                data.append(r)

            result.append([date] + data)

        df = pd.DataFrame(data=result, columns=['date'] + region_names)
        return df


if __name__ == '__main__':
    covid = CovidStats()
    covid.get_data()
