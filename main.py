from gpt import generate_html
import asyncio
import aiohttp_cors
from aiohttp import web
from os import listdir
import json

if 'pages.json' not in listdir():
    with open('pages.json', 'w') as f:
        json.dump({}, f)
with open('pages.json') as f:
    pages = json.load(f)


async def style(request):
    with open('style.css', 'r') as f:
        return web.Response(text=f.read(), content_type='text/css')


async def handle(request):
    path = '/'+request.match_info.get('tail', '')
    url_params = request.rel_url.query
    g = '&'.join([f'{k}={v}' for k, v in url_params.items()])
    if len(g) > 0:
        path += '?'+g
    if path.endswith('.js'):
        return web.Response(text='', status=404)
    if path.endswith('favicon.ico'):
        return web.Response(text='', status=404)
    if path.endswith('style.css'):
        return await style(request)
    if path not in pages:
        extra_info = ''
        if path == '/':
            extra_info = 'Please add a link that brings the user to the /search page.'
        elif path == '/search':
            extra_info = 'Please add a search field and a search button that will run window.location.href="/"+QUERY when clicked.'
        pages[path] = await generate_html(path, extra_info)
        with open('pages.json', 'w') as f:
            json.dump(pages, f)

    return web.Response(text=pages[path], content_type='text/html')

app = web.Application()
app.add_routes([
    web.get('/{tail:.*}', handle)
])
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*"
    )
})
for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app, host='127.0.0.1', port=8080)
