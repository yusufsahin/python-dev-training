"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ProductCard } from "@/components/ProductCard";
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
    <div className="home-page">
      <section className="home-hero">
        <p className="home-eyebrow">E‑ticaret · mikroservis demo</p>
        <h1 className="home-title">Storium</h1>
        <p className="home-lead">Öne çıkan ürünler ve kategorilerle keşfet.</p>
      </section>

      <div className="home-layout">
        <aside className="category-panel" aria-labelledby="cat-heading">
          <h2 id="cat-heading" className="category-panel__title">
            Kategoriler
          </h2>
          <ul className="category-tree">
            {nav.map((root) => (
              <li key={root.slug} className="category-tree__root">
                <Link href={`/category/${root.slug}`} className="category-tree__link">
                  {root.name}
                </Link>
                {root.children?.length ? (
                  <ul className="category-tree__sub">
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
        </aside>

        <section className="featured-section">
          <h2 className="section-heading">Öne çıkan ürünler</h2>
          <div className="product-grid">
            {featured.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
