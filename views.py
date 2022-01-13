from my_framework.shortcuts import render


class Index:
    def __call__(self, request):
        return '200 OK', render(request, 'index.html', context={'name': 'igor', 'key': 'value'})

class About:
    def __call__(self, request):
        return '200 OK', 'about'

def category(request):
    return '200 OK', 'category'

class PageCourse:
    def __call__(self, request):
        return '200 OK', 'PageCourse'

def create_user(request):
    if request['method'] == "GET":
        return '200 OK', render(request, 'create.html')
    if request['method'] == "POST":
        print(request['data'])
        return '200 OK', render(request, 'create.html')