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

async def fetch(client: httpx.AsyncClient, url: str, semaphore: asyncio.Semaphore, results: dict, active: list, max_active: list):
    async with semaphore:
        active[0] += 1
        max_active[0] = max(max_active[0], active[0])
        results[url] = {
                'status_code': None,
                'response': None,
                'error': None
            }
        
        print(f'Fetching url: {url}. Active coroutines: {active[0]}') # Printing should be removed in production
        try:
            r = await client.get(url, timeout=3)
            r.raise_for_status()
            results[url]['response'] = r
            results[url]['status_code'] = r.status_code
        except httpx.TimeoutException as err:
            results[url]['error'] = 'Timeout'
        except httpx.RequestError as err:
            results[url]['error'] = str(err)
        finally:
            active[0] -= 1
    

async def url_fetcher(urls: list, max_concurrency: int = 5):
    results = dict()
    semaphore = asyncio.Semaphore(max_concurrency)
    active = [0]
    max_active = [0]

    async with httpx.AsyncClient(follow_redirects=True) as client:
        async with asyncio.TaskGroup() as tg:
            for url in urls:
                tg.create_task(fetch(client, url, semaphore, results, active, max_active))

    print(f'Max active coroutines: {max_active[0]}')
    return results


if __name__ == '__main__':
    results = asyncio.run(url_fetcher(urls))
    for url, result in results.items():
        print(f'Url: {url}. Status code: {result["status_code"]}. Response: {result["response"]}. Error: {result["error"]}')