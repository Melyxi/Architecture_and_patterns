from my_framework.shortcuts import render


class Index:
    def __call__(self, request):
        return '200 OK', render(request, 'index.html', context={'name': 'igor', 'key': 'value'})


class About:
    def __call__(self, request):
        return '200 OK', render(request, 'about.html')


def category(request):
    return '200 OK', 'category'


class PageCourse:
    def __call__(self, request):
        return '200 OK', 'PageCourse'


class Contacts:
    def __call__(self, request):
        if request['method'] == "GET":
            return '200 OK', render(request, 'contacts.html')
        if request['method'] == "POST":
            return '200 OK', render(request, 'contacts.html')
