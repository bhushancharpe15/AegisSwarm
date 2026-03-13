import React from 'react';
import { Target, Search, Zap, Layers, AlertTriangle, Activity } from 'lucide-react';

const Stat = ({ icon: Icon, label, value, valueClass = 'text-slate-100', sub }) => (
    <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/40 space-y-1">
        <div className="flex items-center gap-1.5 text-slate-500">
            <Icon className="h-3 w-3" />
            <span className="text-[9px] font-bold uppercase tracking-wider">{label}</span>
        </div>
        <div className={`text-2xl font-black font-mono ${valueClass}`}>{value}</div>
        {sub && <div className="text-[9px] text-slate-600">{sub}</div>}
    </div>
);

const MetricsPanel = ({ metrics, step, robots }) => {
    const coverage = metrics?.coverage_percent || 0;
    const avgEnergy = robots?.length
        ? Math.round(robots.reduce((sum, r) => sum + r.energy, 0) / robots.length)
        : 0;

    const coverageColor = coverage >= 75 ? 'text-emerald-400' : coverage >= 40 ? 'text-amber-400' : 'text-indigo-400';
    const coverageBg    = coverage >= 75 ? 'bg-emerald-500/10 ring-1 ring-emerald-500/20' : coverage >= 40 ? 'bg-amber-500/10 ring-1 ring-amber-500/20' : 'bg-indigo-500/10 ring-1 ring-indigo-500/20';
    const coverageBar   = coverage >= 75 ? 'bg-emerald-500' : coverage >= 40 ? 'bg-amber-500' : 'bg-indigo-500';
    const energyBar     = avgEnergy >= 60 ? 'bg-emerald-500' : avgEnergy >= 30 ? 'bg-amber-500' : 'bg-rose-500';
    const stepPct       = Math.min(((step || 0) / 100) * 100, 100);

    return (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 backdrop-blur-md shadow-xl space-y-4">
            {/* Section header */}
            <div className="flex items-center gap-1.5">
                <span className="inline-block h-1.5 w-1.5 rounded-full bg-indigo-500" />
                <h2 className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Mission Analytics</h2>
            </div>

            {/* Coverage hero */}
            <div className={`flex flex-col items-center justify-center p-4 rounded-xl ${coverageBg}`}>
                <div className={`text-5xl font-black tabular-nums ${coverageColor}`}>{Math.round(coverage)}%</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">Area Coverage</div>
                <div className="w-full mt-3 h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div className={`h-full ${coverageBar} transition-all duration-700`} style={{ width: `${Math.min(coverage, 100)}%` }} />
                </div>
            </div>

            {/* Stats grid */}
            <div className="grid grid-cols-2 gap-2">
                <Stat icon={Layers}       label="Step"       value={step || 0}                   sub="/ 100 max" />
                <Stat icon={Search}       label="Found"      value={metrics?.events_detected || 0} sub="events" />
                <Stat icon={AlertTriangle} label="Collisions" value={metrics?.collisions || 0}     valueClass={metrics?.collisions > 0 ? 'text-rose-400' : 'text-slate-100'} />
                <Stat icon={Activity}     label="Active"     value={metrics?.active_robots || 0}   sub="robots" />
            </div>

            {/* Mission step progress */}
            <div className="space-y-1">
                <div className="flex justify-between text-[9px] font-bold uppercase tracking-wider text-slate-600">
                    <span>Mission Progress</span>
                    <span className="text-indigo-400 tabular-nums">{Math.round(stepPct)}%</span>
                </div>
                <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-indigo-500 transition-all duration-500" style={{ width: `${stepPct}%` }} />
                </div>
            </div>

            {/* Avg energy */}
            <div className="space-y-1">
                <div className="flex justify-between text-[9px] font-bold uppercase tracking-wider text-slate-600">
                    <span className="flex items-center gap-1"><Zap className="h-2.5 w-2.5" />Avg Energy</span>
                    <span className={avgEnergy >= 60 ? 'text-emerald-400' : avgEnergy >= 30 ? 'text-amber-400' : 'text-rose-400'}>
                        {robots?.length ? `${avgEnergy}%` : '—'}
                    </span>
                </div>
                <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className={`h-full ${energyBar} transition-all duration-700`} style={{ width: robots?.length ? `${avgEnergy}%` : '0%' }} />
                </div>
            </div>
        </div>
    );
};

export default MetricsPanel;
