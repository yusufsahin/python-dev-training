# Teklif UI — design system

## Kaynak

Tema ve yapı **`Designsystemcreation-main`** projesindeki `src/styles/theme.css` ile hizalandı:

- Neredeyse aynı **CSS değişkenleri** (`:root`, `.dark`, `@theme inline`).
- **Tipografi tabanı:** `h1`–`h4`, `label`, `button`, `input` için `@layer base` (utility sınıfları bunların üzerine yazar).
- **Form:** `Input` arka planı `bg-input-background` (`--input-background`).
- **Animasyon:** shadcn dialog/sheet için `tw-animate-css` (`src/index.css` içinde import).

## Dosyalar

| Dosya | Açıklama |
|--------|-----------|
| `src/styles/theme.css` | Tüm renk, radius, sidebar, chart ve tipografi değişkenleri |
| `src/index.css` | `tailwindcss` + `tw-animate-css` + `theme.css` |
| `src/design-system/tokens.ts` | Jetonların programatik özeti (dokümantasyon) |

## Önizleme

Uygulama üst sekmesinden **DS** → Make ile aynı 7 sekme: Renkler, Tipografi, Butonlar, Formlar, Veri, İkonlar, Layout.

`DesignSystemPage` **yalnızca DS sekmesi açıldığında** `React.lazy` ile yüklenir (`App.tsx` + `Suspense`); ana paket boyutu küçük kalır.

Showcase bileşenleri: `src/features/design-system/*Showcase.tsx`, giriş: `DesignSystemPage.tsx`.

Eklenen shadcn bileşenleri (form + veri vitrinleri için): `switch`, `checkbox`, `radio-group`, `avatar`, `progress`.

## Modal / CRUD

Değişmedi: `ModalWrapper`, `ModalManager`, `modalSlice`. Yeni entity eklerken bu tokenları kullanmaya devam edin.

## shadcn bileşen eklemek

```bash
cd web
npx shadcn@latest add tabs
```
