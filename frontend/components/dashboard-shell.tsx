"use client";

import dynamic from "next/dynamic";
import { useEffect, useMemo, useState } from "react";
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
  Loader2,
  Map,
  Moon,
  Play,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  Sun,
  X
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

import { api, loginDemo, type RealtimeCity, type Severity } from "@/lib/api";

const IndiaRiskMap = dynamic(() => import("./india-risk-map"), { ssr: false });

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

const severityColors: Record<Severity, string> = {
  critical: "text-red-200 bg-red-500/20",
  high: "text-orange-200 bg-orange-500/20",
  moderate: "text-amber-100 bg-amber-500/20",
  low: "text-teal-100 bg-teal-500/20"
};

export function DashboardShell() {
  const [token, setToken] = useState<string | null>(null);
  const [cities, setCities] = useState<RealtimeCity[]>([]);
  const [query, setQuery] = useState("");
  const [showSearch, setShowSearch] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [severityFilter, setSeverityFilter] = useState<"all" | Severity>("all");
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dark, setDark] = useState(true);
  const [updatedAt, setUpdatedAt] = useState<string | null>(null);

  async function loadLiveData(existingToken?: string) {
    setError(null);
    setRefreshing(true);
    try {
      const activeToken = existingToken ?? token ?? (await loginDemo());
      if (!token) setToken(activeToken);
      const rows = await api<RealtimeCity[]>("/realtime/risk/top50?limit=50", activeToken);
      setCities(rows);
      setUpdatedAt(new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load live city risk data");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    loginDemo()
      .then((newToken) => {
        setToken(newToken);
        return loadLiveData(newToken);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Unable to authenticate with CrisisIQ API");
        setLoading(false);
        setRefreshing(false);
      });
    const interval = window.setInterval(() => loadLiveData(), 300000);
    return () => window.clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  const filteredCities = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    return cities
      .filter((city) => severityFilter === "all" || city.severity === severityFilter)
      .filter((city) => {
        if (!normalized) return true;
        return [city.city, city.state, city.code, city.category, city.severity].some((value) =>
          String(value).toLowerCase().includes(normalized)
        );
      })
      .sort((a, b) => b.risk_score - a.risk_score);
  }, [cities, query, severityFilter]);

  const topCities = filteredCities.slice(0, 10);
  const averageRisk = cities.length ? cities.reduce((sum, city) => sum + city.risk_score, 0) / cities.length : 0;
  const criticalCount = cities.filter((city) => city.severity === "critical").length;
  const newsEnabled = cities.filter((city) => city.live.news.available).length;
  const weatherEnabled = cities.filter((city) => city.live.weather.available).length;
  const highest = topCities[0];

  const kpis = [
    { label: "National Risk", value: averageRisk.toFixed(1), delta: highest ? `${highest.city} leads` : "loading", icon: Activity },
    { label: "Cities Monitored", value: String(cities.length || 50), delta: "top 50 India", icon: Map },
    { label: "Critical Alerts", value: String(criticalCount), delta: `${topCities.length} visible`, icon: Bell },
    { label: "Live Feeds", value: `${weatherEnabled}/${newsEnabled}`, delta: "weather/news", icon: ShieldCheck }
  ];

  const trend = topCities.slice(0, 6).map((city) => ({
    month: city.city.split(" ")[0],
    risk: Math.round(city.risk_score),
    forecast: Math.min(100, Math.round(city.risk_score + Math.max(2, city.live.weather.heatwave_days * 4)))
  }));

  const driverAverages = useMemo(() => {
    const keys = ["employment_stress", "price_pressure", "public_safety", "climate_anomaly", "sentiment_distress"];
    return keys.map((key) => ({
      name: key.replace("_stress", "").replace("_anomaly", "").replace("_distress", "").replace("_", " "),
      value: Math.round((cities.reduce((sum, city) => sum + (city.drivers[key] ?? 0), 0) / Math.max(cities.length, 1)) * 100)
    }));
  }, [cities]);

  const shap = highest
    ? Object.entries(highest.drivers)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([feature, impact]) => ({ feature: feature.replaceAll("_", " "), impact }))
    : [];

  function exportCsv() {
    const rows = filteredCities.map((city) => ({
      code: city.code,
      city: city.city,
      state: city.state,
      risk_score: city.risk_score,
      severity: city.severity,
      category: city.category,
      temperature_c: city.live.weather.temperature_c ?? "",
      rainfall_mm: city.live.weather.rainfall_mm ?? "",
      news_sentiment: city.live.news.sentiment,
      updated_at: city.updated_at
    }));
    const header = Object.keys(rows[0] ?? { code: "", city: "", state: "", risk_score: "" });
    const csv = [header.join(","), ...rows.map((row) => header.map((key) => JSON.stringify(row[key as keyof typeof row] ?? "")).join(","))].join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `crisisiq-live-cities-${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <main className={dark ? "min-h-screen" : "min-h-screen bg-slate-100 text-slate-950"}>
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
          <header className="mb-5 flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.18em] text-signal">Operational intelligence</p>
              <h2 className="text-3xl font-semibold">Socio-economic crisis command center</h2>
              <p className="mt-2 text-sm text-slate-400">
                Live top-50 Indian city risk from weather, news sentiment, and socio-economic baselines.
                {updatedAt ? ` Last updated ${updatedAt}.` : ""}
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              {showSearch && (
                <div className="glass flex items-center gap-2 px-3 py-2">
                  <Search className="h-4 w-4 text-slate-400" />
                  <input
                    className="w-44 bg-transparent text-sm outline-none placeholder:text-slate-500"
                    placeholder="City, state, category"
                    value={query}
                    onChange={(event) => setQuery(event.target.value)}
                    autoFocus
                  />
                  <button aria-label="Clear search" onClick={() => setQuery("")}>
                    <X className="h-4 w-4 text-slate-400" />
                  </button>
                </div>
              )}
              <button className="glass flex items-center gap-2 px-3 py-2 text-sm" onClick={() => setShowSearch((value) => !value)}>
                <Search className="h-4 w-4" />Search
              </button>
              <button className="glass flex items-center gap-2 px-3 py-2 text-sm" onClick={() => setShowFilters((value) => !value)}>
                <Filter className="h-4 w-4" />Filters
              </button>
              <button className="glass flex items-center gap-2 px-3 py-2 text-sm" onClick={exportCsv} disabled={!filteredCities.length}>
                <Download className="h-4 w-4" />Export
              </button>
              <button className="glass flex items-center gap-2 px-3 py-2 text-sm" onClick={() => loadLiveData()} disabled={refreshing}>
                {refreshing ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}Refresh
              </button>
              <button className="glass px-3 py-2" aria-label="Toggle theme" onClick={() => setDark((value) => !value)}>
                {dark ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
              </button>
            </div>
          </header>

          {showFilters && (
            <section className="glass mb-4 flex flex-wrap items-center gap-2 p-3">
              {(["all", "critical", "high", "moderate", "low"] as const).map((severity) => (
                <button
                  key={severity}
                  className={`rounded-md px-3 py-2 text-sm ${severityFilter === severity ? "bg-signal text-ink" : "bg-white/10 text-slate-200"}`}
                  onClick={() => setSeverityFilter(severity)}
                >
                  {severity}
                </button>
              ))}
            </section>
          )}

          {error && <div className="glass mb-4 border-red-500/40 p-3 text-sm text-red-100">{error}</div>}

          <section id="overview" className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {kpis.map(({ label, value, delta, icon: Icon }) => (
              <article key={label} className="glass p-4">
                <div className="mb-4 flex items-center justify-between">
                  <p className="text-sm text-slate-300">{label}</p>
                  <Icon className="h-5 w-5 text-signal" />
                </div>
                <div className="text-3xl font-semibold">{loading ? "..." : value}</div>
                <p className="mt-1 text-xs text-slate-400">{delta}</p>
              </article>
            ))}
          </section>

          <section className="mt-4 grid gap-4 xl:grid-cols-[1.2fr_.8fr]">
            <article id="state-heatmaps" className="glass p-4">
              <div className="mb-3 flex items-center justify-between">
                <h3 className="font-semibold">India Top-50 Risk Heatmap</h3>
                <span className="rounded bg-danger/20 px-2 py-1 text-xs text-red-200">{filteredCities.length} live markers</span>
              </div>
              <IndiaRiskMap regions={filteredCities} />
            </article>
            <article id="prediction-analytics" className="glass p-4">
              <h3 className="mb-3 font-semibold">Highest Risk City Forecast</h3>
              <ResponsiveContainer width="100%" height={360}>
                <AreaChart data={trend}>
                  <defs>
                    <linearGradient id="risk" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="5%" stopColor="#f97316" stopOpacity={0.7} />
                      <stop offset="95%" stopColor="#f97316" stopOpacity={0.05} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(255,255,255,.1)" />
                  <XAxis dataKey="month" stroke="#94a3b8" tick={{ fontSize: 11 }} />
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
              <h3 className="mb-3 font-semibold">Top Driver Impact {highest ? `· ${highest.city}` : ""}</h3>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={shap} layout="vertical">
                  <XAxis type="number" stroke="#94a3b8" />
                  <YAxis dataKey="feature" type="category" stroke="#94a3b8" width={135} tick={{ fontSize: 11 }} />
                  <Tooltip contentStyle={{ background: "#101418", border: "1px solid rgba(255,255,255,.14)" }} />
                  <Bar dataKey="impact" fill="#2dd4bf" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </article>
            <article className="glass p-4">
              <h3 className="mb-3 font-semibold">Average Crisis Drivers</h3>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={driverAverages}>
                  <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip contentStyle={{ background: "#101418", border: "1px solid rgba(255,255,255,.14)" }} />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {driverAverages.map((_, i) => <Cell key={i} fill={["#2dd4bf", "#f59e0b", "#ef4444", "#38bdf8", "#a3e635"][i]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </article>
            <article className="glass p-4">
              <h3 className="mb-3 font-semibold">Top Risk Cities</h3>
              <div className="max-h-[260px] space-y-3 overflow-auto pr-1">
                {topCities.map((city) => (
                  <div key={city.code} className="rounded-md border border-line bg-white/5 p-3">
                    <div className="flex items-center justify-between gap-3">
                      <span className="font-medium">{city.city}</span>
                      <span className="text-lg font-semibold">{city.risk_score.toFixed(1)}</span>
                    </div>
                    <p className="text-xs text-slate-400">{city.code} · {city.state} · {city.category}</p>
                    <span className={`mt-2 inline-flex rounded px-2 py-1 text-xs ${severityColors[city.severity]}`}>{city.severity}</span>
                  </div>
                ))}
              </div>
            </article>
          </section>

          <section className="mt-4 grid gap-4 xl:grid-cols-3">
            <Panel title="Pipeline Monitor" id="pipeline-monitor" items={[`Open-Meteo weather ${weatherEnabled}/50`, `News sentiment ${newsEnabled}/50`, `Auto-refresh every 5 min`]} />
            <Panel title="Alerts" id="alerts" items={topCities.slice(0, 3).map((city) => `${city.severity.toUpperCase()} risk in ${city.city}: ${city.risk_score.toFixed(1)}`)} />
            <RecommendationsPanel cities={topCities.slice(0, 3)} />
          </section>

          <section id="ai-assistant" className="glass mt-4 p-4">
            <div className="mb-3 flex items-center gap-2"><Bot className="h-5 w-5 text-signal" /><h3 className="font-semibold">AI Scenario Assistant</h3></div>
            <div className="grid gap-3 lg:grid-cols-[1fr_auto]">
              <input className="rounded-md border border-line bg-white/10 px-4 py-3 outline-none" defaultValue={highest ? `Simulate additional heatwave stress for ${highest.city}` : "Simulate a 20% rainfall deficit in Rajasthan"} />
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
        {items.length ? items.map((item) => (
          <div key={item} className="rounded-md border border-line bg-white/5 px-3 py-2 text-sm text-slate-200">{item}</div>
        )) : <div className="rounded-md border border-line bg-white/5 px-3 py-2 text-sm text-slate-400">Loading live data...</div>}
      </div>
    </article>
  );
}

function RecommendationsPanel({ cities }: { cities: RealtimeCity[] }) {
  return (
    <article id="recommendations" className="glass p-4">
      <h3 className="mb-3 font-semibold">Recommendations</h3>
      <div className="max-h-[300px] space-y-3 overflow-auto pr-1">
        {cities.length ? cities.map((city) => (
          <div key={city.code} className="rounded-md border border-line bg-white/5 p-3">
            <div className="mb-1 flex items-center justify-between gap-3">
              <span className="font-medium">{city.city}</span>
              <span className="text-xs text-slate-400">{city.category}</span>
            </div>
            <p className="mb-2 text-xs text-slate-400">{city.recommendation.rationale}</p>
            {city.recommendation.actions.slice(0, 2).map((action) => (
              <div key={action} className="mb-1 rounded bg-white/5 px-2 py-1 text-xs text-slate-200">{action}</div>
            ))}
          </div>
        )) : <div className="rounded-md border border-line bg-white/5 px-3 py-2 text-sm text-slate-400">Loading live recommendations...</div>}
      </div>
    </article>
  );
}
