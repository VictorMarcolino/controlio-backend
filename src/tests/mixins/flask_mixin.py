from flask import Flask

from app.blueprints import default_api


class FlaskMixin(object):
    _client = None
    app = None
    response = ...

    def set_up_flask(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(default_api, url_prefix='/api')
        self.app.testing = True
        self._client = self.app.test_client()

    @property
    def client(self):
        if not self._client:
            raise NotImplementedError()
        return self._client

    def when_client_calls_delete(self, path):
        self.response = self.client.delete(path)
        return self.response.json

    def when_client_calls_put(self, path, body):
        self.response = self.client.put(path, json=body)
        return self.response.json

    def assert_response_content(self, json_body):
        obj = self.response.json
        if isinstance(json_body, list):
            for i in json_body:
                for k, v in i.items():
                    result = list(filter(lambda x: (x.get(k) == v), obj))
                    self.assertEqual(result[0].get(k), v)
        else:
            for k, v in json_body.items():
                self.assertEqual(obj.get(k), v)

    def assert_response_not_found(self):
        self.assertEqual(self.response.status_code, 404)

    def assert_response_ok(self):
        self.assertEqual(self.response.status_code, 200)

    def when_client_calls_get(self, path):
        self.response = self.client.get(path)

    def when_client_calls_post(self, path, json_body):
        self.response = self.client.post(path, json=json_body)
