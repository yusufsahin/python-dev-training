const baseURL = import.meta.env.VITE_API_URL ?? "/api";

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = path.startsWith("http") ? path : `${baseURL}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error((err as { detail?: string }).detail ?? "İstek başarısız");
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export async function getTasks(params?: {
  status?: string;
  priority?: number;
  category_id?: number;
  search?: string;
}): Promise<import("../app/types").Task[]> {
  const sp = new URLSearchParams();
  if (params?.status) sp.set("status", params.status);
  if (params?.priority != null) sp.set("priority", String(params.priority));
  if (params?.category_id != null) sp.set("category_id", String(params.category_id));
  if (params?.search) sp.set("search", params.search);
  const q = sp.toString();
  return request(`/tasks${q ? `?${q}` : ""}`);
}

export async function getTask(id: number): Promise<import("../app/types").Task> {
  return request(`/tasks/${id}`);
}

export async function createTask(
  body: import("../app/types").TaskFormData
): Promise<import("../app/types").Task> {
  return request("/tasks", {
    method: "POST",
    body: JSON.stringify({
      ...body,
      due_date: body.due_date || null,
      category_id: body.category_id ?? null,
    }),
  });
}

export async function updateTask(
  id: number,
  body: Partial<import("../app/types").TaskFormData>
): Promise<import("../app/types").Task> {
  return request(`/tasks/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      ...body,
      due_date: body?.due_date ?? undefined,
      category_id: body?.category_id ?? undefined,
    }),
  });
}

export async function deleteTask(id: number): Promise<void> {
  return request(`/tasks/${id}`, { method: "DELETE" });
}

export async function getCategories(): Promise<import("../app/types").Category[]> {
  return request("/categories");
}

export async function createCategory(name: string, color: string): Promise<import("../app/types").Category> {
  return request("/categories", {
    method: "POST",
    body: JSON.stringify({ name, color }),
  });
}

export async function deleteCategory(id: number): Promise<void> {
  return request(`/categories/${id}`, { method: "DELETE" });
}
