// api.js
import axios from "axios";

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/',
  timeout: 10000,
});

// ✅ Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    console.log(`[API] → ${config.method?.toUpperCase()} ${config.url}`, {
      headers: config.headers,
      data: config.data,
    });
    return config;
  },
  (error) => {
    console.error('[API] ❌ Request error:', error);
    return Promise.reject(error);
  }
);

// ✅ Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API] ← ${response.status} ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    console.error('[API] ❌ Response error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
    });

    if (error.response?.status === 401) {
      console.warn('[API] Unauthorized — token invalid or expired. Clearing token.');
      localStorage.removeItem('token');
      // ⚠️ Jangan redirect manual di sini — biar router guard yang handle
    }

    return Promise.reject(error);
  }
);

export default apiClient;
