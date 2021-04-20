from unittest import TestCase

from tests.mixins.database import DatabaseMixin
from tests.mixins.flask_mixin import FlaskMixin
from tests.specs.api_spec import ApiSpec


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

    def test_001_return_empty_result_when_ask_for_list_of_actuators_with_with_none_registered(self):
        self.when_client_calls_get('/api/actuator_binary/')
        self.assert_200_ok()
        self.assert_size_of_json_response(0)

    def test_002_include_actuator(self):
        self.when_client_calls_post('/api/actuator_binary/', json_body={
            'name': 'kimi no wa'
        })
        self.assert_201_created()
        result = self.when_client_calls_get('/api/actuator_binary/')
        self.assert_200_ok()
        self.assertEqual(result[0].get('name'), 'kimi no wa')

    def test_003_remove_actuator(self):
        self.when_client_calls_post('/api/actuator_binary/', json_body={
            'name': 'kimi no wa'
        })
        self.assert_201_created()
        result = self.when_client_calls_get('/api/actuator_binary/')
        self.assert_200_ok()
        self.assert_size_of_json_response(1)
        self.assertEqual(result[0].get('name'), 'kimi no wa')
        self.when_client_calls_delete(f'/api/actuator_binary/{result[0].get("identifier")}')
        self.assert_200_ok()
        result = self.when_client_calls_get('/api/actuator_binary/')
        self.assert_200_ok()
        self.assert_size_of_json_response(0)

    def test_004_update_actuator(self):
        self.when_client_calls_post('/api/actuator_binary/', json_body={
            'name': 'kimi no wa'
        })
        self.assert_201_created()
        result = self.when_client_calls_get('/api/actuator_binary/')
        self.assert_200_ok()
        self.assert_size_of_json_response(1)
        self.assertEqual(result[0].get('name'), 'kimi no wa')
        result = self.when_client_calls_put(f'/api/actuator_binary/{result[0].get("identifier")}', json_body={
            'name': 'shingeki'
        })
        self.assert_200_ok()
        self.assertEqual(result.get('name'), 'shingeki')

    def test_005_update_actuator_error(self):
        self.when_client_calls_post('/api/actuator_binary/', json_body={
            'name': 'kimi no wa'
        })
        self.assert_201_created()
        result = self.when_client_calls_get('/api/actuator_binary/')
        self.assert_200_ok()
        self.assert_size_of_json_response(1)
        self.assertEqual(result[0].get('name'), 'kimi no wa')
        self.when_client_calls_put(f'/api/actuator_binary/{result[0].get("identifier")}', json_body={
            'kasjdh': 'shingeki'
        })
        self.assert_400_bad_request()

    def test_006_update_actuator_not_found_error(self):
        self.when_client_calls_get('/api/actuator_binary/')
        self.assert_200_ok()
        self.assert_size_of_json_response(0)
        self.when_client_calls_put(f'/api/actuator_binary/75144bdb-e47e-45e5-95df-0fa5b3ac991e', json_body={
            'kasjdh': 'shingeki'
        })
        self.assert_404_not_found()

    def assert_size_of_json_response(self, size):
        self.assertEqual(len(self.response.json), size)
