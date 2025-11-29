import axios from 'axios';

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('supabase.auth.token'); // Adjust based on how Supabase stores it or get from session
    if (token) {
        const session = JSON.parse(token);
        if (session?.currentSession?.access_token) {
            config.headers.Authorization = `Bearer ${session.currentSession.access_token}`;
        }
    }
    return config;
});

export default api;
