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

type Props = {
  open: boolean
  urunId: string
  label: string
  onClose: () => void
}

export function UrunDeleteModal({ open, urunId, label, onClose }: Props) {
  const [deleteUrun, { isLoading }] = useDeleteUrunMutation()

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
          <AlertDialogCancel disabled={isLoading}>Vazgeç</AlertDialogCancel>
          <AlertDialogAction
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            disabled={isLoading}
            onClick={async (e) => {
              e.preventDefault()
              await deleteUrun(urunId).unwrap()
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
