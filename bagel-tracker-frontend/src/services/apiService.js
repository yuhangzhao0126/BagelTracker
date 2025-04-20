import axios from 'axios';
import { getToken } from './authService';

// const API_URL = 'http://localhost:8080/api'; // Update with your backend URL
// const API_URL = 'https://bagel-tracker-backend-cvdrf5eqb9bje5hp.eastasia-01.azurewebsites.net/api'; // Update with your backend URL
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000/api'
  : 'https://bagel-tracker-backend-cvdrf5eqb9bje5hp.eastasia-01.azurewebsites.net/api';

const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if user is authenticated
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const loginUser = async (credentials) => {
  try {
    const response = await apiClient.post('/auth/login', credentials);
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Network error occurred' };
  }
};

export const registerUser = async (userData) => {
  try {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Network error occurred' };
  }
};

export const searchUsers = async (prefix) => {
  try {
    const response = await apiClient.get(`/auth/users/search?prefix=${prefix}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Network error occurred' };
  }
};

export const recordMatch = async (matchData) => {
  try {
    const response = await apiClient.post('/matches', matchData);
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Network error occurred' };
  }
};

export const getUserMatches = async (userId, limit = 10) => {
  try {
    const response = await apiClient.get(`/matches/user/${userId}?limit=${limit}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Network error occurred' };
  }
};

export const getAllMatches = async (limit = 50) => {
  try {
    const response = await apiClient.get(`/matches/all?limit=${limit}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Network error occurred' };
  }
};
