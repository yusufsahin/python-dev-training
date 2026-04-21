import { useCallback, useMemo } from 'react'
import { CariCreateModal } from '@/features/cari/modals/CariCreateModal'
import { CariDeleteModal } from '@/features/cari/modals/CariDeleteModal'
import { CariEditModal } from '@/features/cari/modals/CariEditModal'
import { UrunCreateModal } from '@/features/urun/modals/UrunCreateModal'
import { UrunDeleteModal } from '@/features/urun/modals/UrunDeleteModal'
import { UrunEditModal } from '@/features/urun/modals/UrunEditModal'
import { popModal, selectTopModal } from '@/store/slices/modalSlice'
import { useAppDispatch, useAppSelector } from '@/store/hooks'

/**
 * Uygulama kökünde bir kez render edilir. Redux’taki üst modal anahtarına göre
 * ilgili CRUD modal bileşenini gösterir.
 */
export function ModalManager() {
  const dispatch = useAppDispatch()
  const top = useAppSelector(selectTopModal)

  const onClose = useCallback(() => {
    dispatch(popModal())
  }, [dispatch])

  const node = useMemo(() => {
    switch (top.key) {
      case 'none':
        return null
      case 'cari:create':
        return <CariCreateModal open onClose={onClose} />
      case 'cari:edit':
        return <CariEditModal open cariId={top.cariId} onClose={onClose} />
      case 'cari:delete':
        return (
          <CariDeleteModal
            open
            cariId={top.cariId}
            label={top.label}
            onClose={onClose}
          />
        )
      case 'urun:create':
        return <UrunCreateModal open onClose={onClose} />
      case 'urun:edit':
        return <UrunEditModal open urunId={top.urunId} onClose={onClose} />
      case 'urun:delete':
        return (
          <UrunDeleteModal open urunId={top.urunId} label={top.label} onClose={onClose} />
        )
      default:
        return null
    }
  }, [onClose, top])

  return <>{node}</>
}
