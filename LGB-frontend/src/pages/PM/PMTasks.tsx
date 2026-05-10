import { useState, useCallback } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import {
    CheckCircle2, Circle, Clock, AlertCircle,
    ArrowLeft, Filter, Search, ChevronDown, ChevronUp,
    Brain, Server, Code2, Shield, Layers, FileText,
    TestTube, Gauge, Pause, X, FileCode, Timer, Tag,
    History, RefreshCw, CheckSquare,
} from 'lucide-react';
import { PMService, usePMPolling } from '../../services/pm.api';
import type { PMTask, PMPhase, PMStatusHistory } from '../../services/pm.api';

/* ─── Config ─── */
const STATUS: Record<string, { label: string; icon: typeof Circle; dot: string; text: string }> = {
    not_started: { label: 'Not Started', icon: Circle, dot: 'bg-slate-400', text: 'text-slate-400' },
    in_progress: { label: 'In Progress', icon: Clock, dot: 'bg-blue-400', text: 'text-blue-400' },
    scaffolded: { label: 'Scaffolded', icon: Layers, dot: 'bg-amber-400', text: 'text-amber-400' },
    completed: { label: 'Completed', icon: CheckCircle2, dot: 'bg-emerald-400', text: 'text-emerald-400' },
    blocked: { label: 'Blocked', icon: AlertCircle, dot: 'bg-red-400', text: 'text-red-400' },
    deferred: { label: 'Deferred', icon: Pause, dot: 'bg-purple-400', text: 'text-purple-400' },
};

const PRIORITY: Record<string, { badge: string }> = {
    critical: { badge: 'bg-red-500/10 text-red-400 border-red-500/20' },
    high: { badge: 'bg-orange-500/10 text-orange-400 border-orange-500/20' },
    medium: { badge: 'bg-amber-500/10 text-amber-400 border-amber-500/20' },
    low: { badge: 'bg-slate-500/10 text-slate-400 border-slate-500/20' },
};

const CAT_ICONS: Record<string, typeof Code2> = {
    backend: Server, frontend: Code2, devops: Gauge, ai: Brain,
    docs: FileText, testing: TestTube, security: Shield, infra: Layers,
};

