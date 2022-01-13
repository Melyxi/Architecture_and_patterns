class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class MyFramework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes, middleware_context):
        self.routes = routes
        self.middleware_context = middleware_context
        self.request = {}
        self.view = None

    def view_route(self, path):
        if path in self.routes:
            self.view = self.routes[path]
        else:
            self.view = PageNotFound404()

    def middleware(self):
        for front in self.middleware_context:
            front(self.request)

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'

        self.view_route(path)
        self.middleware()
        code, body = self.view(self.request)

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
