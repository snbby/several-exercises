import asyncio

import httpx

urls = [
    'https://python.org',
    'https://pypi.org',
    'https://linkedin.com',
    'https://github.com',
    'https://google.com',
    'https://twitter.com',
    'https://nonexistent.com'
]

async def fetch(client: httpx.AsyncClient, url: str, semaphore: asyncio.Semaphore, results: dict):
    async with semaphore:
        try:
            r = await client.get(url, timeout=10)
            r.raise_for_status()
            results[url] = {
                'status_code': r.status_code,
                'response': r,
                'error': None
            }
        except httpx.RequestError as err:
            results[url] = {
                'status_code': None,
                'response': None,
                'error': str(err)
            }
    

async def url_fetcher(urls: list, max_concurrency: int = 5):
    results = dict()
    semaphore = asyncio.Semaphore(max_concurrency)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        async with asyncio.TaskGroup() as tg:
            for url in urls:
                tg.create_task(fetch(client, url, semaphore, results))
    return results


if __name__ == '__main__':
    results = asyncio.run(url_fetcher(urls))
    for url, response in results.items():
        print(f'Url: {url}. Status code: {response["status_code"]}. Error: {response["error"]}')