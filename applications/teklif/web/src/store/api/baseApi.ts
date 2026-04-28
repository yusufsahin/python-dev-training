import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { CariDto } from '@/features/cari/types'
import type { TeklifCreateInput, TeklifDto, TeklifDurum } from '@/features/teklif/types'
import type { UrunKartDto } from '@/features/urun/types'

const apiBaseUrl = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, '')
  ?? 'http://localhost:8000'

export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: apiBaseUrl,
    prepareHeaders: (headers) => {
      headers.set('Accept', 'application/json')
      return headers
    },
  }),
  tagTypes: ['Cari', 'UrunKart', 'Teklif'],
  endpoints: (build) => ({
    listCariler: build.query<CariDto[], void>({
      query: () => ({ url: 'cariler' }),
      providesTags: (r) =>
        r ? [...r.map(({ id }) => ({ type: 'Cari' as const, id })), 'Cari'] : ['Cari'],
    }),
    getCari: build.query<CariDto, string>({
      query: (id) => ({ url: `cariler/${id}` }),
      providesTags: (_r, _e, id) => [{ type: 'Cari', id }],
    }),
    createCari: build.mutation<CariDto, Omit<CariDto, 'id'>>({
      query: (body) => ({
        url: 'cariler',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Cari'],
    }),
    updateCari: build.mutation<CariDto, CariDto>({
      query: (body) => ({
        url: `cariler/${body.id}`,
        method: 'PATCH',
        body,
      }),
      invalidatesTags: (_r, _e, arg) => [{ type: 'Cari', id: arg.id }, 'Cari'],
    }),
    deleteCari: build.mutation<{ ok: true }, string>({
      query: (id) => ({
        url: `cariler/${id}`,
        method: 'DELETE',
      }),
      transformResponse: () => ({ ok: true } as const),
      invalidatesTags: (_r, _e, id) => [{ type: 'Cari', id }, 'Cari'],
    }),

    listUrunler: build.query<UrunKartDto[], void>({
      query: () => ({ url: 'urunler' }),
      providesTags: (r) =>
        r
          ? [...r.map(({ id }) => ({ type: 'UrunKart' as const, id })), 'UrunKart']
          : ['UrunKart'],
    }),
    getUrun: build.query<UrunKartDto, string>({
      query: (id) => ({ url: `urunler/${id}` }),
      providesTags: (_r, _e, id) => [{ type: 'UrunKart', id }],
    }),
    createUrun: build.mutation<UrunKartDto, Omit<UrunKartDto, 'id'>>({
      query: (body) => ({
        url: 'urunler',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['UrunKart'],
    }),
    updateUrun: build.mutation<UrunKartDto, UrunKartDto>({
      query: (body) => ({
        url: `urunler/${body.id}`,
        method: 'PATCH',
        body,
      }),
      invalidatesTags: (_r, _e, arg) => [{ type: 'UrunKart', id: arg.id }, 'UrunKart'],
    }),
    deleteUrun: build.mutation<{ ok: true }, string>({
      query: (id) => ({
        url: `urunler/${id}`,
        method: 'DELETE',
      }),
      transformResponse: () => ({ ok: true } as const),
      invalidatesTags: (_r, _e, id) => [{ type: 'UrunKart', id }, 'UrunKart'],
    }),

    listTeklifler: build.query<TeklifDto[], void>({
      query: () => ({ url: 'teklifler' }),
      providesTags: (r) =>
        r ? [...r.map(({ id }) => ({ type: 'Teklif' as const, id })), 'Teklif'] : ['Teklif'],
    }),
    getTeklif: build.query<TeklifDto, string>({
      query: (id) => ({ url: `teklifler/${id}` }),
      providesTags: (_r, _e, id) => [{ type: 'Teklif', id }],
    }),
    createTeklif: build.mutation<TeklifDto, TeklifCreateInput>({
      query: (body) => ({
        url: 'teklifler',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Teklif'],
    }),
    updateTeklifDurum: build.mutation<TeklifDto, { id: string; durum: TeklifDurum }>({
      query: ({ id, durum }) => ({
        url: `teklifler/${id}/durum`,
        method: 'PATCH',
        body: { durum },
      }),
      invalidatesTags: (_r, _e, { id }) => [{ type: 'Teklif', id }, 'Teklif'],
    }),
  }),
})

export const {
  useListCarilerQuery,
  useGetCariQuery,
  useCreateCariMutation,
  useUpdateCariMutation,
  useDeleteCariMutation,
  useListUrunlerQuery,
  useGetUrunQuery,
  useCreateUrunMutation,
  useUpdateUrunMutation,
  useDeleteUrunMutation,
  useListTekliflerQuery,
  useGetTeklifQuery,
  useCreateTeklifMutation,
  useUpdateTeklifDurumMutation,
} = baseApi
