import axios from 'axios';
import { API_BASE_URL } from '../config/constants';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - logs outgoing requests
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Response interceptor - logs responses and handles errors
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.config.url} - Status ${response.status}`);
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status (4xx, 5xx)
      console.error('[API Error]', error.response.status, error.response.data);
    } else if (error.request) {
      // Request made but no response (network error)
      console.error('[Network Error]', error.message);
    } else {
      // Error in request setup
      console.error('[Request Setup Error]', error.message);
    }
    return Promise.reject(error);
  }
);