function joinUrl(base, path) {
  const p = path.startsWith("/") ? path : `/${path}`;
  if (base === undefined || base === null || base === "") return p;
  const b = String(base).replace(/\/$/, "");
  return `${b}${p}`;
}

async function parseError(res) {
  let body;
  try {
    body = await res.json();
  } catch {
    body = {};
  }
  if (body.errors && Array.isArray(body.errors)) {
    return body.errors.join(" ");
  }
  if (body.detail) {
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) {
      return body.detail.map((d) => d.msg || d).join(" ");
    }
  }
  return res.statusText || `HTTP ${res.status}`;
}

export function createApiClient(apiBase) {
  const prefix = joinUrl(apiBase, "/api/v1");

  async function request(method, path, { body, headers } = {}) {
    const url = joinUrl(prefix, path);
    const opts = {
      method,
      headers: {
        ...(body ? { "Content-Type": "application/json" } : {}),
        ...headers,
      },
    };
    if (body !== undefined) {
      opts.body = JSON.stringify(body);
    }
    let res;
    try {
      res = await fetch(url, opts);
    } catch (err) {
      const isNetwork =
        err instanceof TypeError &&
        (err.message === "Failed to fetch" || err.message.includes("fetch"));
      throw new Error(
        isNetwork
          ? "Cannot reach the API. Start FastAPI on port 8000 (ch11: uvicorn app.main:app --reload) or use docker compose. Vite proxies /api to 127.0.0.1:8000."
          : err.message || String(err)
      );
    }
    if (res.status === 204) return null;
    if (!res.ok) {
      throw new Error(await parseError(res));
    }
    return res.json();
  }

  return {
    health: () => request("GET", "/health"),
    listTasks: () => request("GET", "/tasks"),
    getTask: (id) => request("GET", `/tasks/${encodeURIComponent(id)}`),
    createTask: (dto) => request("POST", "/tasks", { body: dto }),
    updateTask: (id, dto) =>
      request("PUT", `/tasks/${encodeURIComponent(id)}`, { body: dto }),
    deleteTask: (id) =>
      request("DELETE", `/tasks/${encodeURIComponent(id)}`),
  };
}
