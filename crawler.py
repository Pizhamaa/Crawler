import asyncio
import aiohttp
from collections import deque
from bs4 import BeautifulSoup

queue = deque(['https://www.orthrusonline.ru/dex/'])
VISITED = set()

COUNT = 10
LEFT = True


async def do_request(session, url):
    async with session.get(url=url) as response:
        html = await response.text()
        return html


async def main():
    global LEFT

    async with aiohttp.ClientSession() as session:
        while queue and len(VISITED) < COUNT:

            if LEFT:
                url = queue.popleft()
            else:
                url = queue.pop()

            if url in VISITED:
                continue

            VISITED.add(url)

            html = await do_request(session=session, url=url)

            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a')

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
    asyncio.run(main())
    print(VISITED)
    print(len(VISITED))