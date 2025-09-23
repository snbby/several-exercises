import test from "node:test";
import assert from "node:assert/strict";
import { urlFetcher } from "./url-fetcher.js";

test("fetch client with max concurrency", async (t) => {

  const statusByUrl = new Map([
    [`https://pypi.org`, 200],
    [`https://github.com`, 200],
    [`https://google.com`, 200],
    [`https://linkedin.com`, 500],
    [`https://twitter.com`, 500],
  ]);
  const maxConcurrency = 3;

  const fakeFetchWithTimeout = async (url, _opts) => {
    const status = statusByUrl.get(url);
    return new Response("x", { status, statusText: "Mock" });
  };

  const urls = [...statusByUrl.keys()];
  const results = await urlFetcher(urls, maxConcurrency, fakeFetchWithTimeout);
  // Status code check
  assert.equal(results.responses[`https://pypi.org`].statusCode, 200);
  assert.equal(results.responses[`https://github.com`].statusCode, 200);
  assert.equal(results.responses[`https://google.com`].statusCode, 200);
  assert.equal(results.responses[`https://linkedin.com`].error, 'HTTP 500 Mock');
  assert.equal(results.responses[`https://twitter.com`].error, 'HTTP 500 Mock');

  // Check max concurrency
  assert.equal(results.concurrency.maxActive, maxConcurrency);
});

