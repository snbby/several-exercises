import asyncio

from concurrency_exercise import url_fetcher

def test_concurrent_url_fetcher():
    urls = {
        'https://python.org': {'expected_status_code': 200},
        'https://pypi.org': {'expected_status_code': 200},
        'https://linkedin.com': {'expected_status_code': 200},
        'https://github.com': {'expected_status_code': 200},
        'https://google.com': {'expected_status_code': 200},
        'https://twitter.com': {'expected_status_code': 200},
        'https://nonexistent.com': {'expected_status_code': None},
    }
    max_concurrency = 5

    results = asyncio.run(url_fetcher(urls=urls.keys(), max_concurrency=max_concurrency))
    for url, result in results.items():
        assert result['status_code'] == urls[url]['expected_status_code']
