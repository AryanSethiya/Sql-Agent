import { useAuth } from "../AuthContext";

export async function apiFetch(url, options = {}) {
  const { token } = useAuth();
  const headers = {
    ...(options.headers || {}),
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
  const response = await fetch(url, { ...options, headers });
  if (response.status === 401 || response.status === 403) {
    // Handle unauthorized
    throw new Error("Unauthorized");
  }
  return response.json();
} 