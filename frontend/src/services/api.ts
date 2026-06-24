const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function loginUser(email: string, password: string) {
  const res = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error?.message || 'Login failed.');
  }

  // Store auth details
  localStorage.setItem('lablex_token', data.access_token);
  localStorage.setItem('lablex_tenant_id', data.tenant_id);
  localStorage.setItem('lablex_role', data.role);

  return data;
}

export function logoutUser() {
  localStorage.removeItem('lablex_token');
  localStorage.removeItem('lablex_tenant_id');
  localStorage.removeItem('lablex_role');
}

export function getAuthToken() {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('lablex_token');
  }
  return null;
}

export function getTenantId() {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('lablex_tenant_id');
  }
  return null;
}

export async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  const token = getAuthToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error?.message || 'Request failed.');
  }

  return data;
}
