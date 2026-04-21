import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Button } from '@/components/ui/button'
import { Form } from '@/components/ui/form'
import { ModalWrapper } from '@/components/modals/ModalWrapper'
import { CariFormFields } from '@/features/cari/components/CariFormFields'
import {
  cariFormSchema,
  type CariFormValues,
} from '@/features/cari/schemas/cariFormSchema'
import { useCreateCariMutation } from '@/store/api/baseApi'

type Props = {
  open: boolean
  onClose: () => void
}

export function CariCreateModal({ open, onClose }: Props) {
  const [createCari, { isLoading }] = useCreateCariMutation()
  const form = useForm<CariFormValues>({
    resolver: zodResolver(cariFormSchema),
    defaultValues: {
      unvan: '',
      vergiNo: '',
      eposta: '',
      telefon: '',
    },
  })

  const onSubmit = form.handleSubmit(async (values) => {
    await createCari(values).unwrap()
    form.reset()
    onClose()
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
      title="Yeni cari"
      description="Müşteri veya tedarikçi kartı oluşturun. Kayıt şu an yalnızca tarayıcı oturumunda tutulmaktadır (UI-first mock)."
      footer={
        <div className="flex w-full flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <Button type="button" variant="outline" onClick={() => { form.reset(); onClose(); }}>
            Vazgeç
          </Button>
          <Button type="submit" form="cari-create-form" disabled={isLoading}>
            {isLoading ? 'Kaydediliyor…' : 'Kaydet'}
          </Button>
        </div>
      }
    >
      <Form {...form}>
        <form id="cari-create-form" className="space-y-4" onSubmit={onSubmit}>
          <CariFormFields form={form} />
        </form>
      </Form>
    </ModalWrapper>
  )
}
