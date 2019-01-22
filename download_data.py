import os
import re
import csv
from splinter import Browser
from random_useragent import random_useragent
from urllib.parse import unquote


class DataGetter:
    """
    Using splinter for Browser controlling, because site won't allow us getting data using 'automated software'.
    Changing only user agent in request headers did not work.
    """

    DOWNLOAD_DIRECTORY = 'data/raw'
    BASEURL = 'https://www.findagrave.com'

    cemetery_expression = re.compile(
        r'<h2 itemprop="name" class="name-grave"><a itemprop="url" '
        r'href="(/cemetery/[0-9]+?/.*?)" '
        r'data-cemetery-name=".*?">.*?</a></h2>'
    )

    grave_expression = re.compile(
        r'<a class="memorial-item" id=".*?" href=".*?">(.*?)</a>',
        re.DOTALL
    )

    grave_details_expression = re.compile(
        r'<h2 class="name-grave"><i>(?P<name>.*?)</i>\s*</h2>.*?'
        r'<b class="text-muted birthDeathDates">(?P<dates>.*?)</b>.*?',
        re.DOTALL
    )

    def __init__(self, debug=False):
        self.debug = debug

        # Make download directory if it doesn't exits
        os.makedirs(self.DOWNLOAD_DIRECTORY, exist_ok=True)

        # Open browser
        agent = random_useragent.Randomize().random_agent('desktop', 'windows')
        self.browser = Browser('firefox', headless=not debug, user_agent=agent)

    def cleanup(self):
        self.browser.quit()

    def get_graves_data(self, html):
        for grave in self.grave_expression.finditer(html):
            details = next(self.grave_details_expression.finditer(
                grave.groups(0)[0]
            ), None)

            if details is None:
                print('Could not get data from grave. Skipping it.')
                continue

            yield details.groupdict(0)

    def get_data(self):
        path = 'cemetery/search'
        location_slovenia = 'country_87'
        orderby = 'memorials'

        cemetery_names = []

        for page in range(1, 5):
            self.browser.visit(
                f'{self.BASEURL}/{path}?locationId={location_slovenia}&orderby={orderby}&page={page}'
            )

            print('-' * 80)
            print(f'CEMETERIES page {page}')

            for cemetery in self.cemetery_expression.finditer(self.browser.html):
                *url, name = unquote(cemetery.groups(0)[0]).split('/')

                print(f'Visiting cemetery {name}')

                url = '/'.join(url)

                # navigate to page and wait for redirect
                self.browser.visit(
                    f'{self.BASEURL}{url}'
                )

                cemetery_full_name = self.browser.find_by_css('.bio-name').text
                cemetery_names.append(cemetery_full_name)

                # prepare csv writer
                csv_file = open(os.path.join(
                    self.DOWNLOAD_DIRECTORY, f'{name}.csv'), 'w'
                )
                csv_writer = csv.DictWriter(
                    csv_file,
                    fieldnames=['name', 'dates']
                )
                csv_writer.writeheader()

                search_url = self.browser.url + '/memorial-search?firstName=&lastName='
                total = 0

                for page in range(1, 200):
                    self.browser.visit(
                        search_url + f'&page={page}'
                    )

                    i = 0
                    for grave in self.get_graves_data(self.browser.html):
                        csv_writer.writerow(grave)
                        i += 1

                    if i == 0:
                        print(f'Finished with cemetery {name}.')
                        break

                    total += i
                    print(f'Page {page}, {i} graves, total {total} graves on this cemetery.')

                csv_file.close()

        with open(os.path.join('data', 'cemetery_names.csv'), 'w') as f:
            f.write('\n'.join(cemetery_names))


if __name__ == '__main__':
    d = DataGetter(debug=False)

    d.get_data()
    d.cleanup()
