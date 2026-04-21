import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Button } from '@/components/ui/button'
import { Form } from '@/components/ui/form'
import { ModalWrapper } from '@/components/modals/ModalWrapper'
import { CariFormFields } from '@/features/cari/components/CariFormFields'
import {
  cariFormSchema,
  type CariFormValues,
} from '@/features/cari/schemas/cariFormSchema'
import { useGetCariQuery, useUpdateCariMutation } from '@/store/api/baseApi'

type Props = {
  open: boolean
  cariId: string
  onClose: () => void
}

export function CariEditModal({ open, cariId, onClose }: Props) {
  const { data, isFetching } = useGetCariQuery(cariId, { skip: !open })
  const [updateCari, { isLoading }] = useUpdateCariMutation()
  const form = useForm<CariFormValues>({
    resolver: zodResolver(cariFormSchema),
    defaultValues: {
      unvan: '',
      vergiNo: '',
      eposta: '',
      telefon: '',
    },
  })

  useEffect(() => {
    if (data) {
      form.reset({
        unvan: data.unvan,
        vergiNo: data.vergiNo,
        eposta: data.eposta,
        telefon: data.telefon,
      })
    }
  }, [data, form])

  const onSubmit = form.handleSubmit(async (values) => {
    if (!data) return
    await updateCari({ ...data, ...values }).unwrap()
    onClose()
  })

  return (
    <ModalWrapper
      open={open}
      onOpenChange={(v) => {
        if (!v) onClose()
      }}
      title="Cari düzenle"
      description={isFetching ? 'Yükleniyor…' : data?.unvan}
      footer={
        <div className="flex w-full flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <Button type="button" variant="outline" onClick={onClose}>
            Vazgeç
          </Button>
          <Button type="submit" form="cari-edit-form" disabled={isLoading || isFetching || !data}>
            {isLoading ? 'Kaydediliyor…' : 'Güncelle'}
          </Button>
        </div>
      }
    >
      {!data && isFetching ? (
        <p className="text-sm text-muted-foreground">Kayıt yükleniyor…</p>
      ) : (
        <Form {...form}>
          <form id="cari-edit-form" className="space-y-4" onSubmit={onSubmit}>
            <CariFormFields form={form} />
          </form>
        </Form>
      )}
    </ModalWrapper>
  )
}
