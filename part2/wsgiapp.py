
def app(environ, start_response):
    print(environ['PATH_INFO'])
    start_response('200 OK', [('Content-Type', 'application/json')])
    path = environ['PATH_INFO']
    
    if path in routes:
        return routes[path]()
    else:
        return [b'Not found\n']


def hello():
    return [b'[{"hello": "World!"}]\n']

def folks():
    return [b"""
    [
        {"name": "Nick", "age": 10},
        {"name": "Bob", "age": 60},
        {"name": "Kevin", "age": 12}
    ]\n
    """]
routes = {
    "/hello": hello,
    "/folks": folks
}
