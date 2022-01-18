from views import Index, About, category, PageCourse, Contacts


routes = {
    '/': Index(),
    '/about/': About(),
    '/category/': category,
    '/page/': PageCourse(),
    '/contacts/': Contacts(),
}