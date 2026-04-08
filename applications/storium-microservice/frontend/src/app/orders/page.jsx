"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

export default function OrdersPage() {
  const { token } = useAuth();
  const [orders, setOrders] = useState([]);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!token) return;
    let c = false;
    (async () => {
      try {
        const list = await api("/api/orders", { token });
        if (!c) setOrders(list);
      } catch (e) {
        if (!c) setErr(e.message);
      }
    })();
    return () => {
      c = true;
    };
  }, [token]);

  if (!token) {
    return (
      <p>
        <Link href="/login">Giriş yapın</Link>.
      </p>
    );
  }
  if (err) return <p style={{ color: "crimson" }}>{err}</p>;

  return (
    <div>
      <h1>Siparişlerim</h1>
      {!orders.length ? <p>Henüz sipariş yok.</p> : null}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {orders.map((o) => (
          <li key={o.id} className="card" style={{ marginBottom: "0.75rem" }}>
            <strong>#{o.id}</strong> — {o.status_display} — {o.total_price} ₺
            <div style={{ fontSize: "0.9rem", color: "#444" }}>{o.created_at}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
