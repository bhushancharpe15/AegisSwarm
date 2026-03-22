import React, { useEffect, useState } from 'react';
import { Server, Wifi, WifiOff, Grid3x3, Bot, Gauge, Clock } from 'lucide-react';
import { API_BASE_URL } from '../services/api';

const Dot = ({ color }) => (
    <span className={`inline-block h-1.5 w-1.5 rounded-full ${color}`} />
);

const Pill = ({ icon: Icon, label, value, status }) => {
    const colors = {
        ok:      'border-emerald-500/20 bg-emerald-500/5 text-emerald-400',
        warn:    'border-amber-500/20 bg-amber-500/5 text-amber-400',
        error:   'border-rose-500/20 bg-rose-500/5 text-rose-400',
        neutral: 'border-slate-700/40 bg-slate-800/40 text-slate-400',
    };
    const dotColors = {
        ok: 'bg-emerald-500 shadow-[0_0_4px_rgba(16,185,129,0.8)]',
        warn: 'bg-amber-400',
        error: 'bg-rose-500',
        neutral: 'bg-slate-500',
    };
    return (
        <div className={`flex items-center gap-2 rounded-lg border px-3 py-1.5 text-xs font-medium ${colors[status]}`}>
            <Dot color={dotColors[status]} />
            <Icon className="h-3 w-3 opacity-70" />
            <span className="text-slate-500 text-[10px] uppercase tracking-wide">{label}</span>
            <span className="font-bold">{value}</span>
        </div>
    );
};

const SystemHealth = ({ isConnected, simulationData, missionStatus }) => {
    const [apiOk, setApiOk] = useState(null);
    const [elapsed, setElapsed] = useState(0);
    const [startTime] = useState(Date.now());

    useEffect(() => {
        fetch(`${API_BASE_URL}/health`)
            .then(r => r.ok ? setApiOk(true) : setApiOk(false))
            .catch(() => setApiOk(false));
    }, []);

    useEffect(() => {
        const t = setInterval(() => setElapsed(Math.floor((Date.now() - startTime) / 1000)), 1000);
        return () => clearInterval(t);
    }, [startTime]);

    const fmt = s => `${String(Math.floor(s / 60)).padStart(2,'0')}:${String(s % 60).padStart(2,'0')}`;
    const step = simulationData?.step ?? 0;
    const maxSteps = 100;
    const progress = Math.min((step / maxSteps) * 100, 100);

    return (
        <div className="mb-5 rounded-xl border border-slate-800/80 bg-slate-900/50 px-4 py-3 backdrop-blur-sm">
            <div className="flex flex-wrap items-center gap-2">
                <Pill icon={Server}   label="API"        value={apiOk === null ? 'CHECKING' : apiOk ? 'HEALTHY' : 'OFFLINE'} status={apiOk === null ? 'neutral' : apiOk ? 'ok' : 'error'} />
                <Pill icon={isConnected ? Wifi : WifiOff} label="STREAM"     value={isConnected ? 'LIVE' : 'OFFLINE'}    status={isConnected ? 'ok' : 'error'} />
                <Pill icon={Grid3x3}  label="GRID"       value="20 × 20"     status="neutral" />
                <Pill icon={Bot}      label="ROBOTS"     value={simulationData?.metrics?.active_robots ?? 5} status="neutral" />
                <Pill icon={Gauge}    label="STEP"       value={`${step} / ${maxSteps}`}  status={step >= maxSteps ? 'warn' : 'neutral'} />
                <Pill icon={Clock}    label="UPTIME"     value={fmt(elapsed)} status="neutral" />

                {/* Mission progress bar */}
                <div className="ml-auto flex items-center gap-2 min-w-[120px]">
                    <span className="text-[10px] uppercase tracking-widest text-slate-600">Mission</span>
                    <div className="flex-1 h-1 min-w-[80px] bg-slate-800 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-indigo-500 transition-all duration-500"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                    <span className="text-[10px] font-bold text-indigo-400 tabular-nums">{Math.round(progress)}%</span>
                </div>
            </div>
        </div>
    );
};

export default SystemHealth;
