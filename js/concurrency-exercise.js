import { urlFetcher } from "./url-fetcher.js";

(async () => {
    const maxConcurrency = 5;
    const urls = [
    `https://example.com`, 
    `https://httpbin.org/status/200`, 
    `https://httpbin.org/delay/8`,
    `https://python.org`,
    `https://pypi.org`,
    `https://linkedin.com`,
    `https://github.com`,
    `https://google.com`,
    `https://twitter.com`,
    `https://nonexistent.com`
];
  const res = await urlFetcher(urls, maxConcurrency);
  console.dir(res, { depth: 2 });
})()