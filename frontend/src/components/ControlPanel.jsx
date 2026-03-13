import React from 'react';
import { Play, Pause, Square, RotateCcw, Activity } from 'lucide-react';
import { missionApi } from '../services/api';

const statusColors = {
    RUNNING:     'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
    PAUSED:      'text-amber-400 bg-amber-500/10 border-amber-500/30',
    STOPPED:     'text-rose-400 bg-rose-500/10 border-rose-500/30',
    COMPLETED:   'text-sky-400 bg-sky-500/10 border-sky-500/30',
    INITIALIZED: 'text-slate-300 bg-slate-700/30 border-slate-600/30',
};

const ControlPanel = ({ currentStatus }) => {
    const isRunning  = currentStatus === 'RUNNING';
    const isPaused   = currentStatus === 'PAUSED';
    const isIdle     = !currentStatus || currentStatus === 'INITIALIZED' || currentStatus === 'STOPPED' || currentStatus === 'COMPLETED';
    const colorClass = statusColors[currentStatus] || statusColors['INITIALIZED'];

    return (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5 backdrop-blur-md shadow-xl">
            <div className="flex items-center gap-2 mb-5">
                <Activity className="h-4 w-4 text-rose-500" />
                <h2 className="text-xs font-bold uppercase tracking-widest text-slate-300">Mission Command Center</h2>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {/* Launch */}
                <button
                    onClick={() => missionApi.start()}
                    disabled={isRunning || isPaused}
                    className="flex flex-col items-center justify-center gap-2 p-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed shadow-lg shadow-indigo-500/20 active:scale-95 transition-all"
                >
                    <Play className="h-5 w-5 fill-white" />
                    <span className="text-[10px] font-bold uppercase">Launch</span>
                </button>

                {/* Pause / Resume */}
                <button
                    onClick={() => isRunning ? missionApi.pause() : missionApi.resume()}
                    disabled={isIdle}
                    className="flex flex-col items-center justify-center gap-2 p-4 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed border border-slate-700 active:scale-95 transition-all text-slate-100"
                >
                    {isRunning ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5" />}
                    <span className="text-[10px] font-bold uppercase">{isRunning ? 'Pause' : 'Resume'}</span>
                </button>

                {/* Terminate */}
                <button
                    onClick={() => missionApi.stop()}
                    disabled={isIdle}
                    className="flex flex-col items-center justify-center gap-2 p-4 rounded-xl bg-rose-600/10 hover:bg-rose-600/25 disabled:opacity-40 disabled:cursor-not-allowed border border-rose-500/30 text-rose-400 active:scale-95 transition-all"
                >
                    <Square className="h-5 w-5" />
                    <span className="text-[10px] font-bold uppercase">Terminate</span>
                </button>

                {/* Reset */}
                <button
                    onClick={() => missionApi.reset()}
                    className="flex flex-col items-center justify-center gap-2 p-4 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 active:scale-95 transition-all text-slate-100"
                >
                    <RotateCcw className="h-5 w-5" />
                    <span className="text-[10px] font-bold uppercase">Reset</span>
                </button>

                {/* Status badge */}
                <div className={`col-span-2 md:col-span-1 flex flex-col items-center justify-center p-4 rounded-xl border ${colorClass}`}>
                    <span className="text-[9px] font-bold text-slate-500 uppercase mb-1">Status</span>
                    <span className="text-xs font-black uppercase tracking-widest">
                        {currentStatus || 'IDLE'}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default ControlPanel;
