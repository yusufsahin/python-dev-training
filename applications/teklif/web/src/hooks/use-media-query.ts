import { useEffect, useState } from 'react'

/**
 * Mobile-first: default false until match — avoids SSR/hydration flash in future SSR setups.
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const m = window.matchMedia(query)
    const onChange = () => setMatches(m.matches)
    onChange()
    m.addEventListener('change', onChange)
    return () => m.removeEventListener('change', onChange)
  }, [query])

  return matches
}

export function useIsDesktop() {
  return useMediaQuery('(min-width: 768px)')
}
