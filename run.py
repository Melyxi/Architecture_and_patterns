from wsgiref.simple_server import make_server
import click
from my_framework.main import MyFramework
# from urls import routes
from views import routers
from middlewares import fronts

application = MyFramework(routers, fronts)


@click.command()
@click.option('--port', default=8080)
@click.option('--addr', default='')
def run_server(addr, port):
    with make_server(addr, port, application) as httpd:
        print(f"Запуск на порту {port}...")
        httpd.serve_forever()


run_server()
