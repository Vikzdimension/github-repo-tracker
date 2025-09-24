export const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchProjects() {
  const res = await fetch(`${API_BASE}/projects/`, {
    credentials: "include",
  });
  
  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }
  
  return await res.json();
}
