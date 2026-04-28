export type TeklifDurum = 'TASLAK' | 'GONDERILDI' | 'ONAYLANDI' | 'IPTAL'

export type TeklifKalemiDto = {
  urunId: string
  miktar: number
  birimFiyat: number
  kdvOrani: number
  araToplam: number
  kdvTutari: number
}

export type TeklifDto = {
  id: string
  cariId: string
  paraBirimi: 'TRY'
  durum: TeklifDurum
  kalemler: TeklifKalemiDto[]
  toplamTutar: number
  toplamKdv: number
  genelToplam: number
  createdAt: string
}

export type TeklifCreateInput = {
  cariId: string
  paraBirimi: 'TRY'
  kalemler: Array<{
    urunId: string
    miktar: number
    birimFiyat: number
    kdvOrani: number
  }>
}
