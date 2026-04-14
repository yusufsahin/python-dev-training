"use client";

import Image from "next/image";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ProductCard } from "@/components/ProductCard";
import { api } from "@/lib/api";
import { productImageSrc } from "@/lib/productImage";
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

  const imgSrc = productImageSrc(p);

  return (
    <div className="product-detail">
      <nav className="breadcrumb" aria-label="Breadcrumb">
        {data.breadcrumb?.map((b, i) => (
          <span key={b.slug}>
            {i > 0 ? <span className="breadcrumb__sep"> / </span> : null}
            <Link href={`/category/${b.slug}`}>{b.name}</Link>
          </span>
        ))}
      </nav>

      <div className="product-detail__grid">
        <div className="product-detail__media">
          <Image
            className="product-detail__img"
            src={imgSrc}
            alt={p.name}
            width={800}
            height={600}
            priority
            sizes="(max-width: 768px) 100vw, 50vw"
          />
        </div>
        <div className="product-detail__info">
          <h1 className="page-title product-detail__name">{p.name}</h1>
          <p className="product-detail__desc">{p.description}</p>
          <p className="product-detail__buy-row">
            <span className="product-detail__price">{p.price} ₺</span>
            <span className={p.is_in_stock ? "product-detail__stock" : "product-detail__stock is-out"}>
              {p.is_in_stock ? `Stok: ${p.stock}` : "Stokta yok"}
            </span>
          </p>
          <button type="button" className="primary product-detail__cta" onClick={addToCart} disabled={!p.is_in_stock || !cartId}>
            Sepete ekle
          </button>
          {msg ? <p className="product-detail__msg">{msg}</p> : null}
        </div>
      </div>

      {data.related_products?.length ? (
        <section className="related-section">
          <h2 className="section-heading">Benzer ürünler</h2>
          <div className="product-grid">
            {data.related_products.map((rp) => (
              <ProductCard key={rp.id} product={rp} />
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}
