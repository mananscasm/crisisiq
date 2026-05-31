import { ShieldCheck } from "lucide-react";
import Link from "next/link";

export default function LoginPage() {
  return (
    <main className="grid min-h-screen place-items-center px-4">
      <section className="glass w-full max-w-md p-8">
        <div className="mb-8 flex items-center gap-3">
          <ShieldCheck className="h-9 w-9 text-signal" />
          <div>
            <h1 className="text-2xl font-semibold">CrisisIQ</h1>
            <p className="text-sm text-slate-300">Secure analyst console</p>
          </div>
        </div>
        <form className="space-y-4">
          <input className="w-full rounded-md border border-line bg-white/10 px-4 py-3 outline-none" defaultValue="admin@crisisiq.ai" />
          <input className="w-full rounded-md border border-line bg-white/10 px-4 py-3 outline-none" defaultValue="CrisisIQ@123" type="password" />
          <Link href="/" className="block rounded-md bg-signal px-4 py-3 text-center font-semibold text-ink">
            Sign in
          </Link>
        </form>
      </section>
    </main>
  );
}
