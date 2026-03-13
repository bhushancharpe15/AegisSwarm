import React from 'react';
import Dashboard from './pages/Dashboard';
import { Hexagon } from 'lucide-react';

function App() {
    return (
        <div className="min-h-screen bg-[#060d1a] font-sans text-slate-100 selection:bg-indigo-500/30">
            {/* Top accent line */}
            <div className="h-px w-full bg-gradient-to-r from-transparent via-indigo-500/60 to-transparent" />

            <header className="border-b border-slate-800/60 bg-slate-900/40 px-6 py-3.5 backdrop-blur-xl sticky top-0 z-50">
                <div className="mx-auto flex max-w-7xl items-center justify-between">
                    {/* Logo + Title */}
                    <div className="flex items-center gap-3">
                        <div className="relative flex h-9 w-9 items-center justify-center">
                            <Hexagon className="h-9 w-9 text-indigo-500" strokeWidth={1.5} />
                            <span className="absolute text-xs font-black text-white">AS</span>
                        </div>
                        <div>
                            <h1 className="text-lg font-black tracking-tight leading-none">
                                <span className="bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">Aegis</span><span className="bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">Swarm</span>
                            </h1>
                            <p className="text-[10px] tracking-[0.2em] text-slate-500 uppercase mt-0.5">Swarm Intelligence Platform</p>
                        </div>
                    </div>

                    {/* Right: live indicators */}
                    <div className="flex items-center gap-3">
                        <div className="hidden sm:flex items-center gap-1.5 rounded-full border border-emerald-500/25 bg-emerald-500/8 px-3 py-1">
                            <span className="relative flex h-2 w-2">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-60"></span>
                                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
                            </span>
                            <span className="text-[10px] font-bold tracking-widest text-emerald-400 uppercase">System Online</span>
                        </div>
                        <div className="hidden md:flex items-center gap-1 text-[10px] text-slate-600 font-mono">
                            <span>v1.0.0</span>
                            <span className="mx-1 text-slate-700">·</span>
                            <span>20×20 Grid</span>
                            <span className="mx-1 text-slate-700">·</span>
                            <span>5 Robots</span>
                        </div>
                    </div>
                </div>
            </header>

            <main className="mx-auto max-w-7xl px-6 py-5">
                <Dashboard />
            </main>

            <footer className="border-t border-slate-800/50 px-6 py-5 text-center">
                <p className="text-[11px] text-slate-600">© 2026 <span className="text-slate-500">AegisSwarm</span> · Distributed Multi-Agent Intelligence Platform</p>
            </footer>
        </div>
    );
}

export default App;
