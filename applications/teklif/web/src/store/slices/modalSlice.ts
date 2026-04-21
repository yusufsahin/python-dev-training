import { createSlice, type PayloadAction } from '@reduxjs/toolkit'

/** Tüm CRUD modalları merkezi kayıt defterinden açılır; yeni entity tipleri buraya eklenir. */
export type AppModalState =
  | { key: 'none' }
  | { key: 'cari:create' }
  | { key: 'cari:edit'; cariId: string }
  | { key: 'cari:delete'; cariId: string; label: string }
  | { key: 'urun:create' }
  | { key: 'urun:edit'; urunId: string }
  | { key: 'urun:delete'; urunId: string; label: string }

type ModalSliceState = {
  stack: AppModalState[]
}

const initialState: ModalSliceState = {
  stack: [{ key: 'none' }],
}

export const modalSlice = createSlice({
  name: 'modal',
  initialState,
  reducers: {
    pushModal: (state, action: PayloadAction<Exclude<AppModalState, { key: 'none' }>>) => {
      state.stack.push(action.payload)
    },
    replaceModal: (
      state,
      action: PayloadAction<Exclude<AppModalState, { key: 'none' }> | { key: 'none' }>,
    ) => {
      state.stack = [action.payload]
    },
    popModal: (state) => {
      if (state.stack.length > 1) {
        state.stack.pop()
      } else {
        state.stack = [{ key: 'none' }]
      }
    },
    closeAll: (state) => {
      state.stack = [{ key: 'none' }]
    },
  },
})

export const { pushModal, replaceModal, popModal, closeAll } = modalSlice.actions

export function selectTopModal(state: { modal: ModalSliceState }): AppModalState {
  const s = state.modal.stack
  return s[s.length - 1] ?? { key: 'none' }
}
