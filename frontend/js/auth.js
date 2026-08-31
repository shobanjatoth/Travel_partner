// /**
//  * Authentication Helper Module
//  */

// // Check if user is logged in
// function isAuthenticated() {
//   return !!localStorage.getItem(CONFIG.TOKEN_KEY);
// }

// // Enforce login for protected pages
// function requireAuth() {
//   if (!isAuthenticated()) {
//     window.location.href = '/pages/login.html';
//   }
// }

// // Handle login or registration submission
// async function submitAuth(isLogin, payload) {
//   const endpoint = isLogin ? '/auth/login' : '/auth/register';
//   const res = await apiRequest(endpoint, 'POST', payload);

//   if (res && res.ok) {
//     localStorage.setItem(CONFIG.TOKEN_KEY, res.data.access_token);
//     localStorage.setItem(CONFIG.USER_KEY, JSON.stringify({
//       id: res.data.user_id,
//       name: res.data.user_name,
//       email: res.data.email
//     }));
//     window.location.href = '/pages/dashboard.html';
//   } else {
//     alert(res?.data?.detail || 'Authentication failed');
//   }
// }

// // Logout function
// function logout() {
//   localStorage.removeItem(CONFIG.TOKEN_KEY);
//   localStorage.removeItem(CONFIG.USER_KEY);
//   window.location.href = '/pages/login.html';
// }







/**
 * Authentication Helper Module
 */

// ---------------------------------------------------------
// Check Authentication
// ---------------------------------------------------------

function isAuthenticated() {
  return Boolean(
    localStorage.getItem(CONFIG.TOKEN_KEY)
  );
}


// ---------------------------------------------------------
// Require Authentication
// ---------------------------------------------------------

function requireAuth() {

  if (!isAuthenticated()) {
    window.location.href = '/pages/login.html';
  }
}


// ---------------------------------------------------------
// Login / Registration
// ---------------------------------------------------------

async function submitAuth(isLogin, payload) {

  const endpoint = isLogin
    ? '/auth/login'
    : '/auth/register';

  const res = await apiRequest(
    endpoint,
    'POST',
    payload
  );

  if (!res) {
    alert('Authentication request failed.');
    return;
  }

  if (res.ok) {

    const data = res.data;

    // Make sure backend returned a token
    if (!data.access_token) {
      console.error(
        'Authentication response missing access_token:',
        data
      );

      alert('Authentication succeeded but no access token was returned.');
      return;
    }

    localStorage.setItem(
      CONFIG.TOKEN_KEY,
      data.access_token
    );

    localStorage.setItem(
      CONFIG.USER_KEY,
      JSON.stringify({
        id: data.user_id,
        name: data.user_name,
        email: data.email
      })
    );

    // Go to dashboard
    window.location.href =
      '/pages/dashboard.html';

    return;
  }

  alert(
    res.data?.detail ||
    'Authentication failed.'
  );
}


// ---------------------------------------------------------
// Logout
// ---------------------------------------------------------

function logout() {

  localStorage.removeItem(
    CONFIG.TOKEN_KEY
  );

  localStorage.removeItem(
    CONFIG.USER_KEY
  );

  window.location.href =
    '/pages/login.html';
}