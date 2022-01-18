from jinja2 import Template, Environment, FileSystemLoader
from os.path import join


def render(request, template_name, folder='templates', context=None, **kwargs):
    if context is None:
        context = {}
    context = {**{'request': request}, **context}

    # создаем объект окружения
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)

    return template.render(context)