/* ─── Select Component ─── */
function FilterSelect({ value, onChange, label, options }: {
    value: string; onChange: (v: string) => void; label: string;
    options: { value: string; label: string }[];
}) {
    return (
        <div className="relative">
            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="appearance-none pl-3 pr-8 py-2 rounded-xl bg-white/[0.04] border border-white/[0.08] text-sm text-slate-300 focus:outline-none focus:border-cyan-500/40 cursor-pointer hover:bg-white/[0.06] transition-all"
            >
                <option value="">{label}</option>
                {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
            <ChevronDown className="absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-500 pointer-events-none" />
        </div>
    );
}

/* ─── Task Row ─── */
function TaskRow({ task, isExpanded, onToggle, onStatusChange }: {
    task: PMTask; isExpanded: boolean;
    onToggle: () => void; onStatusChange: (id: number, s: string) => void;
}) {
    const st = STATUS[task.status] || STATUS.not_started;
    const pr = PRIORITY[task.priority] || PRIORITY.medium;
    const StatusIcon = st.icon;
    const CatIcon = CAT_ICONS[task.category] || Code2;

    return (
        <div className={`rounded-xl border transition-all duration-200 ${isExpanded ? 'border-cyan-500/20 bg-white/[0.03]' : 'border-white/[0.05] bg-white/[0.015] hover:bg-white/[0.03] hover:border-white/[0.08]'}`}>
            {/* Main Row */}
            <div className="flex items-center gap-3 px-4 py-3.5 cursor-pointer" onClick={onToggle}>
                {/* Status toggle */}
                <button
                    onClick={(e) => { e.stopPropagation(); onStatusChange(task.id, task.status === 'completed' ? 'not_started' : 'completed'); }}
                    className="shrink-0 group/btn"
                >
                    <StatusIcon className={`w-[18px] h-[18px] ${st.text} group-hover/btn:scale-110 transition-transform`} />
                </button>

                {/* Code */}
                <span className="text-[11px] font-mono text-slate-600 w-[72px] shrink-0">{task.task_code}</span>

                {/* Title */}
                <span className={`flex-1 text-sm truncate ${task.status === 'completed' ? 'text-slate-500 line-through' : 'text-slate-200'}`}>
                    {task.title}
                </span>

                {/* Category */}
                <div className="hidden sm:flex items-center gap-1 shrink-0">
                    <CatIcon className="w-3.5 h-3.5 text-slate-500" />
                    <span className="text-[11px] text-slate-500 capitalize">{task.category}</span>
                </div>

                {/* Phase */}
                <span className="text-[11px] text-slate-600 shrink-0 hidden lg:block w-[100px] truncate text-right">
                    {task.phase_name || '—'}
                </span>

                {/* Priority badge */}
                <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border shrink-0 capitalize ${pr.badge}`}>
                    {task.priority || 'medium'}
                </span>

                {/* Hours */}
                {task.estimated_hours && (
                    <span className="text-[11px] text-slate-600 shrink-0 hidden xl:block w-8 text-right">{task.estimated_hours}h</span>
                )}

                {/* Expand */}
                {isExpanded
                    ? <ChevronUp className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                    : <ChevronDown className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                }
            </div>

            {/* Expanded */}
            {isExpanded && (
                <div className="px-4 pb-4 pt-1 border-t border-white/[0.04] space-y-4">
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3">
                        <div className="flex items-start gap-2">
                            <FileCode className="w-4 h-4 text-slate-500 mt-0.5 shrink-0" />
                            <div>
                                <span className="text-[10px] text-slate-600 uppercase tracking-wider block">Target File</span>
                                <span className="text-sm text-cyan-400 font-mono break-all">{task.target_file || '—'}</span>
                            </div>
                        </div>
                        <div className="flex items-start gap-2">
                            <Timer className="w-4 h-4 text-slate-500 mt-0.5 shrink-0" />
                            <div>
                                <span className="text-[10px] text-slate-600 uppercase tracking-wider block">Estimated</span>
                                <span className="text-sm text-white">{task.estimated_hours || '—'} hours</span>
                            </div>
                        </div>
                        <div className="flex items-start gap-2">
                            <Tag className="w-4 h-4 text-slate-500 mt-0.5 shrink-0" />
                            <div>
                                <span className="text-[10px] text-slate-600 uppercase tracking-wider block">Tags</span>
                                <div className="flex gap-1.5 mt-1 flex-wrap">
                                    {task.tags?.length ? task.tags.map(t => (
                                        <span key={t.id} className="text-[10px] px-2 py-0.5 rounded-full border" style={{ backgroundColor: `${t.color}12`, color: t.color, borderColor: `${t.color}30` }}>
                                            {t.name}
                                        </span>
                                    )) : <span className="text-xs text-slate-600">—</span>}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Status Actions */}
                    <div className="flex items-center gap-1.5 flex-wrap pt-1">
                        <span className="text-[10px] text-slate-600 uppercase tracking-wider mr-1">Set status:</span>
                        {Object.entries(STATUS).map(([key, cfg]) => (
                            <button
                                key={key}
                                onClick={() => onStatusChange(task.id, key)}
                                className={`text-[11px] px-2.5 py-1 rounded-lg border transition-all ${task.status === key
                                        ? `bg-white/[0.06] border-white/[0.12] ${cfg.text} font-semibold`
                                        : 'border-white/[0.04] text-slate-600 hover:text-slate-300 hover:bg-white/[0.03]'
                                    }`}
                            >
                                {cfg.label}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default function PMTasks() {
    const [searchParams] = useSearchParams();
    const initialPhase = searchParams.get('phase') || '';

    const [tasks, setTasks] = useState<PMTask[]>([]);
    const [phases, setPhases] = useState<PMPhase[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [fPhase, setFPhase] = useState(initialPhase);
    const [fStatus, setFStatus] = useState('');
    const [fPriority, setFPriority] = useState('');
    const [fCategory, setFCategory] = useState('');
    const [showFilters, setShowFilters] = useState(!!initialPhase);
    const [expanded, setExpanded] = useState<number | null>(null);
    const [selected, setSelected] = useState<Set<number>>(new Set());
    const [bulkStatus, setBulkStatus] = useState('');
    const [bulkLoading, setBulkLoading] = useState(false);
    const [history, setHistory] = useState<PMStatusHistory[]>([]);
    const [historyTaskId, setHistoryTaskId] = useState<number | null>(null);
    const [historyLoading, setHistoryLoading] = useState(false);
    const [lastRefreshed, setLastRefreshed] = useState<Date>(new Date());

    const fetchTasks = useCallback(async () => {
        try {
            setLoading(true);
            const f: Record<string, string | number> = {};
            if (fPhase) f.phase = fPhase;
            if (fStatus) f.status = fStatus;
            if (fPriority) f.priority = fPriority;
            if (fCategory) f.category = fCategory;
            if (search) f.search = search;
            const [t, p] = await Promise.all([
                PMService.listTasks(f),
                phases.length ? Promise.resolve(phases) : PMService.listPhases(),
            ]);
            setTasks(t);
            if (!phases.length) setPhases(p);
            setLastRefreshed(new Date());
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, [fPhase, fStatus, fPriority, fCategory, search]);

    // 30-second auto-refresh
    usePMPolling(fetchTasks, 30_000);

    const handleStatusChange = async (id: number, newStatus: string) => {
        // Optimistic update
        setTasks(prev => prev.map(t => t.id === id ? { ...t, status: newStatus } : t));
        try {
            await PMService.updateTaskStatus(id, newStatus);
            // Refresh history if this task's panel is open
            if (historyTaskId === id) loadHistory(id);
        } catch { fetchTasks(); } // revert on error
    };

    const handleBulkUpdate = async () => {
        if (!bulkStatus || selected.size === 0) return;
        setBulkLoading(true);
        try {
            const result = await PMService.bulkUpdateStatus([...selected], bulkStatus);
            setSelected(new Set());
            setBulkStatus('');
            await fetchTasks();
            console.info(`Bulk: ${result.updated} updated, ${result.skipped} skipped`);
        } catch (err) { console.error(err); }
        finally { setBulkLoading(false); }
    };

    const toggleSelect = (id: number) => setSelected(prev => {
        const next = new Set(prev);
        next.has(id) ? next.delete(id) : next.add(id);
        return next;
    });

    const loadHistory = async (taskId: number) => {
        setHistoryTaskId(taskId);
        setHistoryLoading(true);
        const h = await PMService.getTaskHistory(taskId);
        setHistory(h);
        setHistoryLoading(false);
    };

    const clearAll = () => { setFPhase(''); setFStatus(''); setFPriority(''); setFCategory(''); setSearch(''); };
    const activeCount = [fPhase, fStatus, fPriority, fCategory].filter(Boolean).length;

    // Group by phase
    const grouped = tasks.reduce<Record<string, PMTask[]>>((acc, t) => {
        const key = t.phase_name || 'Ungrouped';
        (acc[key] = acc[key] || []).push(t);
        return acc;
    }, {});

    return (
        <div className="min-h-screen bg-[#0a0a0f] relative overflow-hidden text-left p-4 sm:p-8 w-full">
            {/* BG */}
            <div className="absolute top-0 right-1/4 w-80 h-80 bg-indigo-500/5 rounded-full blur-[100px] pointer-events-none" />

            <div className="relative z-10 max-w-full mx-auto px-4 py-8 sm:px-6">
                {/* Header */}
                <div className="flex items-center gap-3 mb-8">
                    <Link to="/pm">
                        <button className="w-9 h-9 rounded-xl border border-white/[0.08] bg-white/[0.03] flex items-center justify-center text-slate-400 hover:text-white hover:border-white/20 transition-all">
                            <ArrowLeft className="w-4 h-4" />
                        </button>
                    </Link>
                    <div className="flex-1">
                        <h1 className="text-2xl font-bold text-white">Tasks</h1>
                        <p className="text-sm text-slate-500">
                            {tasks.length} tasks{activeCount > 0 ? ' (filtered)' : ''}
                            <span className="ml-3 text-slate-700 text-xs">
                                <RefreshCw className="inline w-3 h-3 mr-1" />
                                {lastRefreshed.toLocaleTimeString()}
                            </span>
                        </p>
                    </div>
                    <button
                        onClick={() => setShowFilters(!showFilters)}
                        className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-sm border transition-all ${showFilters ? 'border-cyan-500/30 text-cyan-400 bg-cyan-500/5' : 'border-white/[0.08] text-slate-400 bg-white/[0.03] hover:text-white'
                            }`}
                    >
                        <Filter className="w-4 h-4" /> Filters
                        {activeCount > 0 && (
                            <span className="w-5 h-5 rounded-full bg-cyan-500/20 text-cyan-400 text-[10px] font-bold flex items-center justify-center">{activeCount}</span>
                        )}
                    </button>
                </div>

                {/* Search */}
                <div className="relative mb-4">
                    <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                    <input
                        type="text" value={search} onChange={e => setSearch(e.target.value)}
                        placeholder="Search by code, title, or file path..."
                        className="w-full pl-10 pr-10 py-3 bg-white/[0.03] border border-white/[0.08] rounded-xl text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-cyan-500/40 focus:ring-1 focus:ring-cyan-500/10 transition-all"
                    />
                    {search && (
                        <button onClick={() => setSearch('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white">
                            <X className="w-4 h-4" />
                        </button>
                    )}
                </div>

                {/* Filters */}
                {showFilters && (
                    <div className="flex items-center gap-2.5 flex-wrap mb-6">
                        <FilterSelect value={fPhase} onChange={setFPhase} label="All Phases"
                            options={phases.map(p => ({ value: String(p.id), label: `P${p.phase_number}: ${p.name}` }))} />
                        <FilterSelect value={fStatus} onChange={setFStatus} label="All Statuses"
                            options={Object.entries(STATUS).map(([k, v]) => ({ value: k, label: v.label }))} />
                        <FilterSelect value={fPriority} onChange={setFPriority} label="All Priorities"
                            options={['critical', 'high', 'medium', 'low'].map(k => ({ value: k, label: k.charAt(0).toUpperCase() + k.slice(1) }))} />
                        <FilterSelect value={fCategory} onChange={setFCategory} label="All Categories"
                            options={Object.keys(CAT_ICONS).map(k => ({ value: k, label: k.charAt(0).toUpperCase() + k.slice(1) }))} />
                        {activeCount > 0 && (
                            <button onClick={clearAll} className="text-xs text-slate-500 hover:text-white px-2 py-1 rounded-lg hover:bg-white/[0.04] transition-all">
                                Clear all
                            </button>
                        )}
                    </div>
                )}

                {/* Bulk Toolbar */}
                {selected.size > 0 && (
                    <div className="flex items-center gap-3 mb-4 px-4 py-3 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
                        <CheckSquare className="w-4 h-4 text-cyan-400" />
                        <span className="text-sm text-cyan-300 font-medium">{selected.size} selected</span>
                        <select
                            value={bulkStatus}
                            onChange={e => setBulkStatus(e.target.value)}
                            className="ml-auto px-3 py-1.5 rounded-lg bg-white/[0.06] border border-white/[0.1] text-sm text-slate-300 focus:outline-none"
                        >
                            <option value="">Set status…</option>
                            {Object.entries(STATUS).map(([k, v]) => <option key={k} value={k}>{v.label}</option>)}
                        </select>
                        <button
                            onClick={handleBulkUpdate}
                            disabled={!bulkStatus || bulkLoading}
                            className="px-3 py-1.5 rounded-lg bg-cyan-500/20 text-cyan-300 text-sm font-medium hover:bg-cyan-500/30 disabled:opacity-40 transition-all"
                        >
                            {bulkLoading ? 'Updating…' : 'Apply'}
                        </button>
                        <button onClick={() => setSelected(new Set())} className="text-slate-500 hover:text-white">
                            <X className="w-4 h-4" />
                        </button>
                    </div>
                )}

                {/* Task List */}
                {loading ? (
                    <div className="space-y-2">
                        {[1,2,3,4,5].map(i => <div key={i} className="h-14 rounded-xl bg-white/[0.02] border border-white/[0.04] animate-pulse" />)}
                    </div>
                ) : tasks.length === 0 ? (
                    <div className="text-center py-20">
                        <Search className="w-10 h-10 text-slate-700 mx-auto mb-4" />
                        <p className="text-slate-500 mb-2">No tasks match your filters</p>
                        <button onClick={clearAll} className="text-sm text-cyan-400 hover:text-cyan-300">Clear filters</button>
                    </div>
                ) : (
                    <div className="flex gap-4">
                        <div className="flex-1 space-y-6">
                            {Object.entries(grouped).map(([phaseName, phaseTasks]) => (
                                <div key={phaseName}>
                                    <div className="flex items-center gap-2 mb-2.5">
                                        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{phaseName}</span>
                                        <span className="text-[10px] text-slate-600 bg-white/[0.04] px-2 py-0.5 rounded-full">{phaseTasks.length}</span>
                                    </div>
                                    <div className="space-y-1.5">
                                        {phaseTasks.map(task => (
                                            <div key={task.id} className="flex items-start gap-2">
                                                <button
                                                    onClick={() => toggleSelect(task.id)}
                                                    className={`mt-3.5 shrink-0 w-4 h-4 rounded border transition-all ${
                                                        selected.has(task.id)
                                                            ? 'bg-cyan-500 border-cyan-500'
                                                            : 'border-white/[0.12] hover:border-cyan-500/50'
                                                    }`}
                                                />
                                                <div className="flex-1">
                                                    <TaskRow
                                                        task={task}
                                                        isExpanded={expanded === task.id}
                                                        onToggle={() => setExpanded(expanded === task.id ? null : task.id)}
                                                        onStatusChange={handleStatusChange}
                                                    />
                                                </div>
                                                <button
                                                    onClick={() => historyTaskId === task.id ? setHistoryTaskId(null) : loadHistory(task.id)}
                                                    title="Status history"
                                                    className={`mt-3 shrink-0 p-1.5 rounded-lg border transition-all ${
                                                        historyTaskId === task.id
                                                            ? 'border-indigo-500/30 text-indigo-400 bg-indigo-500/10'
                                                            : 'border-white/[0.06] text-slate-600 hover:text-slate-300'
                                                    }`}
                                                >
                                                    <History className="w-3.5 h-3.5" />
                                                </button>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* History Sidebar */}
                        {historyTaskId !== null && (
                            <div className="w-72 shrink-0">
                                <div className="sticky top-6 rounded-xl border border-white/[0.08] bg-white/[0.02] p-4">
                                    <div className="flex items-center justify-between mb-4">
                                        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                                            <History className="w-3.5 h-3.5" /> Status History
                                        </span>
                                        <button onClick={() => setHistoryTaskId(null)} className="text-slate-600 hover:text-white">
                                            <X className="w-3.5 h-3.5" />
                                        </button>
                                    </div>
                                    {historyLoading ? (
                                        <div className="space-y-2">
                                            {[1,2,3].map(i => <div key={i} className="h-10 rounded-lg bg-white/[0.03] animate-pulse" />)}
                                        </div>
                                    ) : history.length === 0 ? (
                                        <p className="text-xs text-slate-600">No history yet.</p>
                                    ) : (
                                        <div className="relative pl-4">
                                            <div className="absolute left-1.5 top-0 bottom-0 w-px bg-white/[0.06]" />
                                            <div className="space-y-4">
                                                {history.map(h => (
                                                    <div key={h.id} className="relative">
                                                        <div className="absolute -left-[11px] top-1 w-2 h-2 rounded-full bg-slate-700 border border-slate-600" />
                                                        <div className="text-[10px] text-slate-600 mb-0.5">
                                                            {new Date(h.changed_at).toLocaleString('en-IN', { dateStyle: 'short', timeStyle: 'short' })}
                                                            {' · '}{h.changed_by_name}
                                                        </div>
                                                        <div className="flex items-center gap-1.5 flex-wrap">
                                                            <span className="text-[11px] text-slate-500">{h.from_status || 'created'}</span>
                                                            <span className="text-[10px] text-slate-700">→</span>
                                                            <span className="text-[11px] font-semibold text-cyan-400">{h.to_status}</span>
                                                        </div>
                                                        {h.note && <p className="text-[10px] text-slate-600 mt-0.5 italic">{h.note}</p>}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
