"use client";

import dynamic from "next/dynamic";
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bell,
  Bot,
  DatabaseZap,
  Download,
  FileText,
  Filter,
  LineChart,
  Map,
  Moon,
  Play,
  Search,
  ShieldCheck,
  Sparkles
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

const IndiaRiskMap = dynamic(() => import("./india-risk-map"), { ssr: false });

const kpis = [
  { label: "National Risk", value: "67.4", delta: "+4.2", icon: Activity },
  { label: "Regions Monitored", value: "742", delta: "28 states", icon: Map },
  { label: "Critical Alerts", value: "18", delta: "+6 today", icon: Bell },
  { label: "Model ROC-AUC", value: "0.954", delta: "XGBoost", icon: ShieldCheck }
];

const trend = [
  { month: "Jan", risk: 42, forecast: 45 },
  { month: "Feb", risk: 46, forecast: 49 },
  { month: "Mar", risk: 51, forecast: 53 },
  { month: "Apr", risk: 58, forecast: 61 },
  { month: "May", risk: 63, forecast: 66 },
  { month: "Jun", risk: 67, forecast: 70 }
];

const drivers = [
  { name: "Employment", value: 78 },
  { name: "Inflation", value: 66 },
  { name: "Crime", value: 71 },
  { name: "Climate", value: 84 },
  { name: "Sentiment", value: 62 }
];

const topRegions = [
  ["BR-PAT", "Patna", "critical", 86],
  ["RJ-JAI", "Jaipur", "high", 74],
  ["DL-NDL", "New Delhi", "high", 72],
  ["AS-GUW", "Kamrup Metro", "high", 69],
  ["MH-MUM", "Mumbai", "moderate", 58]
];

const shap = [
  { feature: "rainfall deviation", impact: 0.21 },
  { feature: "crime rate", impact: 0.18 },
  { feature: "unemployment", impact: 0.17 },
  { feature: "social sentiment", impact: 0.14 },
  { feature: "poverty", impact: 0.11 }
];

const navItems: Array<[string, LucideIcon]> = [
  ["Overview", BarChart3],
  ["State Heatmaps", Map],
  ["Prediction Analytics", LineChart],
  ["ML Insights", Sparkles],
  ["Pipeline Monitor", DatabaseZap],
  ["Alerts", AlertTriangle],
  ["Recommendations", FileText],
  ["AI Assistant", Bot]
];

