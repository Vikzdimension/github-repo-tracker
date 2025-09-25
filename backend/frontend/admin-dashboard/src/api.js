export const API_BASE = "/api";

export async function fetchProjects() {
  const res = await fetch(`${API_BASE}/projects/`, {
    credentials: "include",
  });
  
  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }
  
  return await res.json();
}
