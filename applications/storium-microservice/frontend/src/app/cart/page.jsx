"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { useCartId } from "@/context/CartIdContext";
import { useCartUi } from "@/context/CartUiContext";

export default function CartPage() {
  const { cartId } = useCartId();
  const { token } = useAuth();
  const { refreshCartCount } = useCartUi();
  const [cart, setCart] = useState(null);
  const [err, setErr] = useState(null);

  const load = useCallback(async () => {
    if (!cartId) return;
    setErr(null);
    try {
      const c = await api("/api/cart", { headers: { "X-Cart-Id": cartId } });
      setCart(c);
      await refreshCartCount();
    } catch (e) {
      setErr(e.message);
    }
  }, [cartId, refreshCartCount]);

  useEffect(() => {
    load();
  }, [load]);

  async function setQty(productId, quantity) {
    await api(`/api/cart/items/${productId}?quantity=${quantity}`, {
      method: "PATCH",
      headers: { "X-Cart-Id": cartId },
    });
    await load();
  }

  async function remove(productId) {
    await api(`/api/cart/items/${productId}`, {
      method: "DELETE",
      headers: { "X-Cart-Id": cartId },
    });
    await load();
  }

  if (!cartId) return <p>Yükleniyor…</p>;
  if (err) return <p style={{ color: "crimson" }}>{err}</p>;
  if (!cart) return <p>Yükleniyor…</p>;

  return (
    <div>
      <h1>Sepet</h1>
      {!cart.items.length ? (
        <p>
          Sepet boş.{" "}
          <Link href="/">Alışverişe devam</Link>
        </p>
      ) : (
        <>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {cart.items.map((i) => (
              <li key={i.product_id} className="card" style={{ marginBottom: "0.75rem" }}>
                <strong>{i.name}</strong> — {i.price} ₺ × {i.quantity} = {i.line_total} ₺
                <div
                  style={{ marginTop: "0.5rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}
                >
                  <button type="button" onClick={() => setQty(i.product_id, i.quantity - 1)}>
                    −
                  </button>
                  <button type="button" onClick={() => setQty(i.product_id, i.quantity + 1)}>
                    +
                  </button>
                  <button type="button" onClick={() => remove(i.product_id)}>
                    Kaldır
                  </button>
                </div>
              </li>
            ))}
          </ul>
          <p>
            <strong>Toplam: {cart.total_price} ₺</strong>
          </p>
          {token ? (
            <Link href="/checkout">
              <button type="button" className="primary">
                Siparişi tamamla
              </button>
            </Link>
          ) : (
            <p>
              Ödeme için{" "}
              <Link href="/login">giriş yapın</Link>.
            </p>
          )}
        </>
      )}
    </div>
  );
}
