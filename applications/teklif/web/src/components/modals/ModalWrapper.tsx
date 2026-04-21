import * as React from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet'
import { useIsDesktop } from '@/hooks/use-media-query'
import { cn } from '@/lib/utils'

export type ModalWrapperProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  title: string
  description?: string
  /** Mobilde sheet altına, masaüstünde dialog altına */
  children: React.ReactNode
  footer?: React.ReactNode
  /** Dialog içeriği max genişlik */
  contentClassName?: string
}

/**
 * Responsive modal kabı: **md+** `Dialog`, küçük ekranlarda alttan **Sheet**.
 * CRUD formları bu bileşenle sarılır; `ModalManager` açık/kapalı durumunu Redux’tan verir.
 */
export function ModalWrapper({
  open,
  onOpenChange,
  title,
  description,
  children,
  footer,
  contentClassName,
}: ModalWrapperProps) {
  const isDesktop = useIsDesktop()

  if (isDesktop) {
    return (
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent
          className={cn(
            'flex max-h-[min(90vh,720px)] flex-col gap-0 overflow-hidden p-0 sm:max-w-lg',
            contentClassName,
          )}
          showCloseButton
        >
          <DialogHeader className="shrink-0 border-b border-border px-6 py-4 text-left">
            <DialogTitle>{title}</DialogTitle>
            {description ? (
              <DialogDescription>{description}</DialogDescription>
            ) : (
              <DialogDescription className="sr-only">{title}</DialogDescription>
            )}
          </DialogHeader>
          <div className="min-h-0 flex-1 overflow-y-auto px-6 py-4">{children}</div>
          {footer ? (
            <DialogFooter className="shrink-0 border-t border-border px-6 py-4 sm:justify-end">
              {footer}
            </DialogFooter>
          ) : null}
        </DialogContent>
      </Dialog>
    )
  }

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side="bottom"
        className={cn('flex max-h-[92vh] flex-col gap-0 rounded-t-xl p-0', contentClassName)}
      >
        <SheetHeader className="shrink-0 border-b border-border px-4 py-3 text-left">
          <SheetTitle>{title}</SheetTitle>
          {description ? (
            <SheetDescription>{description}</SheetDescription>
          ) : (
            <SheetDescription className="sr-only">{title}</SheetDescription>
          )}
        </SheetHeader>
        <div className="min-h-0 flex-1 overflow-y-auto px-4 py-4">{children}</div>
        {footer ? (
          <SheetFooter className="shrink-0 flex-col gap-2 border-t border-border px-4 py-4">
            {footer}
          </SheetFooter>
        ) : null}
      </SheetContent>
    </Sheet>
  )
}
