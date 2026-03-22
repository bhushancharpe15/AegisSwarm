export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'https://aegisswarm-production.up.railway.app').replace(/\/$/, '');

const jsonHeaders = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
};

async function request(path, options = {}) {
    const { body, headers = {}, ...rest } = options;

    try {
        const response = await fetch(`${API_BASE_URL}${path}`, {
            ...rest,
            headers: { ...jsonHeaders, ...headers },
            body: body !== undefined ? JSON.stringify(body) : undefined,
        });

        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`API error on ${path}:`, error);
        throw error;
    }
}

export function getWebSocketUrl(path) {
    const wsBaseUrl = API_BASE_URL.replace(/^http:/, 'ws:').replace(/^https:/, 'wss:');
    return `${wsBaseUrl}${path}`;
}

export const missionApi = {
    start: () => request('/mission/start', { method: 'POST' }),
    pause: () => request('/mission/pause', { method: 'POST' }),
    resume: () => request('/mission/resume', { method: 'POST' }),
    stop: () => request('/mission/stop', { method: 'POST' }),
    reset: () => request('/mission/reset', { method: 'POST' }),
    status: () => request('/mission/status', { method: 'GET' }),
};

export const swarmApi = {
    status: () => request('/robots/status', { method: 'GET' }),
    positions: () => request('/robots/positions', { method: 'GET' }),
};

export const analyticsApi = {
    metrics: () => request('/analytics/metrics', { method: 'GET' }),
    heatmap: () => request('/analytics/heatmap', { method: 'GET' }),
};
