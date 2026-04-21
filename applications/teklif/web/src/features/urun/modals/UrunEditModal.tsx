import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Button } from '@/components/ui/button'
import { Form } from '@/components/ui/form'
import { ModalWrapper } from '@/components/modals/ModalWrapper'
import { UrunFormFields } from '@/features/urun/components/UrunFormFields'
import { urunFormSchema, type UrunFormValues } from '@/features/urun/schemas/urunFormSchema'
import { useGetUrunQuery, useUpdateUrunMutation } from '@/store/api/baseApi'

type Props = {
  open: boolean
  urunId: string
  onClose: () => void
}

export function UrunEditModal({ open, urunId, onClose }: Props) {
  const { data, isFetching } = useGetUrunQuery(urunId, { skip: !open })
  const [updateUrun, { isLoading }] = useUpdateUrunMutation()
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

  useEffect(() => {
    if (!data) return
    form.reset({
      tur: data.tur,
      ad: data.ad,
      sku: data.sku,
      barkod: data.barkod || '',
      birim: data.birim,
      kdvOrani: data.kdvOrani,
      satisFiyati: data.satisFiyati,
      alisFiyati: data.alisFiyati,
      dovizKodu: 'TRY',
      kategori: data.kategori,
      fiyatListesiAdi: data.fiyatListesiAdi,
      aktif: data.aktif,
    })
  }, [data, form])

  const onSubmit = form.handleSubmit(async (values) => {
    if (!data) return
    await updateUrun({
      id: data.id,
      ...values,
      barkod: values.barkod.trim(),
    }).unwrap()
    onClose()
  })

  return (
    <ModalWrapper
      open={open}
      onOpenChange={(v) => {
        if (!v) onClose()
      }}
      title="Ürün / hizmet düzenle"
      description={isFetching ? 'Yükleniyor…' : data?.ad}
      contentClassName="sm:max-w-xl"
      footer={
        <div className="flex w-full flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <Button type="button" variant="outline" onClick={onClose}>
            Vazgeç
          </Button>
          <Button type="submit" form="urun-edit-form" disabled={isLoading || isFetching || !data}>
            {isLoading ? 'Kaydediliyor…' : 'Güncelle'}
          </Button>
        </div>
      }
    >
      {!data && isFetching ? (
        <p className="text-sm text-muted-foreground">Kayıt yükleniyor…</p>
      ) : (
        <Form {...form}>
          <form id="urun-edit-form" className="space-y-4" onSubmit={onSubmit}>
            <UrunFormFields form={form} />
          </form>
        </Form>
      )}
    </ModalWrapper>
  )
}
