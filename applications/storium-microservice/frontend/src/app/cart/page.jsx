"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";
import { productImageSrc } from "@/lib/productImage";
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
          <ul className="cart-lines">
            {cart.items.map((i) => (
              <li key={i.product_id} className="cart-line card">
                <Image
                  className="cart-line__thumb"
                  src={productImageSrc(i)}
                  alt={i.name}
                  width={88}
                  height={88}
                />
                <div className="cart-line__main">
                  <strong>{i.name}</strong>
                  <p className="cart-line__prices">
                    {i.price} ₺ × {i.quantity} = <strong>{i.line_total} ₺</strong>
                  </p>
                  <div className="cart-line__actions">
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
