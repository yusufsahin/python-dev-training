const prefix = import.meta.env.VITE_API_BASE ?? "";

async function parseJson(res) {
  const text = await res.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export async function api(path, { method = "GET", headers = {}, body, token } = {}) {
  const h = { ...headers };
  if (body !== undefined && !(body instanceof FormData)) {
    h["Content-Type"] = "application/json";
  }
  if (token) {
    h.Authorization = `Bearer ${token}`;
  }
  const res = await fetch(`${prefix}${path}`, {
    method,
    headers: h,
    body: body instanceof FormData ? body : body !== undefined ? JSON.stringify(body) : undefined,
  });
  const data = await parseJson(res);
  if (!res.ok) {
    const msg = typeof data?.detail === "string" ? data.detail : JSON.stringify(data?.detail ?? data);
    throw new Error(msg || res.statusText);
  }
  return data;
}
