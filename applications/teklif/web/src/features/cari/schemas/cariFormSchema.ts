import { z } from 'zod'

export const cariFormSchema = z.object({
  unvan: z.string().min(2, 'Ünvan en az 2 karakter olmalıdır.'),
  vergiNo: z
    .string()
    .min(10, 'Vergi numarası / TCKN formatını kontrol edin.')
    .max(11),
  eposta: z.string().email('Geçerli bir e-posta girin.'),
  telefon: z.string().min(10, 'Telefon en az 10 karakter olmalıdır.'),
})

export type CariFormValues = z.infer<typeof cariFormSchema>
