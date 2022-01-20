from my_framework.shortcuts import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import Debug, router, AppRoute

site = Engine()
logger = Logger('main')

routers = {}


# routes = {
#     '/': Index(),
#     '/about/': About(),
#     '/category/': Category(),
#     '/page/': PageCourse(),
#     '/create/': create_user,
#     '/create_category/': CreateCategory(),
#     '/courses_list/': CoursesList(),
#     '/create_course/': CreateCourse(),
#     '/copy_course/': CopyCourse(),
#     '/contacts/': Contacts(),
#     '/course/': Course(),
#
# }

@AppRoute(routers=routers, url='/')
class Index:

    def __call__(self, request):
        logger.log('Главная')
        objects_list = site.categories
        return '200 OK', render(request, 'index.html', context={'objects_list': objects_list})


@AppRoute(routers, '/about/')
class About:
    def __call__(self, request):
        return '200 OK', render(request, 'about.html')

@AppRoute(routers, '/category/')
class Category:
    def __call__(self, request):
        objects_list = site.get_category()
        print(objects_list)
        return '200 OK', render(request, 'category.html', context={'objects_list': objects_list})



@AppRoute(routers, '/page/')
class PageCourse:

    def __call__(self, request):
        return '200 OK', 'PageCourse'


@router(routers, '/create_course/')
@Debug('create_user')
def create_user(request):
    if request['method'] == "GET":
        return '200 OK', render(request, 'create.html')
    if request['method'] == "POST":
        print(request['data'])
        return '200 OK', render(request, 'create.html')


@AppRoute(routers, '/create_course/')
class CreateCourse:
    category_id = -1

    @Debug('CreateCourse')
    def __call__(self, request):
        logger.log('Создание курсов')
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            type_course = data['course']
            type_course = site.decode_value(type_course)
            name = site.decode_value(name)

            category = None
            print(self.category_id)
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                site.create_course(type_course, name, category)

            return '200 OK', render(request, 'course_list.html',

                                    context={'objects_list': category.courses, 'name': category.name, 'id': category.id,
                                             "count": category.count_course()})

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render(request, 'create_course.html',
                                        context={'name': category.name, 'id': category.id})

            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routers, '/courses_list/')
class CoursesList:
    @Debug('CoursesList')
    def __call__(self, request):
        logger.log('Курсы')
        try:

            id_category = request['request_params']['id']

            category = site.find_category_by_id(int(id_category))

            child_category = site.get_category(int(id_category))
            print(child_category, 'child_category')

            return '200 OK', render(request, 'course_list.html',
                                    context={'objects_list': category.courses, 'name': category.name,
                                             'count': category.count_course(),
                                             'id': category.id, 'child_category': child_category})

        except KeyError:
            return '200 OK', 'No courses have been added yet'



@AppRoute(routers, '/create_category/')
class CreateCategory:
    @Debug('CreateCategory')
    def __call__(self, request):
        logger.log('Создание категории')
        if request['method'] == 'POST':
            # метод пост
            parent_id = request['request_params'].get('id')
            if parent_id:
                parent_id = site.decode_value(parent_id)
            print(parent_id, 'parent_id')

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')
            print(category_id, 'category_id')
            category = None
            if parent_id:
                category = site.find_category_by_id(int(parent_id))

            site.create_category(name, category)


            print(site.categories, 'category')
            return '200 OK', render(request, 'category.html', context={'objects_list': site.get_category()})

        if request['method'] == "GET":
            categories = site.categories
            return '200 OK', render(request, 'create_category.html', context={'categories': categories})



@AppRoute(routers, '/copy_course/')
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']
        try:
            name = request_params['name']
            name = site.decode_value(name)
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
                return '200 OK', render(request, 'course_list.html',
                                        context={'objects_list': site.courses, 'name': new_course.category.name})
            return '200 OK', render(request, 'course_list.html', context={'objects_list': site.courses})

        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routers, '/contacts/')
class Contacts:
    def __call__(self, request):
        if request['method'] == "GET":
            return '200 OK', render(request, 'contacts.html')
        if request['method'] == "POST":
            return '200 OK', render(request, 'contacts.html')


@AppRoute(routers, '/course/')
class Course:
    def __call__(self, request):

        if request['method'] == 'GET':
            request_params = request['request_params']
            id_course = request_params.get('id')
            course = site.get_obj_course(int(id_course))
            print(course.users, 'course')
            return '200 OK', render(request, 'course.html', context={'object': course})

        if request['method'] == 'POST':
            request_params = request['request_params']
            id_course = request_params.get('id')
            data = request['data']

            name = site.decode_value(data.get('name'))
            type_user = site.decode_value(data.get('member'))

            user = site.create_user(type_user, name)
            course = site.get_obj_course(int(id_course))
            course.add_obj(user)
            return '200 OK', render(request, 'course.html', context={'object': course})

