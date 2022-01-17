from abc import ABC, abstractmethod
from copy import deepcopy
from quopri import decodestring


class User(ABC):
    first_name = None
    last_name = None
    password = None

    @abstractmethod
    def create(self):
        pass


class Teacher(User):

    def create(self):
        pass


class Student(User):
    def create(self):
        pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# порождающий паттерн Прототип
class CoursePrototype:
    # прототип курсов обучения

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)

        Engine.courses.append(self)

# интерактивный курс
class InteractiveCourse(Course):
    def __init__(self, name, category):
        super().__init__(name, category)
        self.type = "Интерактивный"



# курс в записи
class RecordCourse(Course):
    def __init__(self, name, category):
        super().__init__(name, category)
        self.type = "Запись"


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# категория
class Category:
    auto_id = 0

    def __init__(self, name, category, description=None):
        self.id = Category.auto_id
        self.name = name
        self.category = category
        self.description = description
        self.courses = []

        # при создании объекта увеличивается счетчик
        Category.auto_id += 1

        Engine.categories.append(self)

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# основной интерфейс проекта
class Engine:
    categories = []
    teachers = []
    students = []
    courses = []

    def __init__(self):
        pass

    def create_category(self, name, category=None):
        return Category(name, category)

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    def create_course(self, type_, name, category):
        return CourseFactory.create(type_, name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)


if __name__ == "__main__":
    teacher = Teacher()
    teacher2 = Student()
    teacher.first_name = 'igor'

    print(teacher.first_name, teacher2.first_name)
