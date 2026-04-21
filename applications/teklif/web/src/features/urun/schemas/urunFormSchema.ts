import { z } from 'zod'

const kdvListe = [0, 1, 8, 10, 18, 20] as const

export const urunFormSchema = z.object({
  tur: z.enum(['URUN', 'HIZMET']),
  ad: z.string().min(2, 'Ad en az 2 karakter olmalıdır.'),
  sku: z.string().min(1, 'SKU zorunludur.').max(64),
  barkod: z.string().max(64),
  birim: z.string().min(1, 'Birim seçin veya girin.'),
  kdvOrani: z
    .number()
    .refine((n) => (kdvListe as readonly number[]).includes(n), 'Geçerli bir KDV oranı seçin.'),
  satisFiyati: z.number().nonnegative('Satış fiyatı negatif olamaz.'),
  alisFiyati: z.number().nonnegative('Alış fiyatı negatif olamaz.'),
  dovizKodu: z.literal('TRY'),
  kategori: z.string().min(1, 'Kategori girin.'),
  fiyatListesiAdi: z.string().min(1, 'Fiyat listesi adı girin.'),
  aktif: z.boolean(),
})

export type UrunFormValues = z.infer<typeof urunFormSchema>
