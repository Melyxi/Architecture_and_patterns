from abc import ABC, abstractmethod
from copy import deepcopy
from quopri import decodestring
from patterns.behavioral_patterns import FileWriter, Subject


class User(ABC):
    auto_id = 0

    def __init__(self, name):
        self.id = User.auto_id
        self.name = name
        self.courses = []
        User.auto_id += 1

    @abstractmethod
    def create(self):
        pass

    def add_courses(self, obj):
        if obj not in self.courses:
            self.courses.append(obj)

class Teacher(User):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Учитель"
        Engine.teachers.append(self)

    def create(self):
        pass


class Student(User):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Студент"

        Engine.students.append(self)

    def create(self):
        pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип
class CoursePrototype:
    # прототип курсов обучения

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    auto_id = 0

    def __init__(self, name, category):
        self.id = Course.auto_id
        self.name = name
        self.category = category
        self.category.courses.append(self)

        self.users = []

        Course.auto_id += 1
        Engine.courses.append(self)
        self.add_courses_category(category)
        super(Course, self).__init__()

    def __getitem__(self, item):
        return self.users[item]

    def add_obj(self, obj):
        if obj not in self.users:
            self.users.append(obj)

    def add_courses_category(self, obj):
        if obj is not None:
            if obj.category is not None:
                obj.category.courses.append(self)
                return self.add_courses_category(obj.category)







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

    def __str__(self):
        return str(self.name)

    def count_course(self):
        return len(self.courses)

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result

    def add_courses(self, category):
        if category:
            self.courses.extend(self.courses)
            return self.add_courses(category)


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
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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

    def get_obj_course(self, id):
        print(self.courses)
        for item in self.courses:
            if item.id == id:
                return item
        return None

    def get_obj_student(self, id):
        for item in self.students:
            if item.id == id:
                return item
        return None

    def get_obj_teacher(self, id):
        for item in self.teachers:
            if item.id == id:
                return item
        return None


    def get_category(self, id_category=None):
        print(id_category, 'print(id_category)')
        if id_category is not None:
            res = []
            for item in self.categories:
                if item.category is not None:
                    if item.category.id == id_category:
                        res.append(item)

            return res

        else:
            return [item for item in self.categories if item.category is None]

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

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


if __name__ == "__main__":
    teacher = Teacher()
    teacher2 = Student()
    teacher.first_name = 'igor'

    print(teacher.first_name, teacher2.first_name)
