from jinja2 import Template
from os.path import join


def render(request, template_name, folder='templates', context=None, **kwargs):
    if context is None:
        context = {}
    context = {**{'request': request}, **context}
    file_path = join(folder, template_name)
    with open(file_path, encoding='utf-8') as file:
        template = Template(file.read())

    return template.render(context)