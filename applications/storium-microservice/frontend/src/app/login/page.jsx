"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setErr(null);
    try {
      await login(username, password);
      router.push("/");
    } catch (ex) {
      setErr(ex.message);
    }
  }

  return (
    <div style={{ maxWidth: 360 }}>
      <h1>Giriş</h1>
      <form onSubmit={onSubmit} style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <label>
          Kullanıcı adı
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />
        </label>
        <label>
          Parola
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />
        </label>
        {err ? <p style={{ color: "crimson" }}>{err}</p> : null}
        <button type="submit" className="primary">
          Giriş
        </button>
      </form>
      <p>
        Hesabınız yok mu? <Link href="/register">Kayıt olun</Link>
      </p>
    </div>
  );
}
