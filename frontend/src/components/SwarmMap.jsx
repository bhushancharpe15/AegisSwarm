import React, { useMemo } from 'react';
import { Bot, Map as MapIcon, Wifi, WifiOff, Radio } from 'lucide-react';

const SwarmMap = ({ data, isConnected }) => {
    const robots = data?.robots || [];
    const heatmap = data?.heatmap || [];
    const gridSize = heatmap.length > 0 ? heatmap.length : 20;

    const robotSet = useMemo(() => {
        const s = new Set();
        robots.forEach(r => s.add(`${r.x},${r.y}`));
        return s;
    }, [robots]);

    const renderGrid = useMemo(() => {
        if (!heatmap.length) return null;

        return heatmap.map((row, x) =>
            row.map((cell, y) => {
                const hasRobot = robotSet.has(`${x},${y}`);
                let bg = '#0f172a';           // unexplored — slate-950
                if (cell === 1) bg = '#1e3a5f'; // partial — deep blue
                if (cell === 2) bg = '#1d4ed8'; // fully explored — blue-700

                return (
                    <div
                        key={`${x}-${y}`}
                        style={{
                            gridColumnStart: x + 1,
                            gridRowStart: y + 1,
                            backgroundColor: hasRobot ? 'transparent' : bg,
                            transition: 'background-color 0.4s',
                        }}
                        className="w-full h-full relative"
                    >
                        {hasRobot && (
                            <div
                                style={{ backgroundColor: bg }}
                                className="absolute inset-0 flex items-center justify-center"
                            >
                                <div className="h-[70%] w-[70%] rounded-full bg-violet-500 shadow-[0_0_8px_3px_rgba(139,92,246,0.7)] ring-1 ring-white/40" />
                            </div>
                        )}
                    </div>
                );
            })
        );
    }, [heatmap, robotSet]);

    return (
        <div className="relative rounded-2xl border border-slate-800 bg-slate-900/90 p-4 shadow-2xl backdrop-blur-xl ring-1 ring-white/5 overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between mb-3 px-1">
                <div className="flex items-center gap-2">
                    <MapIcon className="h-4 w-4 text-indigo-400" />
                    <h2 className="text-sm font-bold text-slate-100 tracking-wide">Swarm Intelligence Visualization</h2>
                </div>
                <div className={`flex items-center gap-1.5 rounded-full px-3 py-1 text-[10px] font-bold tracking-widest uppercase border ${
                    isConnected
                        ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'
                        : 'border-rose-500/30 bg-rose-500/10 text-rose-400'
                }`}>
                    {isConnected ? (
                        <><Radio className="h-3 w-3 animate-pulse" /> LIVE</>
                    ) : (
                        <><WifiOff className="h-3 w-3" /> DISCONNECTED</>
                    )}
                </div>
            </div>

            {/* Grid */}
            <div className="aspect-square w-full mx-auto rounded-xl border border-slate-800/60 shadow-inner overflow-hidden" style={{ background: '#060d1a' }}>
                <div
                    className="grid w-full h-full"
                    style={{
                        gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
                        gridTemplateRows: `repeat(${gridSize}, 1fr)`,
                        gap: '1px',
                        backgroundColor: '#1e293b40',
                    }}
                >
                    {renderGrid || (
                        <div className="col-span-full row-span-full flex flex-col items-center justify-center text-slate-600 space-y-3">
                            <Bot className="h-12 w-12 opacity-20 animate-pulse" />
                            <p className="text-sm italic">Waiting for environment data...</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Legend */}
            <div className="mt-3 flex flex-wrap items-center gap-x-5 gap-y-1 px-1 text-[10px] font-medium text-slate-500 uppercase tracking-wider">
                <div className="flex items-center gap-1.5"><div className="h-2.5 w-2.5 rounded-sm" style={{background:'#0f172a',border:'1px solid #334155'}}></div> Unexplored</div>
                <div className="flex items-center gap-1.5"><div className="h-2.5 w-2.5 rounded-sm" style={{background:'#1e3a5f'}}></div> Partial</div>
                <div className="flex items-center gap-1.5"><div className="h-2.5 w-2.5 rounded-sm" style={{background:'#1d4ed8'}}></div> Explored</div>
                <div className="flex items-center gap-1.5 ml-auto"><div className="h-2.5 w-2.5 rounded-full bg-violet-500 shadow-[0_0_6px_rgba(139,92,246,0.8)]"></div> Robot</div>
            </div>
        </div>
    );
};

export default SwarmMap;
