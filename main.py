from gpt import generate_html_through_markdown
import asyncio
from aiohttp import web
from os import listdir
import json
import subprocess
subprocess.run(['pygmentize', '-S', 'default', '-f', 'html',
               '-a', '.codehilite', '>', 'syntax.css'], shell=True)

if 'pages.json' not in listdir():
    with open('pages.json', 'w') as f:
        json.dump({}, f)
with open('pages.json') as f:
    pages = json.load(f)


async def style(request):
    with open('style.css', 'r') as f:
        return web.Response(text=f.read(), content_type='text/css')


async def syntax(request):
    with open('syntax.css', 'r') as f:
        return web.Response(text=f.read(), content_type='text/css')

generating = []


async def in_generating(path):
    while path in generating:
        await asyncio.sleep(0.1)


async def handle(request):
    path = '/'+(request.match_info.get('tail', '').strip('/'))
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
    if path.endswith('syntax.css'):
        return await syntax(request)
    if path not in pages:
        if path not in generating:
            generating.append(path)
            pages[path] = await generate_html_through_markdown(path)
            generating.remove(path)
        else:
            await in_generating(path)
        with open('pages.json', 'w') as f:
            json.dump(pages, f)

    return web.Response(text=pages[path], content_type='text/html')

app = web.Application()
app.add_routes([
    web.get('/{tail:.*}', handle)
])

web.run_app(app, host='127.0.0.1', port=8080)
