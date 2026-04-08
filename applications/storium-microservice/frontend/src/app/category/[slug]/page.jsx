"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function CategoryPage() {
  const params = useParams();
  const slug = params.slug;
  const [data, setData] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!slug) return;
    let c = false;
    (async () => {
      try {
        const d = await api(`/api/catalog/categories/${encodeURIComponent(slug)}`);
        if (!c) setData(d);
      } catch (e) {
        if (!c) setErr(e.message);
      }
    })();
    return () => {
      c = true;
    };
  }, [slug]);

  if (err) return <p style={{ color: "crimson" }}>{err}</p>;
  if (!data) return <p>Yükleniyor…</p>;

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
      <h1>{data.category.name}</h1>
      <div className="product-grid">
        {data.products.map((p) => (
          <div key={p.id} className="card">
            <Link href={`/product/${p.slug}`}>
              <strong>{p.name}</strong>
            </Link>
            <p>{p.price} ₺</p>
          </div>
        ))}
      </div>
      <p>
        Sayfa {data.page} / {data.total_pages} (toplam {data.total_count})
      </p>
    </div>
  );
}
