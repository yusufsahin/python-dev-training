import { lazy, Suspense, useState } from 'react'
import { FileText, LayoutGrid, Package, Palette, Users } from 'lucide-react'
import { ModalManager } from '@/components/modals/ModalManager'
import { PageSpinner } from '@/components/PageSpinner'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { CariListPage } from '@/features/cari/pages/CariListPage'
import { TeklifListPage } from '@/features/teklif/pages/TeklifListPage'
import { UrunListPage } from '@/features/urun/pages/UrunListPage'

const DesignSystemPage = lazy(() => import('@/features/design-system/DesignSystemPage'))

export default function App() {
  const [mainTab, setMainTab] = useState<'app' | 'design'>('app')
  const [appSection, setAppSection] = useState<'cari' | 'urun' | 'teklif'>('cari')

  return (
    <>
      <Tabs
        value={mainTab}
        onValueChange={(v) => setMainTab(v as 'app' | 'design')}
        className="flex min-h-svh flex-col"
      >
        <div className="sticky top-0 z-30 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
          <div className="mx-auto flex max-w-5xl items-center gap-2 px-4 py-2 sm:px-6">
            <TabsList className="grid w-full max-w-xs grid-cols-2">
              <TabsTrigger value="app" className="gap-2">
                <LayoutGrid className="size-4 shrink-0" />
                Uygulama
              </TabsTrigger>
              <TabsTrigger value="design" className="gap-2">
                <Palette className="size-4 shrink-0" />
                DS
              </TabsTrigger>
            </TabsList>
          </div>
        </div>
        <TabsContent value="app" className="mt-0 flex-1 outline-none" forceMount>
          <div className="border-b bg-muted/40">
            <div className="mx-auto flex max-w-5xl flex-wrap gap-1 px-4 py-2 sm:px-6">
              <Button
                size="sm"
                variant={appSection === 'cari' ? 'secondary' : 'ghost'}
                className="gap-2"
                onClick={() => setAppSection('cari')}
              >
                <Users className="size-4 shrink-0" />
                Cariler
              </Button>
              <Button
                size="sm"
                variant={appSection === 'urun' ? 'secondary' : 'ghost'}
                className="gap-2"
                onClick={() => setAppSection('urun')}
              >
                <Package className="size-4 shrink-0" />
                Ürün / hizmet
              </Button>
              <Button
                size="sm"
                variant={appSection === 'teklif' ? 'secondary' : 'ghost'}
                className="gap-2"
                onClick={() => setAppSection('teklif')}
              >
                <FileText className="size-4 shrink-0" />
                Teklifler
              </Button>
            </div>
          </div>
          {appSection === 'cari' ? <CariListPage /> : null}
          {appSection === 'urun' ? <UrunListPage /> : null}
          {appSection === 'teklif' ? <TeklifListPage /> : null}
        </TabsContent>
        <TabsContent value="design" className="mt-0 flex-1 outline-none" forceMount>
          {mainTab === 'design' ? (
            <Suspense fallback={<PageSpinner />}>
              <DesignSystemPage />
            </Suspense>
          ) : null}
        </TabsContent>
      </Tabs>
      <ModalManager />
    </>
  )
}
