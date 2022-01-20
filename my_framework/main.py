from quopri import decodestring

from my_framework.requests import GetRequests, PostRequests

class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class MyFramework(GetRequests, PostRequests):
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes, middleware_context):
        self.routes = routes
        self.middleware_context = middleware_context
        self.request = {}
        self.__view = None

    def view_route(self, path):
        if path in self.routes:
            self.__view = self.routes[path]
        else:
            self.__view = PageNotFound404()

    def middleware(self):
        for front in self.middleware_context:
            front(self.request)

    def post_get_request(self, method, environ):
        if method == 'POST':
            data = self.post_request_params(environ)
            self.request['data'] = data
            print(f'Нам пришёл post-запрос: {self.decode_value(data)}')
        if method == 'GET':
            request_params = self.get_request_params(environ)

            self.request['request_params'] = request_params
            print(f'Нам пришли GET-параметры: {self.decode_value(request_params)}')

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'
        self.request['path_info'] = path

        method = environ['REQUEST_METHOD']
        self.request['method'] = method

        self.post_get_request(method, environ)
        self.view_route(path)
        self.middleware()
        code, body = self.__view(self.request)

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data