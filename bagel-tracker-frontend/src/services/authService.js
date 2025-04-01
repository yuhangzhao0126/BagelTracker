const TOKEN_KEY = 'auth_token';
const USER_KEY = 'user';

export const login = (token, userData) => {
  localStorage.setItem(TOKEN_KEY, token);
  if (userData) {
    localStorage.setItem(USER_KEY, JSON.stringify(userData));
  }
};

export const logout = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

export const isAuthenticated = () => {
  return localStorage.getItem(TOKEN_KEY) !== null;
};

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

export const getUser = () => {
  const userData = localStorage.getItem(USER_KEY);
  return userData ? JSON.parse(userData) : null;
};