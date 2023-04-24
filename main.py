from gpt import generate_html
import asyncio
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
    if path.endswith('favicon.ico'):
        return web.Response(text='', status=404)
    if path.endswith('style.css'):
        return await style(request)
    if path not in pages:
        pages[path] = await generate_html(path, '')
        with open('pages.json', 'w') as f:
            json.dump(pages, f)

    return web.Response(text=pages[path], content_type='text/html')

app = web.Application()
app.add_routes([
    web.get('/{tail:.*}', handle)
])

web.run_app(app)
