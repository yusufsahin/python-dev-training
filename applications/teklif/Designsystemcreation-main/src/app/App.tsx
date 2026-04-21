import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { ColorPalette } from "./components/design-system/ColorPalette";
import { TypographyShowcase } from "./components/design-system/TypographyShowcase";
import { ButtonShowcase } from "./components/design-system/ButtonShowcase";
import { FormShowcase } from "./components/design-system/FormShowcase";
import { DataDisplayShowcase } from "./components/design-system/DataDisplayShowcase";
import { IconsShowcase } from "./components/design-system/IconsShowcase";
import { LayoutShowcase } from "./components/design-system/LayoutShowcase";
import { Palette, Type, MousePointer, FileInput, Table2, Shapes, Layout } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b sticky top-0 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="mb-1">Design System</h1>
              <p className="text-sm text-muted-foreground">
                Teklif + Ön Muhasebe Platformu
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">v0.2</span>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <p className="text-muted-foreground max-w-3xl">
            Bu design system, tekliften tahsilata kadar satış ve ön muhasebe
            süreçlerini yöneten platform için oluşturulmuş UI komponentlerini,
            renk paletini, tipografiyi ve kullanım kılavuzlarını içerir.
          </p>
        </div>

        <Tabs defaultValue="colors" className="w-full">
          <TabsList className="grid w-full grid-cols-7 mb-8">
            <TabsTrigger value="colors" className="gap-2">
              <Palette className="h-4 w-4" />
              <span className="hidden sm:inline">Renkler</span>
            </TabsTrigger>
            <TabsTrigger value="typography" className="gap-2">
              <Type className="h-4 w-4" />
              <span className="hidden sm:inline">Tipografi</span>
            </TabsTrigger>
            <TabsTrigger value="buttons" className="gap-2">
              <MousePointer className="h-4 w-4" />
              <span className="hidden sm:inline">Butonlar</span>
            </TabsTrigger>
            <TabsTrigger value="forms" className="gap-2">
              <FileInput className="h-4 w-4" />
              <span className="hidden sm:inline">Formlar</span>
            </TabsTrigger>
            <TabsTrigger value="data" className="gap-2">
              <Table2 className="h-4 w-4" />
              <span className="hidden sm:inline">Veri</span>
            </TabsTrigger>
            <TabsTrigger value="icons" className="gap-2">
              <Shapes className="h-4 w-4" />
              <span className="hidden sm:inline">İkonlar</span>
            </TabsTrigger>
            <TabsTrigger value="layout" className="gap-2">
              <Layout className="h-4 w-4" />
              <span className="hidden sm:inline">Layout</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="colors">
            <div className="space-y-6">
              <div>
                <h2 className="mb-2">Renk Paleti</h2>
                <p className="text-sm text-muted-foreground">
                  Platformda kullanılan tüm renkler ve kullanım alanları
                </p>
              </div>
              <ColorPalette />
            </div>
          </TabsContent>

          <TabsContent value="typography">
            <div className="space-y-6">
              <div>
                <h2 className="mb-2">Tipografi</h2>
                <p className="text-sm text-muted-foreground">
                  Başlıklar, paragraflar ve metin stilleri
                </p>
              </div>
              <TypographyShowcase />
            </div>
          </TabsContent>

          <TabsContent value="buttons">
            <div className="space-y-6">
              <div>
                <h2 className="mb-2">Butonlar</h2>
                <p className="text-sm text-muted-foreground">
                  Farklı varyantlar, boyutlar ve kullanım senaryoları
                </p>
              </div>
              <ButtonShowcase />
            </div>
          </TabsContent>

          <TabsContent value="forms">
            <div className="space-y-6">
              <div>
                <h2 className="mb-2">Form Elemanları</h2>
                <p className="text-sm text-muted-foreground">
                  Input, select, checkbox ve diğer form bileşenleri
                </p>
              </div>
              <FormShowcase />
            </div>
          </TabsContent>

          <TabsContent value="data">
            <div className="space-y-6">
              <div>
                <h2 className="mb-2">Veri Görselleştirme</h2>
                <p className="text-sm text-muted-foreground">
                  Tablolar, kartlar, badge'ler ve istatistik gösterimleri
                </p>
              </div>
              <DataDisplayShowcase />
            </div>
          </TabsContent>

          <TabsContent value="icons">
            <div className="space-y-6">
              <div>
                <h2 className="mb-2">İkon Kütüphanesi</h2>
                <p className="text-sm text-muted-foreground">
                  Platformda kullanılan ikonlar ve uygulama alanları
                </p>
              </div>
              <IconsShowcase />
            </div>
          </TabsContent>

          <TabsContent value="layout">
            <div className="space-y-6">
              <div>
                <h2 className="mb-2">Layout ve Yapı</h2>
                <p className="text-sm text-muted-foreground">
                  Spacing, grid sistemleri ve yapısal bileşenler
                </p>
              </div>
              <LayoutShowcase />
            </div>
          </TabsContent>
        </Tabs>
      </main>

      <footer className="border-t mt-16">
        <div className="container mx-auto px-6 py-6">
          <p className="text-sm text-muted-foreground text-center">
            Teklif + Ön Muhasebe Platformu Design System © 2026
          </p>
        </div>
      </footer>
    </div>
  );
}