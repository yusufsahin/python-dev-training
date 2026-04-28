import { zodResolver } from '@hookform/resolvers/zod'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Button } from '@/components/ui/button'
import { Form } from '@/components/ui/form'
import { ModalWrapper } from '@/components/modals/ModalWrapper'
import { UrunFormFields } from '@/features/urun/components/UrunFormFields'
import { urunFormSchema, type UrunFormValues } from '@/features/urun/schemas/urunFormSchema'
import { useCreateUrunMutation } from '@/store/api/baseApi'
import { getErrorMessage } from '@/store/api/getErrorMessage'

type Props = {
  open: boolean
  onClose: () => void
}

export function UrunCreateModal({ open, onClose }: Props) {
  const [createUrun, { isLoading }] = useCreateUrunMutation()
  const [submitError, setSubmitError] = useState<string | null>(null)
  const form = useForm<UrunFormValues>({
    resolver: zodResolver(urunFormSchema),
    defaultValues: {
      tur: 'URUN',
      ad: '',
      sku: '',
      barkod: '',
      birim: 'Adet',
      kdvOrani: 20,
      satisFiyati: 0,
      alisFiyati: 0,
      dovizKodu: 'TRY',
      kategori: '',
      fiyatListesiAdi: 'Genel',
      aktif: true,
    },
  })

  const onSubmit = form.handleSubmit(async (values) => {
    try {
      setSubmitError(null)
      await createUrun({
        ...values,
        barkod: values.barkod.trim(),
      }).unwrap()
      form.reset()
      onClose()
    } catch (e) {
      setSubmitError(getErrorMessage(e, 'Ürün/hizmet kaydedilemedi.'))
    }
  })

  return (
    <ModalWrapper
      open={open}
      onOpenChange={(v) => {
        if (!v) {
          form.reset()
          onClose()
        }
      }}
      title="Yeni ürün / hizmet"
      description="Katalog kartı — teklif ve fatura satırlarında kullanılır (şimdilik mock veri)."
      contentClassName="sm:max-w-xl"
      footer={
        <div className="flex w-full flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <Button
            type="button"
            variant="outline"
            onClick={() => {
              form.reset()
              onClose()
            }}
          >
            Vazgeç
          </Button>
          <Button type="submit" form="urun-create-form" disabled={isLoading}>
            {isLoading ? 'Kaydediliyor…' : 'Kaydet'}
          </Button>
        </div>
      }
    >
      <Form {...form}>
        <form id="urun-create-form" className="space-y-4" onSubmit={onSubmit}>
          {submitError ? <p className="text-sm text-destructive">{submitError}</p> : null}
          <UrunFormFields form={form} />
        </form>
      </Form>
    </ModalWrapper>
  )
}
