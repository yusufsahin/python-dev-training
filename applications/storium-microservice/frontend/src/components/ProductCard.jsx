"use client";

import Image from "next/image";
import Link from "next/link";
import { productImageSrc } from "@/lib/productImage";

export function ProductCard({ product, showStock = true }) {
  const src = productImageSrc(product);
  return (
    <article className="product-card">
      <Link href={`/product/${product.slug}`} className="product-card__media">
        <Image
          src={src}
          alt={product.name}
          width={640}
          height={480}
          sizes="(max-width: 900px) 50vw, 240px"
          className="product-card__image"
        />
      </Link>
      <div className="product-card__body">
        <Link href={`/product/${product.slug}`} className="product-card__title-link">
          <h3 className="product-card__title">{product.name}</h3>
        </Link>
        <p className="product-card__meta">
          <span className="product-card__price">{product.price} ₺</span>
          {showStock ? (
            <span className={`product-card__stock${product.stock <= 0 ? " is-out" : ""}`}>
              {product.stock <= 0 ? "Tükendi" : `Stok: ${product.stock}`}
            </span>
          ) : null}
        </p>
      </div>
    </article>
  );
}
