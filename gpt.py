import functools
import asyncio
import openai
from os import listdir

if 'key_openai.txt' not in listdir():
    print('Please create a file called key_openai.txt with your OpenAI API key in it.')
    exit()
with open('key_openai.txt') as f:
    openai.api_key = f.read().strip()


async def run_async(non_async_function, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(non_async_function, *args, **kwargs))


async def promptChat(messages: list[dict["role": str, "content": str]], model: str = 'gpt-3.5-turbo', max_tokens: int = 128, temperature=0.7, top_p=1, frequency_penalty=0, presence_penalty=0, stop: list[str] | None = None):
    fail_count = 0
    while True:
        try:
            response = await run_async(openai.ChatCompletion.create, model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens, temperature=temperature, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stop=stop)
            break
        except Exception as oops:
            print(oops)
            asyncio.sleep(2**fail_count)
            fail_count += 1
    return response.choices[0].message.content.strip()


async def generate_html(path, extra_info):
    print('Generating HTML for', path)
    html = f"""<html><head><link rel="stylesheet" href="style.css"><title>Inf - """
    msgs = [
        {"role": "system", "content": "I am a machine designed to build webpages for the `infinite website`. The `infinite website` is a website that has all content because it is generated in real time."},
        {"role": "user", "content": f"Generate a website HTML page with the relative path `{path}`. Link to other pages with relative paths **that start with `/`** and **do not end in .html**. Make sure that the page has many links to other pages and that it contains lots of useful information and that the urls are extremely verbose and descriptive about the content of the page it is linking to. Make sure that there is a link rel to the stylesheet `style.css` and that the page has a title. You are allowed to use scripts, but they must be as a script tag done fully at the end of the html file without external src. **Any words should be inside <a> tags linking to their respective page inline with the text Wikipedia-style.** Example: Quantum mechanics is a fundamental <a href=\"/theory\">theory</a> in <a href=\"/physics\">physics</a> that provides a description of the physical properties of <a href=\"/nature\">nature</a> at the scale of <a href=\"/atoms\">atoms</a> and <a href=\"/subatomic%20particles\">subatomic particles</a>.\n{extra_info}".strip()},
        {
            "role": "assistant",
            "content": f"Sure thing. Here is a webpage for the Infinite Website with path `{path}`.\n```{html}"
        }
    ]

    html += await promptChat(msgs, max_tokens=1500, temperature=0,
                             top_p=1, frequency_penalty=0.7, presence_penalty=0.5, stop=['</html>'])
    # print(html)
    html += '</html>'
    return html
