/**
 * Simple module for making HTTP requests (uses fetch).
 */

const DEFAULT_HEADERS = {
  "Content-Type": "application/json",
  Accept: "application/json",
};

/**
 * Make an HTTP request.
 * @param {string} url
 * @param {object} [options] - fetch options (method, headers, body, etc.)
 * @returns {Promise<{ ok: boolean, status: number, data: any, headers: Headers }>}
 */
async function request(url, options = {}) {
  const { method = "GET", headers = {}, body, ...rest } = options;
  const res = await fetch(url, {
    method,
    headers: { ...DEFAULT_HEADERS, ...headers },
    body: body != null ? (typeof body === "string" ? body : JSON.stringify(body)) : undefined,
    ...rest,
  });

  const contentType = res.headers.get("content-type") || "";
  const data = contentType.includes("application/json")
    ? await res.json()
    : await res.text();

  return {
    ok: res.ok,
    status: res.status,
    data,
    headers: res.headers,
  };
}

function get(url, options = {}) {
  return request(url, { ...options, method: "GET" });
}

function post(url, body, options = {}) {
  return request(url, { ...options, method: "POST", body });
}

function put(url, body, options = {}) {
  return request(url, { ...options, method: "PUT", body });
}

function del(url, options = {}) {
  return request(url, { ...options, method: "DELETE" });
}

module.exports = {
  request,
  get,
  post,
  put,
  del,
};
