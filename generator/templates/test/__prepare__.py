from ...base.test import BaseTestCase, AuthorizedTestCase

class Prepare(AuthorizedTestCase):

    def setUp(self):
        super().setUp()
        self.BODY = {
            [BODY]
        }
        if self.__module__.split('.')[-1].find('post') == -1:
            result = self.db.execute('[INSERT]', self.BODY)
            if result.lastrowid:
                self.BODY['id'] = result.lastrowid
            self.db.commit()
