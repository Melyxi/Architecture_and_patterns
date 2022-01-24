from datetime import datetime

from jsonpickle import dumps, loads
from my_framework.shortcuts import render


# поведенческий паттерн - наблюдатель
# Курс
class Observer:

    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):

    def update(self, subject):
        print(('EMAIL->', 'к нам присоединился', subject.students[-1].name))


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


# поведенческий паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'
    success_url = None

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self, request):
        template_name = self.get_template()
        if request['method'] == 'POST':
            if self.success_url is not None:
                template_name = self.success_url

        context = self.get_context_data()
        return '200 OK', render(request, template_name, context=context)

    def __call__(self, request):
        return self.render_template_with_context(request)


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset, 'queryset')
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class DetailView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'object'
    pk = None
    object = None

    def get_queryset(self):
        return self.queryset

    @staticmethod
    def get_request_params(request):
        return request['request_params']

    def get_pk(self):
        return self.pk

    def get_object(self, request):
        self.pk = self.get_request_params(request).get('pk')
        self.object = None
        print(self.queryset, type(self.queryset))
        self.queryset = self.get_queryset()
        for item in self.queryset:
            if item.id == int(self.pk):
                self.object = item

        return self.object

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        context_object_name = self.get_context_object_name()
        context = {context_object_name: self.object}
        return context

    def get(self, request):
        self.get_object(request)
        return self.render_template_with_context(request)

    def __call__(self, request):
        if request['method'] == 'GET':
            return self.get(request)


class CreateView(TemplateView):
    template_name = 'create.html'

    def get_success_url(self):
        return self.success_url

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def post(self, request):
        data = self.get_request_data(request)
        self.create_obj(data)
        return self.render_template_with_context(request)

    def get(self, request):
        return self.render_template_with_context(request)

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            return self.post(request)
        else:
            return self.get(request)


# поведенческий паттерн - Стратегия
class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            time = datetime.now()
            f.write(f'[{time}]: {text}\n')
