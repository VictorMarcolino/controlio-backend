from unittest import TestCase

from src.tests.mixins.database import DatabaseMixin
from src.tests.mixins.flask_mixin import FlaskMixin
from src.tests.specs.api_spec import ApiSpec


class ApiTest(DatabaseMixin, FlaskMixin, ApiSpec, TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.database_set_up_class()

    def setUp(self) -> None:
        self.database_set_up()
        self.set_up_flask()

    def tearDown(self) -> None:
        self.database_tear_down()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.database_tear_down_class()

    # def assert_tenant_on_database(self, uuid):
    #     self.db_session.query(Tenant).filter(Tenant.uuid == uuid).one()

    def test_001_return_empty_result_when_ask_for_list_of_devices_with_with_none_registered(self):
        self.when_client_calls_get('/api/device_switch/')
        res = self.response
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, [])

    def test_002_include_device(self):
        self.when_client_calls_post('/api/device_switch/', json_body={
            'name': 'kimi no wa'
        })
        res = self.response
        self.assertEqual(res.status_code, 202)
        self.when_client_calls_get('/api/device_switch/')
        res = self.response
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json[0].get('name'), 'kimi no wa')
