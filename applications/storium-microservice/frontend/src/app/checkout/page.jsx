"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { useCartId } from "@/context/CartIdContext";
import { useCartUi } from "@/context/CartUiContext";

export default function CheckoutPage() {
  const { token } = useAuth();
  const { cartId, resetCartId } = useCartId();
  const { setCartCount } = useCartUi();
  const router = useRouter();
  const [form, setForm] = useState({
    shipping_name: "",
    shipping_address: "",
    shipping_city: "",
    shipping_phone: "",
    notes: "",
  });
  const [err, setErr] = useState(null);

  if (!token) {
    return (
      <p>
        <Link href="/login">Giriş yapın</Link>.
      </p>
    );
  }

  async function onSubmit(e) {
    e.preventDefault();
    setErr(null);
    try {
      await api("/api/orders/checkout", {
        method: "POST",
        token,
        headers: { "X-Cart-Id": cartId },
        body: form,
      });
      resetCartId();
      setCartCount(0);
      router.push("/orders");
    } catch (ex) {
      setErr(ex.message);
    }
  }

  return (
    <div style={{ maxWidth: 480 }}>
      <h1>Teslimat</h1>
      <form onSubmit={onSubmit} style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <label>
          Ad Soyad
          <input
            value={form.shipping_name}
            onChange={(e) => setForm({ ...form, shipping_name: e.target.value })}
            required
          />
        </label>
        <label>
          Adres
          <textarea
            value={form.shipping_address}
            onChange={(e) => setForm({ ...form, shipping_address: e.target.value })}
            required
            rows={3}
          />
        </label>
        <label>
          Şehir
          <input
            value={form.shipping_city}
            onChange={(e) => setForm({ ...form, shipping_city: e.target.value })}
            required
          />
        </label>
        <label>
          Telefon
          <input
            value={form.shipping_phone}
            onChange={(e) => setForm({ ...form, shipping_phone: e.target.value })}
          />
        </label>
        <label>
          Not
          <input value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        </label>
        {err ? <p style={{ color: "crimson" }}>{err}</p> : null}
        <button type="submit" className="primary">
          Siparişi onayla
        </button>
      </form>
    </div>
  );
}