export function DashboardShell() {
  return (
    <main className="min-h-screen">
      <div className="flex min-h-screen">
        <aside className="hidden w-72 shrink-0 border-r border-line bg-ink/80 p-5 backdrop-blur md:block">
          <div className="mb-8 flex items-center gap-3">
            <ShieldCheck className="h-9 w-9 text-signal" />
            <div>
              <h1 className="text-xl font-semibold">CrisisIQ</h1>
              <p className="text-xs text-slate-400">India crisis intelligence</p>
            </div>
          </div>
          <nav className="space-y-1 text-sm">
            {navItems.map(([label, Icon]) => (
              <a key={label} className="flex items-center gap-3 rounded-md px-3 py-2 text-slate-300 hover:bg-white/10" href={`#${label.toLowerCase().replaceAll(" ", "-")}`}>
                <Icon className="h-4 w-4" />
                {label}
              </a>
            ))}
          </nav>
        </aside>

        <section className="flex-1 p-4 lg:p-6">
          <header className="mb-5 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.18em] text-signal">Operational intelligence</p>
              <h2 className="text-3xl font-semibold">Socio-economic crisis command center</h2>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <button className="glass flex items-center gap-2 px-3 py-2 text-sm"><Search className="h-4 w-4" />Search</button>
              <button className="glass flex items-center gap-2 px-3 py-2 text-sm"><Filter className="h-4 w-4" />Filters</button>
              <button className="glass flex items-center gap-2 px-3 py-2 text-sm"><Download className="h-4 w-4" />Export</button>
              <button className="glass px-3 py-2" aria-label="Toggle dark mode"><Moon className="h-4 w-4" /></button>
            </div>
          </header>

          <section id="overview" className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {kpis.map(({ label, value, delta, icon: Icon }) => (
              <article key={label} className="glass p-4">
                <div className="mb-4 flex items-center justify-between">
                  <p className="text-sm text-slate-300">{label}</p>
                  <Icon className="h-5 w-5 text-signal" />
                </div>
                <div className="text-3xl font-semibold">{value}</div>
                <p className="mt-1 text-xs text-slate-400">{delta}</p>
              </article>
            ))}
          </section>

          <section className="mt-4 grid gap-4 xl:grid-cols-[1.2fr_.8fr]">
            <article id="state-heatmaps" className="glass p-4">
              <div className="mb-3 flex items-center justify-between">
                <h3 className="font-semibold">India Risk Heatmap</h3>
                <span className="rounded bg-danger/20 px-2 py-1 text-xs text-red-200">live markers</span>
              </div>
              <IndiaRiskMap />
            </article>
            <article id="prediction-analytics" className="glass p-4">
              <h3 className="mb-3 font-semibold">Risk Forecast</h3>
              <ResponsiveContainer width="100%" height={360}>
                <AreaChart data={trend}>
                  <defs>
                    <linearGradient id="risk" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="5%" stopColor="#f97316" stopOpacity={0.7} />
                      <stop offset="95%" stopColor="#f97316" stopOpacity={0.05} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(255,255,255,.1)" />
                  <XAxis dataKey="month" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip contentStyle={{ background: "#101418", border: "1px solid rgba(255,255,255,.14)" }} />
                  <Area dataKey="risk" stroke="#f97316" fill="url(#risk)" />
                  <Line dataKey="forecast" stroke="#2dd4bf" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </article>
          </section>

          <section className="mt-4 grid gap-4 xl:grid-cols-3">
            <article id="ml-insights" className="glass p-4">
              <h3 className="mb-3 font-semibold">SHAP Driver Impact</h3>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={shap} layout="vertical">
                  <XAxis type="number" stroke="#94a3b8" />
                  <YAxis dataKey="feature" type="category" stroke="#94a3b8" width={120} />
                  <Tooltip contentStyle={{ background: "#101418", border: "1px solid rgba(255,255,255,.14)" }} />
                  <Bar dataKey="impact" fill="#2dd4bf" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </article>
            <article className="glass p-4">
              <h3 className="mb-3 font-semibold">Crisis Drivers</h3>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={drivers}>
                  <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip contentStyle={{ background: "#101418", border: "1px solid rgba(255,255,255,.14)" }} />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {drivers.map((_, i) => <Cell key={i} fill={["#2dd4bf", "#f59e0b", "#ef4444", "#38bdf8", "#a3e635"][i]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </article>
            <article className="glass p-4">
              <h3 className="mb-3 font-semibold">Top Risk Regions</h3>
              <div className="space-y-3">
                {topRegions.map(([code, name, severity, score]) => (
                  <div key={code} className="rounded-md border border-line bg-white/5 p-3">
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{name}</span>
                      <span className="text-lg font-semibold">{score}</span>
                    </div>
                    <p className="text-xs text-slate-400">{code} · {severity}</p>
                  </div>
                ))}
              </div>
            </article>
          </section>

          <section className="mt-4 grid gap-4 xl:grid-cols-3">
            <Panel title="Pipeline Monitor" id="pipeline-monitor" items={["census_ingestion success", "weather_features success", "sentiment_stream running"]} />
            <Panel title="Alerts" id="alerts" items={["Critical risk in Patna", "High climate anomaly in Jaipur", "Sentiment deterioration in New Delhi"]} />
            <Panel title="Recommendations" id="recommendations" items={["Water and heat shelters", "Skill cohorts and MSME credit", "Hotspot policing and field verification"]} />
          </section>

          <section id="ai-assistant" className="glass mt-4 p-4">
            <div className="mb-3 flex items-center gap-2"><Bot className="h-5 w-5 text-signal" /><h3 className="font-semibold">AI Scenario Assistant</h3></div>
            <div className="grid gap-3 lg:grid-cols-[1fr_auto]">
              <input className="rounded-md border border-line bg-white/10 px-4 py-3 outline-none" defaultValue="Simulate a 20% rainfall deficit and 3 point unemployment increase in Rajasthan" />
              <button className="flex items-center justify-center gap-2 rounded-md bg-signal px-4 py-3 font-semibold text-ink"><Play className="h-4 w-4" />Run simulation</button>
            </div>
          </section>
        </section>
      </div>
    </main>
  );
}

function Panel({ title, id, items }: { title: string; id: string; items: string[] }) {
  return (
    <article id={id} className="glass p-4">
      <h3 className="mb-3 font-semibold">{title}</h3>
      <div className="space-y-2">
        {items.map((item) => (
          <div key={item} className="rounded-md border border-line bg-white/5 px-3 py-2 text-sm text-slate-200">{item}</div>
        ))}
      </div>
    </article>
  );
}
