"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useCartId } from "@/context/CartIdContext";
import { useCartUi } from "@/context/CartUiContext";

export default function ProductPage() {
  const params = useParams();
  const slug = params.slug;
  const { cartId } = useCartId();
  const { refreshCartCount } = useCartUi();
  const [data, setData] = useState(null);
  const [err, setErr] = useState(null);
  const [msg, setMsg] = useState(null);

  useEffect(() => {
    if (!slug) return;
    let c = false;
    (async () => {
      try {
        const d = await api(`/api/catalog/products/${encodeURIComponent(slug)}`);
        if (!c) setData(d);
      } catch (e) {
        if (!c) setErr(e.message);
      }
    })();
    return () => {
      c = true;
    };
  }, [slug]);

  async function addToCart() {
    if (!cartId) return;
    setMsg(null);
    try {
      await api("/api/cart/items", {
        method: "POST",
        headers: { "X-Cart-Id": cartId },
        body: { product_id: data.product.id, quantity: 1 },
      });
      setMsg("Sepete eklendi.");
      await refreshCartCount();
    } catch (e) {
      setMsg(e.message);
    }
  }

  if (err) return <p style={{ color: "crimson" }}>{err}</p>;
  if (!data) return <p>Yükleniyor…</p>;
  const p = data.product;

  return (
    <div>
      <nav style={{ marginBottom: "1rem" }}>
        {data.breadcrumb?.map((b, i) => (
          <span key={b.slug}>
            {i > 0 ? " / " : ""}
            <Link href={`/category/${b.slug}`}>{b.name}</Link>
          </span>
        ))}
      </nav>
      <h1>{p.name}</h1>
      <p>{p.description}</p>
      <p>
        <strong>{p.price} ₺</strong> — Stok: {p.stock}
      </p>
      <button type="button" className="primary" onClick={addToCart} disabled={!p.is_in_stock || !cartId}>
        Sepete ekle
      </button>
      {msg ? <p>{msg}</p> : null}
      {data.related_products?.length ? (
        <section style={{ marginTop: "2rem" }}>
          <h2>Benzer ürünler</h2>
          <div className="product-grid">
            {data.related_products.map((rp) => (
              <div key={rp.id} className="card">
                <Link href={`/product/${rp.slug}`}>{rp.name}</Link>
              </div>
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}
