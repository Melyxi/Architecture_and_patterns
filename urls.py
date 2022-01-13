from views import Index, About, category, PageCourse


routes = {
    '/': Index(),
    '/about/': About(),
    '/category/': category,
    '/page/': PageCourse(),
}