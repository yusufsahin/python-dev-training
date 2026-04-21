/** Epic 2 — Ürün/hizmet kartı (MVP: tek para birimi TRY, tek fiyat listesi alanı). */
export type UrunTur = 'URUN' | 'HIZMET'

export type UrunKartDto = {
  id: string
  tur: UrunTur
  ad: string
  sku: string
  barkod: string
  birim: string
  kdvOrani: number
  satisFiyati: number
  alisFiyati: number
  dovizKodu: 'TRY'
  kategori: string
  fiyatListesiAdi: string
  aktif: boolean
}
