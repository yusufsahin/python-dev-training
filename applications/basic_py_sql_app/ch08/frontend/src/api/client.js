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
          ? "Cannot reach the API. Start the backend on port 8000 (from ch08: uvicorn app.main:app --reload --host 127.0.0.1 --port 8000) or use docker compose up. Vite dev proxies /api to 127.0.0.1:8000."
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
    listDepartments: () => request("GET", "/departments"),
    createDepartment: (dto) => request("POST", "/departments", { body: dto }),
    updateDepartment: (id, dto) =>
      request("PUT", `/departments/${id}`, { body: dto }),
    deleteDepartment: (id) => request("DELETE", `/departments/${id}`),
    listStudents: () => request("GET", "/students"),
    createStudent: (dto) => request("POST", "/students", { body: dto }),
    updateStudent: (id, dto) =>
      request("PUT", `/students/${id}`, { body: dto }),
    deleteStudent: (id) => request("DELETE", `/students/${id}`),
  };
}
