import axios from 'axios';

const API_URL = '/hydroponics/api/';

const api = axios.create({
    baseURL: API_URL,
    auth: {
        username: 'admin@hydroponics.local',
        password: 'admin123456'
    }
});

export const getDevices = () => api.get('devices/');
export const getDeviceStats = (id) => api.get(`devices/${id}/stats/`);
export const getLatestReadings = (id) => api.get(`devices/${id}/latest_readings/`);

export default api;
