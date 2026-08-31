/**
 * Reusable HTTP Fetch Wrapper with Authorization Headers
 */
async function apiRequest(endpoint, method = 'GET', body = null) {
  const token = localStorage.getItem(CONFIG.TOKEN_KEY);

  const headers = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const options = { method, headers };
  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, options);

    // Auto-logout on expired session
    if (response.status === 401 && !endpoint.includes('/auth')) {
      localStorage.removeItem(CONFIG.TOKEN_KEY);
      localStorage.removeItem(CONFIG.USER_KEY);
      window.location.href = '/pages/login.html';
      return null;
    }

    const data = await response.json();
    return { ok: response.ok, status: response.status, data };
  } catch (error) {
    console.error('API Error:', error);
    return { ok: false, error: 'Network error communicating with backend server.' };
  }
}