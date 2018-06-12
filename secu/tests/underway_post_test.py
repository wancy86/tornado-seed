import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
import common
from common.json import json_by_result

class T(AuthorizedTestCase):

    @property
    def path(self):
        return '/service/secu/underway'

    def setUp(self):
        super().setUp()
        self.data = {
            "itemid": "a6523c40a08f481a92c25c6945dc7b41"
        }

    def test_by_correct_info(self):
        response = requests.post(self.url, json=self.data)
        resp = response.json()
        self.assertEqual('000', resp['code'])

