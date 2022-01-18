from datetime import date


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


def fake_request(request):
    print('200 OK', 'Hello from Fake')


fronts = [secret_front, other_front, fake_request]
