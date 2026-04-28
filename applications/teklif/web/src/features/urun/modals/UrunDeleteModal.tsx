import { useState } from 'react'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { useDeleteUrunMutation } from '@/store/api/baseApi'
import { getErrorMessage } from '@/store/api/getErrorMessage'

type Props = {
  open: boolean
  urunId: string
  label: string
  onClose: () => void
}

export function UrunDeleteModal({ open, urunId, label, onClose }: Props) {
  const [deleteUrun, { isLoading }] = useDeleteUrunMutation()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <AlertDialog
      open={open}
      onOpenChange={(v) => {
        if (!v) onClose()
      }}
    >
      <AlertDialogContent className="max-w-[calc(100%-2rem)]">
        <AlertDialogHeader>
          <AlertDialogTitle>Kaydı sil?</AlertDialogTitle>
          <AlertDialogDescription>
            <span className="font-medium text-foreground">{label}</span> katalogdan kaldırılacaktır
            (mock veri).
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          {submitError ? <p className="w-full text-sm text-destructive">{submitError}</p> : null}
          <AlertDialogCancel disabled={isLoading}>Vazgeç</AlertDialogCancel>
          <AlertDialogAction
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            disabled={isLoading}
            onClick={async (e) => {
              e.preventDefault()
              try {
                setSubmitError(null)
                await deleteUrun(urunId).unwrap()
                onClose()
              } catch (error) {
                setSubmitError(getErrorMessage(error, 'Ürün/hizmet silinemedi.'))
              }
            }}
          >
            {isLoading ? 'Siliniyor…' : 'Evet, sil'}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
