"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function HomePage() {
  const [featured, setFeatured] = useState([]);
  const [nav, setNav] = useState([]);
  const [err, setErr] = useState(null);

  useEffect(() => {
    let c = false;
    (async () => {
      try {
        const [f, n] = await Promise.all([api("/api/catalog/featured"), api("/api/catalog/nav")]);
        if (!c) {
          setFeatured(f);
          setNav(n);
        }
      } catch (e) {
        if (!c) setErr(String(e.message));
      }
    })();
    return () => {
      c = true;
    };
  }, []);

  if (err) return <p style={{ color: "crimson" }}>{err}</p>;

  return (
    <div>
      <h1>Storium</h1>
      <section style={{ marginBottom: "2rem" }}>
        <h2>Kategoriler</h2>
        <ul>
          {nav.map((root) => (
            <li key={root.slug}>
              <Link href={`/category/${root.slug}`}>{root.name}</Link>
              {root.children?.length ? (
                <ul>
                  {root.children.map((ch) => (
                    <li key={ch.slug}>
                      <Link href={`/category/${ch.slug}`}>{ch.name}</Link>
                    </li>
                  ))}
                </ul>
              ) : null}
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h2>Öne çıkan ürünler</h2>
        <div className="product-grid">
          {featured.map((p) => (
            <div key={p.id} className="card">
              <Link href={`/product/${p.slug}`}>
                <strong>{p.name}</strong>
              </Link>
              <p>
                {p.price} ₺ — Stok: {p.stock}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
