import { Card, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

/** İç içe sekmeler; üstteki DS sekmelerinden bağımsız değer anahtarları kullanılır. */
export function LayoutShowcase() {
  return (
    <div className="space-y-8">
      <Card>
        <CardContent className="space-y-4 p-6">
          <h3>Spacing</h3>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">4px</div>
            <div className="h-8 bg-primary" style={{ width: '0.25rem' }} />
            <span className="text-xs text-muted-foreground">Tailwind: 1</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">8px</div>
            <div className="h-8 bg-primary" style={{ width: '0.5rem' }} />
            <span className="text-xs text-muted-foreground">2</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">12px</div>
            <div className="h-8 bg-primary" style={{ width: '0.75rem' }} />
            <span className="text-xs text-muted-foreground">3</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">16px</div>
            <div className="h-8 bg-primary" style={{ width: '1rem' }} />
            <span className="text-xs text-muted-foreground">4</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">24px</div>
            <div className="h-8 bg-primary" style={{ width: '1.5rem' }} />
            <span className="text-xs text-muted-foreground">6</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">32px</div>
            <div className="h-8 bg-primary" style={{ width: '2rem' }} />
            <span className="text-xs text-muted-foreground">8</span>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-4 p-6">
          <h3>Border radius</h3>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            <div className="space-y-2">
              <div className="h-20 rounded-sm bg-primary" />
              <p className="text-center text-sm">rounded-sm</p>
            </div>
            <div className="space-y-2">
              <div className="h-20 rounded-md bg-primary" />
              <p className="text-center text-sm">rounded-md</p>
            </div>
            <div className="space-y-2">
              <div className="h-20 rounded-lg bg-primary" />
              <p className="text-center text-sm">rounded-lg</p>
            </div>
            <div className="space-y-2">
              <div className="h-20 rounded-xl bg-primary" />
              <p className="text-center text-sm">rounded-xl</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-4 p-6">
          <h3>Separator</h3>
          <div>
            <p>Bölüm 1</p>
            <Separator className="my-4" />
            <p>Bölüm 2</p>
          </div>
          <div className="flex items-center gap-4">
            <p>Sol</p>
            <Separator orientation="vertical" className="h-8" />
            <p>Sağ</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-6 p-6">
          <h3>Grid</h3>
          <div>
            <p className="mb-3 text-sm text-muted-foreground">1 → md:2 kolon</p>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="rounded-lg bg-muted p-4">Kolon 1</div>
              <div className="rounded-lg bg-muted p-4">Kolon 2</div>
            </div>
          </div>
          <div>
            <p className="mb-3 text-sm text-muted-foreground">1 → md:2 → lg:3</p>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              <div className="rounded-lg bg-muted p-4">Kolon 1</div>
              <div className="rounded-lg bg-muted p-4">Kolon 2</div>
              <div className="rounded-lg bg-muted p-4">Kolon 3</div>
            </div>
          </div>
          <div>
            <p className="mb-3 text-sm text-muted-foreground">2 → lg:4</p>
            <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
              <div className="rounded-lg bg-muted p-4">1</div>
              <div className="rounded-lg bg-muted p-4">2</div>
              <div className="rounded-lg bg-muted p-4">3</div>
              <div className="rounded-lg bg-muted p-4">4</div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <h3 className="mb-6">Sekme örneği</h3>
          <Tabs defaultValue="ds-layout-info" className="w-full">
            <TabsList className="flex h-auto w-full flex-wrap gap-1">
              <TabsTrigger value="ds-layout-info">Genel</TabsTrigger>
              <TabsTrigger value="ds-layout-financial">Mali</TabsTrigger>
              <TabsTrigger value="ds-layout-contact">İletişim</TabsTrigger>
            </TabsList>
            <TabsContent value="ds-layout-info" className="mt-4">
              <p className="text-sm text-muted-foreground">Genel bilgiler sekmesi</p>
            </TabsContent>
            <TabsContent value="ds-layout-financial" className="mt-4">
              <p className="text-sm text-muted-foreground">Mali bilgiler sekmesi</p>
            </TabsContent>
            <TabsContent value="ds-layout-contact" className="mt-4">
              <p className="text-sm text-muted-foreground">İletişim sekmesi</p>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}
