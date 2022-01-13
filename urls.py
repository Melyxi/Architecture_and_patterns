from views import Index, About, category, PageCourse, create_user


routes = {
    '/': Index(),
    '/about/': About(),
    '/category/': category,
    '/page/': PageCourse(),
    '/create/': create_user,
}