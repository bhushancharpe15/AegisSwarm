import { useState, useEffect, useRef, useCallback } from 'react';

export function useSimulationStream() {
    const [simulationData, setSimulationData] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const socketRef = useRef(null);
    const reconnectTimer = useRef(null);

    const connect = useCallback(() => {
        if (socketRef.current?.readyState === WebSocket.OPEN) return;

        // Use relative path so Vite proxy handles it in dev,
        // and the real host handles it in production (no hardcoded localhost)
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const socket = new WebSocket(`${protocol}//${window.location.host}/ws/simulation`);
        socketRef.current = socket;

        socket.onopen = () => {
            setIsConnected(true);
            if (reconnectTimer.current) {
                clearTimeout(reconnectTimer.current);
                reconnectTimer.current = null;
            }
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                setSimulationData(data);
            } catch (_) {}
        };

        socket.onclose = () => {
            setIsConnected(false);
            // Auto-reconnect after 2 seconds
            reconnectTimer.current = setTimeout(connect, 2000);
        };

        socket.onerror = () => {
            socket.close();
        };
    }, []);

    useEffect(() => {
        connect();
        return () => {
            clearTimeout(reconnectTimer.current);
            socketRef.current?.close();
        };
    }, [connect]);

    return { simulationData, isConnected };
}
