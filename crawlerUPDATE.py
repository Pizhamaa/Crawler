import asyncio
import aiohttp
from collections import deque
from bs4 import BeautifulSoup
import time as tm

# TODO ПОКА ЧТО НА ЭТАПЕ ДОРАБОТКИ!!!

queue = deque(['https://www.orthrusonline.ru/dex/'])

VISITED = set()

COUNT = 100

LEFT = True

SIZE = 10

async def do_request(session, url):
    try:
        async with session.get(url=url) as response:
            html = await response.text(encoding='utf-8', errors='ignore')
            return url, html
    except aiohttp.ClientResponseError:
        return url, None


async def do_requests(session, urls):
    tasks = [do_request(session=session, url=url) for url in urls]
    results = await asyncio.gather(*tasks)

    pages = {}

    for url, html in results:
        pages[url] = html

    return pages




def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    return links


async def main():
    global LEFT

    async with aiohttp.ClientSession() as session:
        while queue and len(VISITED) < COUNT:
            # urls = [queue.popleft() if LEFT else queue.pop() for _ in range(len(queue) // 2 if len(queue) != 1 else len(queue))]
            urls = [queue.popleft() if LEFT else queue.pop() for _ in range(min(SIZE, len(queue)))] # TODO
            pages = await do_requests(session=session, urls=urls)

            for url, html in pages.items():

                print(len(VISITED))

                if html is None:
                    continue

                if url in VISITED:
                    continue

                VISITED.add(url)

                links = await asyncio.to_thread(parse, html)

                for link in links:
                    href = link.get('href')

                    if href and href[:4] == 'http':
                        if href not in VISITED:
                            if LEFT:
                                queue.append(href)
                            else:
                                queue.appendleft(href)

                LEFT = not LEFT



if __name__ == '__main__':
    start = tm.time()

    asyncio.run(main())
    print(VISITED)
    print(len(VISITED))

    print(f'TIME: {tm.time() - start}')

# COUNT 1000 = 377 sec TODO улучшить результат