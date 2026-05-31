export const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "https://crisisiq-backend.vercel.app/api/v1";

export type Severity = "critical" | "high" | "moderate" | "low";

export type RealtimeCity = {
  code: string;
  city: string;
  state: string;
  latitude: number;
  longitude: number;
  population_millions: number;
  risk_score: number;
  probability: number;
  severity: Severity;
  category: string;
  drivers: Record<string, number>;
  recommendation: {
    region_code: string;
    category: string;
    severity_score: number;
    actions: string[];
    rationale: string;
  };
  features: Record<string, number | string>;
  live: {
    weather: {
      available: boolean;
      temperature_c: number | null;
      humidity_pct: number | null;
      rainfall_mm: number | null;
      wind_kph: number | null;
      rainfall_deviation: number;
      heatwave_days: number;
      provider?: string;
    };
    news: {
      available: boolean;
      article_count: number;
      sentiment: number;
      provider?: string;
      headlines: Array<{ title: string; domain: string; published_at: string | null; score: number }>;
    };
  };
  sources: string[];
  updated_at: string;
};

export async function api<T>(path: string, token: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store"
  });
  if (!response.ok) throw new Error(`API ${response.status}: ${await response.text()}`);
  return response.json();
}

export async function loginDemo(): Promise<string> {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "admin@crisisiq.ai", password: "CrisisIQ@123" }),
    cache: "no-store"
  });
  if (!response.ok) throw new Error(`Login failed: ${response.status}`);
  const body = (await response.json()) as { access_token: string };
  return body.access_token;
}

export const demoTokenHint = "Login with admin@crisisiq.ai / CrisisIQ@123";
