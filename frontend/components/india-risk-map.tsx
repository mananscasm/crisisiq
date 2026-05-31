"use client";

import { CircleMarker, MapContainer, Popup, TileLayer } from "react-leaflet";
import type { RealtimeCity } from "@/lib/api";

type RiskMarker = Pick<RealtimeCity, "code" | "city" | "state" | "latitude" | "longitude" | "risk_score" | "severity" | "category">;

function color(risk: number) {
  if (risk >= 80) return "#ef4444";
  if (risk >= 60) return "#f97316";
  return "#2dd4bf";
}

export default function IndiaRiskMap({ regions }: { regions: RiskMarker[] }) {
  return (
    <MapContainer center={[22.6, 79.2]} zoom={5} scrollWheelZoom={false}>
      <TileLayer attribution="&copy; OpenStreetMap" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {regions.map((region) => (
        <CircleMarker
          key={region.code}
          center={[region.latitude, region.longitude]}
          pathOptions={{ color: color(region.risk_score), fillColor: color(region.risk_score), fillOpacity: 0.55 }}
          radius={Math.max(7, region.risk_score / 6)}
        >
          <Popup>
            <strong>{region.city}</strong>
            <br />
            {region.state} · {region.code}
            <br />
            Risk score: {region.risk_score}
            <br />
            {region.severity} · {region.category}
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
