import { useState, useEffect } from 'react';
import {
    Target, Layers, CheckCircle2, Shield, Brain, Server, Code2,
    FileText, TestTube, Gauge, ChevronRight, GitBranch, LayoutDashboard, Package,
    AlertTriangle, Globe, TrendingUp, CheckCircle, Circle, ExternalLink,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { PMService } from '../../services/pm.api';
import type { PMDashboard as PMDashboardType, PMPhase, PMFeature, PMArchLayer, PMDocEntry, PMTechDebt, PMDeployment, PMBusinessGoal } from '../../services/pm.api';

const STATUS_DOT: Record<string, string> = {
    not_started: 'bg-slate-400', in_progress: 'bg-blue-400', scaffolded: 'bg-amber-400',
    completed: 'bg-emerald-400', blocked: 'bg-red-400', deferred: 'bg-purple-400',
    planned: 'bg-slate-400', designing: 'bg-violet-400', in_development: 'bg-blue-400',
    testing: 'bg-amber-400', shipped: 'bg-emerald-400', deprecated: 'bg-red-400',
    missing: 'bg-red-400', draft: 'bg-amber-400', review: 'bg-blue-400',
    published: 'bg-emerald-400', stale: 'bg-orange-400',
    not_deployed: 'bg-slate-400', deploying: 'bg-blue-400', healthy: 'bg-emerald-400',
    degraded: 'bg-amber-400', down: 'bg-red-400',
};
const STATUS_LBL: Record<string, string> = {
    not_started: 'Not Started', in_progress: 'In Progress', scaffolded: 'Scaffolded',
    completed: 'Completed', blocked: 'Blocked', deferred: 'Deferred',
    planning: 'Planning', review: 'Review', cancelled: 'Cancelled',
};
const CAT_ICON: Record<string, typeof Code2> = {
    backend: Server, frontend: Code2, devops: Gauge, ai: Brain, ai_ml: Brain,
    docs: FileText, testing: TestTube, security: Shield, infra: Layers,
    database: Server,
};
const CAT_GRAD: Record<string, string> = {
    backend: 'from-blue-500 to-cyan-500', frontend: 'from-violet-500 to-purple-500',
    devops: 'from-amber-500 to-orange-500', ai: 'from-emerald-500 to-teal-500',
    ai_ml: 'from-emerald-500 to-teal-500',
    docs: 'from-slate-400 to-slate-500', testing: 'from-pink-500 to-rose-500',
    security: 'from-red-500 to-orange-500', infra: 'from-cyan-500 to-blue-500',
    database: 'from-orange-500 to-yellow-500',
};

function Ring({ value, size = 100 }: { value: number; size?: number }) {
    const r = (size - 8) / 2, c = 2 * Math.PI * r, o = c - (value / 100) * c;
    return (
        <div className="relative" style={{ width: size, height: size }}>
            <svg className="transform -rotate-90" width={size} height={size}>
                <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth={8} />
                <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="url(#pg)" strokeWidth={8}
                    strokeLinecap="round" strokeDasharray={c} strokeDashoffset={o} className="transition-all duration-1000" />
                <defs><linearGradient id="pg" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#06b6d4" /><stop offset="100%" stopColor="#6366f1" />
                </linearGradient></defs>
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-xl font-bold text-white">{value}%</span>
                <span className="text-[9px] text-slate-500 uppercase tracking-wider">done</span>
            </div>
        </div>
    );
}

function Bar({ value, gradient = 'from-cyan-500 to-indigo-500' }: { value: number; gradient?: string }) {
    return (
        <div className="h-1.5 w-full rounded-full bg-white/[0.06] overflow-hidden">
            <div className={`h-full rounded-full bg-gradient-to-r ${gradient} transition-all duration-700`} style={{ width: `${Math.min(value, 100)}%` }} />
        </div>
    );
}

function Pill({ status, label }: { status: string; label?: string }) {
    return (
        <span className="inline-flex items-center gap-1.5 text-[10px] font-medium text-slate-400">
            <span className={`w-1.5 h-1.5 rounded-full ${STATUS_DOT[status] || 'bg-slate-500'}`} />
            {label || STATUS_LBL[status] || status.replace(/_/g, ' ')}
        </span>
    );
}

function Section({ title, icon: Icon, children, count }: { title: string; icon: typeof Target; children: React.ReactNode; count?: number }) {
    return (
        <div className="mb-8">
            <div className="flex items-center gap-2 mb-4">
                <Icon className="w-5 h-5 text-cyan-400" />
                <h2 className="text-lg font-semibold text-white">{title}</h2>
                {count !== undefined && <span className="text-xs text-slate-600 bg-white/[0.04] px-2 py-0.5 rounded-full">{count}</span>}
            </div>
            {children}
        </div>
    );
}

export default function PMDashboard() {
    const [dash, setDash] = useState<PMDashboardType | null>(null);
    const [phases, setPhases] = useState<PMPhase[]>([]);
    const [features, setFeatures] = useState<PMFeature[]>([]);
    const [layers, setLayers] = useState<PMArchLayer[]>([]);
    const [docs, setDocs] = useState<PMDocEntry[]>([]);
    const [debts, setDebts] = useState<PMTechDebt[]>([]);
    const [deploys, setDeploys] = useState<PMDeployment[]>([]);
    const [goals, setGoals] = useState<PMBusinessGoal[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        (async () => {
            try {
                const [d, p, f, l, dc, dt, dp, g] = await Promise.all([
                    PMService.getDashboard(), PMService.listPhases(), PMService.listFeatures(),
                    PMService.listArchLayers(), PMService.listDocs(), PMService.listTechDebt(),
                    PMService.listDeployments(), PMService.listBusinessGoals(),
                ]);
                setDash(d); setPhases(p); setFeatures(f); setLayers(l);
                setDocs(dc); setDebts(dt); setDeploys(dp); setGoals(g);
            } catch (e) { console.error(e); } finally { setLoading(false); }
        })();
    }, []);

    if (loading) return (
        <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin" />
        </div>
    );
    if (!dash) return (
        <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
            <p className="text-red-400">Failed to load data</p>
        </div>
    );

    const stats = [
        { l: 'Tasks', v: dash.total_tasks, icon: Target, g: 'from-cyan-500/20 to-blue-500/20', b: 'border-cyan-500/20', ig: 'from-cyan-500 to-blue-600' },
        { l: 'Completed', v: dash.by_status?.completed || 0, icon: CheckCircle2, g: 'from-emerald-500/20 to-teal-500/20', b: 'border-emerald-500/20', ig: 'from-emerald-500 to-teal-600' },
        { l: 'Features', v: features.length, icon: Package, g: 'from-violet-500/20 to-purple-500/20', b: 'border-violet-500/20', ig: 'from-violet-500 to-purple-600' },
        { l: 'Tech Debts', v: debts.length, icon: AlertTriangle, g: 'from-red-500/20 to-rose-500/20', b: 'border-red-500/20', ig: 'from-red-500 to-rose-600' },
    ];

    const shippedFeatures = features.filter(f => f.status === 'shipped').length;
    const avgDocComplete = docs.length > 0 ? Math.round(docs.reduce((a, d) => a + d.completeness, 0) / docs.length) : 0;

    return (
        <div className="min-h-screen bg-[#0a0a0f] relative overflow-hidden p-4 sm:p-8 w-full">
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-[128px] pointer-events-none" />
            <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-500/5 rounded-full blur-[128px] pointer-events-none" />

            <div className="relative z-10 max-w-full mx-auto px-4 py-8 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
                            <LayoutDashboard className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-white tracking-tight">Project Management</h1>
                            <p className="text-slate-500 text-sm">SLDC Grid Ops &middot; Architecture Roadmap</p>
                        </div>
                    </div>
                    <div className="flex gap-3">
                        <Link to="/"><button className="px-4 py-2 rounded-xl text-sm text-slate-400 border border-white/10 hover:bg-white/[0.05] transition-all">Back</button></Link>
                        <Link to="/pm/tasks"><button className="px-5 py-2.5 rounded-xl text-sm font-medium text-white bg-gradient-to-r from-cyan-500 to-indigo-600 shadow-lg shadow-cyan-500/20">All Tasks</button></Link>
                    </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    {stats.map(s => (
                        <div key={s.l} className={`rounded-2xl border ${s.b} bg-gradient-to-br ${s.g} p-5 hover:scale-[1.02] transition-transform duration-300`}>
                            <div className="flex items-center justify-between mb-3">
                                <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{s.l}</span>
                                <div className={`w-9 h-9 rounded-xl bg-gradient-to-br ${s.ig} flex items-center justify-center`}>
                                    <s.icon className="w-4 h-4 text-white" />
                                </div>
                            </div>
                            <p className="text-3xl font-bold text-white">{s.v}</p>
                        </div>
                    ))}
                </div>

                {/* Progress + Deployments */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                    <div className="lg:col-span-2 rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
                        <div className="flex items-start gap-8 flex-wrap">
                            <Ring value={dash.completion_percentage || 0} />
                            <div className="flex-1 min-w-[200px]">
                                <h3 className="text-lg font-semibold text-white mb-3">Status Breakdown</h3>
                                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                                    {Object.entries(dash.by_status || {}).map(([s, c]) => (
                                        <div key={s} className="flex items-center gap-2 rounded-lg bg-white/[0.03] border border-white/[0.04] px-3 py-2">
                                            <span className={`w-2 h-2 rounded-full ${STATUS_DOT[s] || 'bg-slate-500'}`} />
                                            <div><p className="text-[10px] text-slate-500">{STATUS_LBL[s] || s}</p><p className="text-sm font-semibold text-white">{c}</p></div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Deployments */}
                    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
                        <div className="flex items-center gap-2 text-cyan-400 mb-4">
                            <Globe className="w-4 h-4" /><span className="text-xs font-semibold uppercase tracking-wider">Deployments</span>
                        </div>
                        <div className="space-y-3">
                            {deploys.length > 0 ? deploys.map(d => (
                                <div key={d.id} className="flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <span className={`w-2 h-2 rounded-full ${STATUS_DOT[d.status] || 'bg-slate-500'}`} />
                                        <span className="text-sm text-slate-300">{d.environment_display || d.environment}</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="text-[10px] text-slate-500">{d.status_display || d.status}</span>
                                        {d.url && <a href={d.url} target="_blank" rel="noopener noreferrer"><ExternalLink className="w-3 h-3 text-slate-600 hover:text-cyan-400" /></a>}
                                    </div>
                                </div>
                            )) : <p className="text-xs text-slate-500">No deployments found</p>}
                        </div>
                    </div>
                </div>

                {/* Phases */}
                <Section title="Execution Phases" icon={GitBranch} count={phases.length}>
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                        {phases.map(p => (
                            <Link to={`/pm/tasks?phase=${p.id}`} key={p.id}>
                                <div className="group rounded-2xl border border-white/[0.06] bg-white/[0.02] hover:bg-white/[0.04] hover:border-white/[0.12] p-5 transition-all h-full cursor-pointer">
                                    <div className="flex items-start justify-between mb-3">
                                        <div className="flex items-center gap-3">
                                            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-500/15 to-indigo-500/15 border border-cyan-500/15 flex items-center justify-center">
                                                <span className="text-xs font-bold text-cyan-400">P{p.phase_number}</span>
                                            </div>
                                            <div>
                                                <h3 className="font-semibold text-white text-sm group-hover:text-cyan-300 transition-colors">{p.name}</h3>
                                                <p className="text-[11px] text-slate-500">{p.duration_weeks || 2}w &middot; {p.task_count || 0} tasks</p>
                                            </div>
                                        </div>
                                        <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-cyan-400" />
                                    </div>
                                    <Bar value={p.progress_percentage || 0} />
                                    <div className="flex items-center justify-between mt-2">
                                        <Pill status={p.status} /><span className="text-[11px] text-slate-500">{p.progress_percentage || 0}%</span>
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                </Section>

                {/* Features */}
                <Section title="Features" icon={Package} count={features.length}>
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
                        {features.map(f => {
                            const Icon = CAT_ICON[f.category] || Code2;
                            return (
                                <div key={f.id} className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-4 flex items-center gap-3">
                                    <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${CAT_GRAD[f.category] || 'from-slate-500 to-slate-600'} flex items-center justify-center shrink-0`}>
                                        <Icon className="w-4 h-4 text-white" />
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm text-white truncate">{f.name}</p>
                                        <div className="flex items-center gap-2 mt-0.5">
                                            <Pill status={f.status} label={f.status_display || f.status} />
                                            {f.user_facing && <span className="text-[9px] text-cyan-500 bg-cyan-500/10 px-1.5 py-0.5 rounded">User-facing</span>}
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                    {features.length === 0 ? <p className="text-xs text-slate-500">No features found</p> : 
                    <p className="text-xs text-slate-600 mt-3">{shippedFeatures} shipped &middot; {features.length - shippedFeatures} planned/in progress</p>}
                </Section>

                {/* Architecture + Docs row */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Architecture Layers */}
                    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <Layers className="w-5 h-5 text-cyan-400" />
                            <h2 className="text-lg font-semibold text-white">Architecture</h2>
                            <span className="text-xs text-slate-600 bg-white/[0.04] px-2 py-0.5 rounded-full">{layers.length} layers</span>
                        </div>
                        <div className="space-y-1.5 max-h-80 overflow-y-auto pr-1">
                            {layers.length > 0 ? layers.map(l => (
                                <div key={l.id} className="flex items-center gap-3 rounded-lg bg-white/[0.02] border border-white/[0.04] px-3 py-2">
                                    <span className="text-[11px] font-mono text-cyan-400 w-6 shrink-0">L{l.layer_number}</span>
                                    <span className="text-sm text-slate-300 flex-1 truncate">{l.name}</span>
                                    <span className="text-[10px] text-slate-600 font-mono truncate max-w-[120px] hidden sm:block">{l.directory}</span>
                                    <Pill status={l.status} />
                                </div>
                            )) : <p className="text-xs text-slate-500">No architecture layers defined</p>}
                        </div>
                    </div>

                    {/* Documentation */}
                    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <FileText className="w-5 h-5 text-cyan-400" />
                            <h2 className="text-lg font-semibold text-white">Documentation</h2>
                            <span className="text-xs text-slate-600 bg-white/[0.04] px-2 py-0.5 rounded-full">{docs.length} docs &middot; avg {avgDocComplete}%</span>
                        </div>
                        <div className="space-y-1.5 max-h-80 overflow-y-auto pr-1">
                            {docs.length > 0 ? docs.map(d => (
                                <div key={d.id} className="flex items-center gap-3 rounded-lg bg-white/[0.02] border border-white/[0.04] px-3 py-2">
                                    <span className="text-[10px] text-slate-500 w-20 shrink-0 capitalize">{d.doc_type_display || d.doc_type}</span>
                                    <span className="text-sm text-slate-300 flex-1 truncate">{d.title}</span>
                                    <div className="w-12 shrink-0"><Bar value={d.completeness} /></div>
                                    <Pill status={d.status} label={d.status_display || d.status} />
                                </div>
                            )) : <p className="text-xs text-slate-500">No docs found</p>}
                        </div>
                    </div>
                </div>

                {/* Tech Debt */}
                <Section title="Technical Debt" icon={AlertTriangle} count={debts.length}>
                    <div className="space-y-2">
                        {debts.length > 0 ? debts.map(d => {
                            const sevColor: Record<string, string> = { critical: 'bg-red-500/10 text-red-400 border-red-500/20', high: 'bg-orange-500/10 text-orange-400 border-orange-500/20', medium: 'bg-amber-500/10 text-amber-400 border-amber-500/20', low: 'bg-slate-500/10 text-slate-400 border-slate-500/20' };
                            return (
                                <div key={d.id} className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-4">
                                    <div className="flex items-start justify-between gap-3">
                                        <div className="flex-1">
                                            <p className="text-sm font-medium text-white">{d.title}</p>
                                            <p className="text-xs text-slate-500 mt-1">{d.impact}</p>
                                        </div>
                                        <div className="flex items-center gap-2 shrink-0">
                                            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${sevColor[d.severity] || sevColor.medium}`}>{d.severity}</span>
                                            <span className="text-[10px] text-slate-600 bg-white/[0.04] px-2 py-0.5 rounded-full">{d.debt_type_display}</span>
                                        </div>
                                    </div>
                                    <p className="text-[10px] text-slate-600 font-mono mt-2">{d.affected_files}</p>
                                </div>
                            );
                        }) : <p className="text-xs text-slate-500">No tech debt items found</p>}
                    </div>
                </Section>

                {/* Business Goals */}
                <Section title="Business Goals (OKRs)" icon={TrendingUp} count={goals.length}>
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                        {goals.length > 0 ? goals.map(g => (
                            <div key={g.id} className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5">
                                <div className="flex items-start justify-between mb-3">
                                    <div>
                                        <p className="text-sm font-semibold text-white">{g.title}</p>
                                        <span className="text-[10px] text-slate-500 capitalize">{g.goal_type_display}</span>
                                    </div>
                                    <span className="text-lg font-bold text-cyan-400">{g.progress_percentage}%</span>
                                </div>
                                <Bar value={g.progress_percentage} />
                                {g.target_metric && (
                                    <div className="flex items-center justify-between mt-3 text-xs text-slate-500">
                                        <span>{g.target_metric}</span>
                                        <span className="font-mono text-white">{g.current_value} / {g.target_value}</span>
                                    </div>
                                )}
                                <div className="mt-3 space-y-1.5">
                                    {g.key_results?.map((kr, i) => (
                                        <div key={i} className="flex items-center gap-2">
                                            {kr.done
                                                ? <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                                                : <Circle className="w-3.5 h-3.5 text-slate-600 shrink-0" />
                                            }
                                            <span className={`text-xs ${kr.done ? 'text-slate-500 line-through' : 'text-slate-300'}`}>{kr.title}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )) : <p className="text-xs text-slate-500">No goals found</p>}
                    </div>
                </Section>

                {/* Category + Priority */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
                        <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-4">Tasks by Category</h3>
                        <div className="space-y-3">
                            {Object.entries(dash.by_category || {}).sort((a, b) => b[1] - a[1]).map(([cat, count]) => {
                                const Icon = CAT_ICON[cat] || Code2; const pct = dash.total_tasks > 0 ? (count / dash.total_tasks) * 100 : 0;
                                return (
                                    <div key={cat} className="flex items-center gap-3">
                                        <div className={`w-7 h-7 rounded-lg bg-gradient-to-br ${CAT_GRAD[cat] || 'from-slate-500 to-slate-600'} flex items-center justify-center`}>
                                            <Icon className="w-3.5 h-3.5 text-white" />
                                        </div>
                                        <div className="flex-1"><div className="flex justify-between mb-1"><span className="text-sm text-slate-300 capitalize">{cat}</span><span className="text-sm font-semibold text-white">{count}</span></div>
                                            <Bar value={pct} gradient={CAT_GRAD[cat]} />
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
                        <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-4">Tasks by Priority</h3>
                        <div className="space-y-4">
                            {[{ k: 'critical', c: 'from-red-500 to-rose-500' }, { k: 'high', c: 'from-orange-500 to-amber-500' }, { k: 'medium', c: 'from-amber-400 to-yellow-500' }, { k: 'low', c: 'from-slate-400 to-slate-500' }].map(({ k, c }) => {
                                const count = dash.by_priority?.[k] || 0; const pct = dash.total_tasks > 0 ? (count / dash.total_tasks) * 100 : 0;
                                return (
                                    <div key={k}><div className="flex justify-between mb-1"><span className="text-sm text-slate-300 capitalize">{k}</span><span className="text-sm font-bold text-white">{count} <span className="text-xs text-slate-600">({pct.toFixed(0)}%)</span></span></div>
                                        <Bar value={pct} gradient={c} />
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </div>

                <div className="text-center pb-4"><p className="text-xs text-slate-600">{phases.length} Phases &middot; {dash.total_tasks} Tasks &middot; {features.length} Features &middot; {layers.length} Arch Layers &middot; {docs.length} Docs &middot; {debts.length} Debts &middot; {goals.length} OKRs</p></div>
            </div>
        </div>
    );
}
