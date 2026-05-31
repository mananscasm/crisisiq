import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CrisisIQ",
  description: "AI-driven socio-economic crisis prediction across Indian regions"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
