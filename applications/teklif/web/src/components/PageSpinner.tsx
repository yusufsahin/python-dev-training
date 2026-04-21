import { cn } from '@/lib/utils'

export function PageSpinner({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        'flex min-h-[40vh] flex-col items-center justify-center gap-3 text-muted-foreground',
        className,
      )}
      role="status"
      aria-label="Yükleniyor"
    >
      <div className="size-8 animate-spin rounded-full border-2 border-muted border-t-primary" />
      <p className="text-sm">Yükleniyor…</p>
    </div>
  )
}
