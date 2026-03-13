import React from 'react';
import SwarmMap from '../components/SwarmMap';
import ControlPanel from '../components/ControlPanel';
import MetricsPanel from '../components/MetricsPanel';
import SystemHealth from '../components/SystemHealth';
import { useSimulationStream } from '../hooks/useSimulationStream';

const Dashboard = () => {
    const { simulationData, isConnected } = useSimulationStream();

    return (
        <div className="space-y-0 animate-in fade-in duration-700">
            <SystemHealth isConnected={isConnected} simulationData={simulationData} missionStatus={simulationData?.status} />
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-5">
            {/* Simulation Map Central Area */}
            <div className="lg:col-span-3 space-y-6">
                <SwarmMap
                    data={simulationData}
                    isConnected={isConnected}
                />
                <ControlPanel currentStatus={simulationData?.status} />
            </div>

            {/* Sidebar Metrics & Analytics */}
            <div className="space-y-6">
                <MetricsPanel metrics={simulationData?.metrics} step={simulationData?.step} robots={simulationData?.robots} />

                <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 backdrop-blur-sm">
                    <h3 className="text-[10px] font-bold uppercase tracking-widest text-slate-500 mb-3 flex items-center gap-1.5">
                        <span className="inline-block h-1.5 w-1.5 rounded-full bg-indigo-500" />
                        Active Robots
                    </h3>
                    <div className="space-y-2">
                        {simulationData?.robots?.map((robot) => {
                            const e = Math.round(robot.energy);
                            const barColor = e >= 60 ? 'bg-emerald-500' : e >= 30 ? 'bg-amber-400' : 'bg-rose-500';
                            return (
                                <div key={robot.id} className="p-2.5 rounded-lg bg-slate-800/60 border border-slate-700/40">
                                    <div className="flex items-center justify-between mb-1.5">
                                        <div className="flex items-center gap-2">
                                            <div className={`h-1.5 w-1.5 rounded-full ${robot.status === 'active' ? 'bg-emerald-500' : 'bg-rose-500'}`} />
                                            <span className="font-mono text-xs font-bold text-slate-200">{robot.id}</span>
                                        </div>
                                        <div className="flex items-center gap-2 text-[10px] text-slate-500">
                                            <span className="font-mono">[{robot.x},{robot.y}]</span>
                                            <span className={e >= 60 ? 'text-emerald-400' : e >= 30 ? 'text-amber-400' : 'text-rose-400'}>{e}%</span>
                                        </div>
                                    </div>
                                    <div className="h-0.5 w-full bg-slate-700 rounded-full overflow-hidden">
                                        <div className={`h-full ${barColor} transition-all duration-500`} style={{ width: `${e}%` }} />
                                    </div>
                                </div>
                            );
                        })}
                        {(!simulationData?.robots || simulationData.robots.length === 0) && (
                            <div className="text-center py-5 text-slate-600 italic text-xs">
                                No active robots detected
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
        </div>
    );
};

export default Dashboard;
