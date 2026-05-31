"use client";

import { CircleMarker, MapContainer, Popup, TileLayer } from "react-leaflet";

const regions = [
  { code: "BR-PAT", name: "Patna", lat: 25.5941, lng: 85.1376, risk: 86 },
  { code: "RJ-JAI", name: "Jaipur", lat: 26.9124, lng: 75.7873, risk: 74 },
  { code: "DL-NDL", name: "New Delhi", lat: 28.6139, lng: 77.209, risk: 72 },
  { code: "AS-GUW", name: "Kamrup Metro", lat: 26.1445, lng: 91.7362, risk: 69 },
  { code: "MH-MUM", name: "Mumbai", lat: 19.076, lng: 72.8777, risk: 58 },
  { code: "KA-BLR", name: "Bengaluru Urban", lat: 12.9716, lng: 77.5946, risk: 41 },
  { code: "TN-CHE", name: "Chennai", lat: 13.0827, lng: 80.2707, risk: 39 }
];

function color(risk: number) {
  if (risk >= 80) return "#ef4444";
  if (risk >= 60) return "#f97316";
  return "#2dd4bf";
}

export default function IndiaRiskMap() {
  return (
    <MapContainer center={[22.6, 79.2]} zoom={5} scrollWheelZoom={false}>
      <TileLayer attribution="&copy; OpenStreetMap" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {regions.map((region) => (
        <CircleMarker
          key={region.code}
          center={[region.lat, region.lng]}
          pathOptions={{ color: color(region.risk), fillColor: color(region.risk), fillOpacity: 0.55 }}
          radius={Math.max(8, region.risk / 5)}
        >
          <Popup>
            <strong>{region.name}</strong>
            <br />
            {region.code} risk score: {region.risk}
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
