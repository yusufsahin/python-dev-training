"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/context/AuthContext";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setErr(null);
    try {
      await register({ email, username, password });
      router.push("/");
    } catch (ex) {
      setErr(ex.message);
    }
  }

  return (
    <div style={{ maxWidth: 360 }}>
      <h1>Kayıt</h1>
      <form onSubmit={onSubmit} style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <label>
          E-posta
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>
          Kullanıcı adı
          <input value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label>
          Parola (en az 8 karakter)
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        {err ? <p style={{ color: "crimson" }}>{err}</p> : null}
        <button type="submit" className="primary">
          Kayıt ol
        </button>
      </form>
      <p>
        Zaten hesabınız var mı? <Link href="/login">Giriş</Link>
      </p>
    </div>
  );
}
