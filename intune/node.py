import logging
import json

import requests
from bs4 import BeautifulSoup

from minemeld.ft.basepoller import BasePollerFT

LOG = logging.getLogger(__name__)


class Miner(BasePollerFT):
    def configure(self):
        super(Miner, self).configure()

        self.polling_timeout = self.config.get('polling_timeout', 30)
        self.verify_cert = self.config.get('verify_cert', True)
        self.url = 'https://docs.microsoft.com/en-us/mem/intune/fundamentals/intune-endpoints'

    def _build_iterator(self, item):
        # builds the request and retrieves the page
        rkwargs = dict(
            stream=False,
            verify=self.verify_cert,
            timeout=self.polling_timeout,
        )

        r = requests.get(
            self.url,
            **rkwargs
        )

        try:
            r.raise_for_status()
        except:
            LOG.debug('%s - exception in request: %s %s',
                      self.name, r.status_code, r.content)
            raise

        # parse the table
        html_soup = BeautifulSoup(r.content, "lxml")
        result=[]
        for row in html_soup.findAll('table')[0].tbody.findAll('tr'):
            col = row.findAll('td')[1].contents
            if col[0][0].isdigit():
                temp = ' '.join(map(str, col)).replace('<br/>', '').split()
            else:
                continue
        result.extend(temp)
        print result

        
        return result

    def _process_item(self, item):

        #indicator = item
        value = {
            'type': 'IPv4',
            'confidence': 100
        }

        return [[item, value]]



