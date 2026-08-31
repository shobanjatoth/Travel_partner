// Global Configuration
// const CONFIG = {
//   API_BASE_URL: 'http://127.0.0.1:8000/api', // Change to your Render/Production URL
//   TOKEN_KEY: 'tripmate_access_token',
//   USER_KEY: 'tripmate_user_info'
// };


/**
 * Global Configuration
 *
 * Frontend and FastAPI backend are served from the same Render domain.
 * Therefore, use a relative API path instead of localhost.
 */

const CONFIG = {
  API_BASE_URL: '/api',

  TOKEN_KEY: 'tripmate_access_token',
  USER_KEY: 'tripmate_user_info'
};