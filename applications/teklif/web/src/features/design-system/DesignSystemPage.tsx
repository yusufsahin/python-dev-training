import {
  FileInput,
  Layout,
  MousePointer,
  Palette,
  Shapes,
  Table2,
  Type,
} from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ButtonShowcase } from '@/features/design-system/ButtonShowcase'
import { ColorPalette } from '@/features/design-system/ColorPalette'
import { DataDisplayShowcase } from '@/features/design-system/DataDisplayShowcase'
import { FormShowcase } from '@/features/design-system/FormShowcase'
import { IconsShowcase } from '@/features/design-system/IconsShowcase'
import { LayoutShowcase } from '@/features/design-system/LayoutShowcase'
import { TypographyShowcase } from '@/features/design-system/TypographyShowcase'

/** Designsystemcreation-main ile aynı sekme yapısı; tokenlar `src/styles/theme.css`. */
function DesignSystemPage() {
  return (
    <div className="min-h-svh bg-background">
      <header className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="mx-auto max-w-6xl px-4 py-4 sm:px-6">
          <h1 className="mb-1">Design system</h1>
          <p className="text-sm text-muted-foreground">
            Kaynak: <code className="rounded bg-muted px-1 py-0.5 text-xs">Designsystemcreation-main</code>{' '}
            — Teklif + ön muhasebe UI
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        <p className="mb-8 max-w-3xl text-muted-foreground">
          Renk ve tipografi <code className="text-foreground">src/styles/theme.css</code> üzerinden
          yönetilir; bileşenler shadcn + lucide ile uyumludur.
        </p>

        <Tabs defaultValue="colors" className="w-full">
          <TabsList className="mb-8 flex h-auto min-h-10 w-full flex-wrap justify-start gap-1 sm:grid sm:grid-cols-4 lg:grid-cols-7">
            <TabsTrigger value="colors" className="gap-1.5 px-2 sm:px-3">
              <Palette className="size-4 shrink-0" />
              <span className="hidden sm:inline">Renkler</span>
              <span className="sm:hidden">Renk</span>
            </TabsTrigger>
            <TabsTrigger value="typography" className="gap-1.5 px-2 sm:px-3">
              <Type className="size-4 shrink-0" />
              <span className="hidden sm:inline">Tipografi</span>
              <span className="sm:hidden">Tipo</span>
            </TabsTrigger>
            <TabsTrigger value="buttons" className="gap-1.5 px-2 sm:px-3">
              <MousePointer className="size-4 shrink-0" />
              <span className="hidden sm:inline">Butonlar</span>
              <span className="sm:hidden">Btn</span>
            </TabsTrigger>
            <TabsTrigger value="forms" className="gap-1.5 px-2 sm:px-3">
              <FileInput className="size-4 shrink-0" />
              <span className="hidden sm:inline">Formlar</span>
              <span className="sm:hidden">Form</span>
            </TabsTrigger>
            <TabsTrigger value="data" className="gap-1.5 px-2 sm:px-3">
              <Table2 className="size-4 shrink-0" />
              <span className="hidden sm:inline">Veri</span>
              <span className="sm:hidden">Veri</span>
            </TabsTrigger>
            <TabsTrigger value="icons" className="gap-1.5 px-2 sm:px-3">
              <Shapes className="size-4 shrink-0" />
              <span className="hidden sm:inline">İkonlar</span>
              <span className="sm:hidden">İkon</span>
            </TabsTrigger>
            <TabsTrigger value="layout" className="gap-1.5 px-2 sm:px-3">
              <Layout className="size-4 shrink-0" />
              <span className="hidden sm:inline">Layout</span>
              <span className="sm:hidden">Lay</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="colors" className="space-y-4">
            <div>
              <h2 className="mb-2">Renk paleti</h2>
              <p className="text-sm text-muted-foreground">Platform renkleri ve grafik tonları</p>
            </div>
            <ColorPalette />
          </TabsContent>

          <TabsContent value="typography" className="space-y-4">
            <div>
              <h2 className="mb-2">Tipografi</h2>
              <p className="text-sm text-muted-foreground">Başlıklar ve gövde metni</p>
            </div>
            <TypographyShowcase />
          </TabsContent>

          <TabsContent value="buttons" className="space-y-4">
            <div>
              <h2 className="mb-2">Butonlar</h2>
              <p className="text-sm text-muted-foreground">Varyant, boyut ve ikon kullanımı</p>
            </div>
            <ButtonShowcase />
          </TabsContent>

          <TabsContent value="forms" className="space-y-4">
            <div>
              <h2 className="mb-2">Form elemanları</h2>
              <p className="text-sm text-muted-foreground">Input, select, checkbox, switch, radio</p>
            </div>
            <FormShowcase />
          </TabsContent>

          <TabsContent value="data" className="space-y-4">
            <div>
              <h2 className="mb-2">Veri görünümü</h2>
              <p className="text-sm text-muted-foreground">Tablo, kart, rozet, avatar, ilerleme</p>
            </div>
            <DataDisplayShowcase />
          </TabsContent>

          <TabsContent value="icons" className="space-y-4">
            <div>
              <h2 className="mb-2">İkonlar</h2>
              <p className="text-sm text-muted-foreground">lucide-react grupları</p>
            </div>
            <IconsShowcase />
          </TabsContent>

          <TabsContent value="layout" className="space-y-4">
            <div>
              <h2 className="mb-2">Layout</h2>
              <p className="text-sm text-muted-foreground">Spacing, radius, grid, separator, sekmeler</p>
            </div>
            <LayoutShowcase />
          </TabsContent>
        </Tabs>
      </main>

      <footer className="mt-16 border-t">
        <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6">
          <p className="text-center text-sm text-muted-foreground">
            Teklif + ön muhasebe design system
          </p>
        </div>
      </footer>
    </div>
  )
}

export { DesignSystemPage }
export default DesignSystemPage
