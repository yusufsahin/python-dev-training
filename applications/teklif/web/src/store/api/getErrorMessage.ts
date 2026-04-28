import type { FetchBaseQueryError } from '@reduxjs/toolkit/query'

type MaybeSerializedError = {
  message?: string
}

function isFetchBaseQueryError(error: unknown): error is FetchBaseQueryError {
  return typeof error === 'object' && error != null && 'status' in error
}

export function getErrorMessage(error: unknown, fallback: string): string {
  if (isFetchBaseQueryError(error)) {
    const data = error.data as { detail?: string; message?: string } | undefined
    if (typeof data?.detail === 'string') return data.detail
    if (typeof data?.message === 'string') return data.message
    if ('error' in error && typeof error.error === 'string') return error.error
  }

  const maybeError = error as MaybeSerializedError
  if (typeof maybeError?.message === 'string') return maybeError.message

  return fallback
}
