/**
 * Semantik jetonlar — kaynak: `Designsystemcreation-main/src/styles/theme.css`
 * (web içinde `src/styles/theme.css` olarak kopyalandı / hizalandı).
 */
export const teklifDesignTokens = {
  radius: {
    sm: 'var(--radius-sm)',
    md: 'var(--radius-md)',
    lg: 'var(--radius-lg)',
    xl: 'var(--radius-xl)',
    base: 'var(--radius)',
  },
  color: {
    background: 'var(--background)',
    foreground: 'var(--foreground)',
    primary: 'var(--primary)',
    primaryForeground: 'var(--primary-foreground)',
    secondary: 'var(--secondary)',
    muted: 'var(--muted)',
    mutedForeground: 'var(--muted-foreground)',
    accent: 'var(--accent)',
    destructive: 'var(--destructive)',
    border: 'var(--border)',
    input: 'var(--input)',
    inputBackground: 'var(--input-background)',
    switchBackground: 'var(--switch-background)',
    ring: 'var(--ring)',
  },
  typography: {
    baseFontSize: 'var(--font-size)',
    xs: 'var(--text-xs)',
    sm: 'var(--text-sm)',
    base: 'var(--text-base)',
    lg: 'var(--text-lg)',
    xl: 'var(--text-xl)',
    '2xl': 'var(--text-2xl)',
    weightNormal: 'var(--font-weight-normal)',
    weightMedium: 'var(--font-weight-medium)',
  },
} as const
