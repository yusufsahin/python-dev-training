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

type Props = {
  open: boolean
  cariId: string
  label: string
  onClose: () => void
}

/** Silme onayı: tüm kırılımlarda `AlertDialog` (Radix) ile tutarlı UX. */
export function CariDeleteModal({ open, cariId, label, onClose }: Props) {
  const [deleteCari, { isLoading }] = useDeleteCariMutation()

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
          <AlertDialogCancel disabled={isLoading}>Vazgeç</AlertDialogCancel>
          <AlertDialogAction
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            disabled={isLoading}
            onClick={async (e) => {
              e.preventDefault()
              await deleteCari(cariId).unwrap()
              onClose()
            }}
          >
            {isLoading ? 'Siliniyor…' : 'Evet, sil'}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
