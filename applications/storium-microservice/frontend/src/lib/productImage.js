/**
 * Ürün görseli: API'deki image_url veya slug'a sabit (deterministik) placeholder.
 */
export function productImageSrc(product) {
  const raw = product?.image_url;
  if (raw && String(raw).trim()) {
    return String(raw).trim();
  }
  const seed = encodeURIComponent(product?.slug || String(product?.id ?? "storium"));
  return `https://picsum.photos/seed/${seed}/640/480`;
}
