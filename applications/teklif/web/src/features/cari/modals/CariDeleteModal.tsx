import { useState } from 'react'
import { useDeleteCariMutation } from '@/store/api/baseApi'
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
import { getErrorMessage } from '@/store/api/getErrorMessage'

type Props = {
  open: boolean
  cariId: string
  label: string
  onClose: () => void
}

/** Silme onayı: tüm kırılımlarda `AlertDialog` (Radix) ile tutarlı UX. */
export function CariDeleteModal({ open, cariId, label, onClose }: Props) {
  const [deleteCari, { isLoading }] = useDeleteCariMutation()
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
          <AlertDialogTitle>Cariyi sil?</AlertDialogTitle>
          <AlertDialogDescription>
            <span className="font-medium text-foreground">{label}</span> kaydı kalıcı olarak
            listeden kaldırılacaktır (mock veri).
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
                await deleteCari(cariId).unwrap()
                onClose()
              } catch (error) {
                setSubmitError(getErrorMessage(error, 'Cari silinemedi.'))
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
