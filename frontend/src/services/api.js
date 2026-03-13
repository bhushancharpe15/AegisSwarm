const API_BASE_URL = '/api';

export const missionApi = {
    start: () => fetch(`${API_BASE_URL}/mission/start`, { method: 'POST' }).then(r => r.json()),
    pause: () => fetch(`${API_BASE_URL}/mission/pause`, { method: 'POST' }).then(r => r.json()),
    resume: () => fetch(`${API_BASE_URL}/mission/resume`, { method: 'POST' }).then(r => r.json()),
    stop: () => fetch(`${API_BASE_URL}/mission/stop`, { method: 'POST' }).then(r => r.json()),
    reset: () => fetch(`${API_BASE_URL}/mission/reset`, { method: 'POST' }).then(r => r.json()),
    status: () => fetch(`${API_BASE_URL}/mission/status`).then(r => r.json()),
};

export const swarmApi = {
    status: () => fetch(`${API_BASE_URL}/robots/status`).then(r => r.json()),
    positions: () => fetch(`${API_BASE_URL}/robots/positions`).then(r => r.json()),
};

export const analyticsApi = {
    metrics: () => fetch(`${API_BASE_URL}/analytics/metrics`).then(r => r.json()),
    heatmap: () => fetch(`${API_BASE_URL}/analytics/heatmap`).then(r => r.json()),
};
