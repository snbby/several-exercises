class Semaphore {
  constructor(max) {
    this.max = max;
    this.inUse = 0;
    this.queue = [];
  }
  async acquire() {
    if (this.inUse < this.max) {
      this.inUse += 1;
      return;
    }
    await new Promise((resolve) => this.queue.push(resolve));
    this.inUse += 1;
  }
  release() {
    this.inUse -= 1;
    const next = this.queue.shift();
    if (next) next();
  }
}

function fetchWithTimeout(url, { timeoutMs = 3000, ...opts } = {}) {
  const ctrl = new AbortController();
  const id = setTimeout(() => ctrl.abort(), timeoutMs);
  return fetch(url, { redirect: `follow`, signal: ctrl.signal, ...opts })
    .finally(() => clearTimeout(id));
}


async function fetchOne(url, semaphore, results, fetchWithTimeoutImpl = fetchWithTimeout) {
  await semaphore.acquire();
  results.concurrency.active += 1;
  results.concurrency.maxActive = Math.max(results.concurrency.active, results.concurrency.maxActive);

  results.responses[url] = { statusCode: null, responseLength: null, error: null };

  // (Remove this log in production)
  console.log(`Fetching url: ${url}. Active coroutines: ${results.concurrency.active}`);

  try {
    const r = await fetchWithTimeoutImpl(url, { timeoutMs: 3000 });
    if (!r.ok) {
      throw new Error(`HTTP ${r.status} ${r.statusText}`);
    }

    // We can store body here, 
    const buf = await r.arrayBuffer();

    results.responses[url].statusCode = r.status;
    results.responses[url].responseLength = buf.byteLength;
  } catch (err) {
    if (err?.name === `AbortError`) {
      results.responses[url].error = `Timeout`;
    } else {
      results.responses[url].error = String(err?.message || err);
    }
  } finally {
    results.concurrency.active -= 1;
    semaphore.release();
  }
}

async function urlFetcher(urls, maxConcurrency = 5, fetchWithTimeoutImpl = fetchWithTimeout) {
  const results = {
    responses: {},
    concurrency: { active: 0, maxActive: 0 }
  };
  const semaphore = new Semaphore(maxConcurrency);

  await Promise.all(
    urls.map((u) => fetchOne(u, semaphore, results, fetchWithTimeoutImpl))
  );

  // (Remove this log in production)
  console.log(`Max active coroutines: ${results.concurrency.maxActive}`);

  return results;
}


export { urlFetcher };
