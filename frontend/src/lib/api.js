// frontend/src/lib/api.js
const BASE = import.meta.env.VITE_API_BASE || "";

export async function api(path, init = {}) {
  const res = await fetch(`${BASE}/api${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init.headers || {}),
    },
  });
  if (!res.ok) throw new Error(await res.text());
  return res.status === 204 ? null : res.json();
}

// 公開API
export const listProjects = (params = new URLSearchParams()) =>
  api(`/projects/?${params.toString()}`);

export const getProject = (slug) => api(`/projects/${slug}`);

// 管理API（トークン必須）
export const adminListAll = (token) =>
  api(`/projects/admin/all`, { headers: { "X-Admin-Token": token } });

export const createProject = (body, token) =>
  api(`/projects/`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: { "X-Admin-Token": token },
  });

export const updateProject = (id, body, token) =>
  api(`/projects/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
    headers: { "X-Admin-Token": token },
  });

export const deleteProject = (id, token) =>
  api(`/projects/${id}`, {
    method: "DELETE",
    headers: { "X-Admin-Token": token },
  });
