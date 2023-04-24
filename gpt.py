import functools
import asyncio
import openai

with open('key_openai.txt') as f:
    openai.api_key = f.read().strip()


async def run_async(non_async_function, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(non_async_function, *args, **kwargs))


async def promptChat(messages: list[dict["role": str, "content": str]], model: str = 'gpt-3.5-turbo', max_tokens: int = 128, temperature=0.7, top_p=1, frequency_penalty=0, presence_penalty=0, stop: list[str] | None = None):
    response = await run_async(openai.ChatCompletion.create, model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens, temperature=temperature, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stop=stop)
    return response.choices[0].message.content.strip()


async def generate_html(path, extra_info):
    msgs = [
        {"role": "system", "content": "I am a machine designed to build webpages for the `infinite website`. The `infinite website` is a website that has all content because it is generated in real time."},
        {"role": "user", "content": f"Generate a website HTML page with the relative path `{path}`. Link to other pages with relative paths **that do not end in .html**. Make sure that the page has many links to other pages and that it contains lots of useful information. Make sure that there is a link rel to the stylesheet `style.css` and that the page has a title. You are allowed to use scripts, but they must be as a script tag done fully within the html file. {extra_info}".strip()},
    ]

    html = await promptChat(msgs, max_tokens=1500, temperature=0,
                            top_p=1, frequency_penalty=0, presence_penalty=0, stop=['</html>'])
    html = '_||_'+(html.split('```')[-1])+'</html>'
    html = html.replace('_||_html', '')
    html = html.replace('_||_', '')
    return html
