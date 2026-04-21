import { Card } from "../ui/card";
import { Separator } from "../ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";

export function LayoutShowcase() {
  return (
    <div className="space-y-8">
      <Card className="p-6">
        <h3 className="mb-6">Spacing Sistemi</h3>
        <div className="space-y-4">
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">space-1</div>
            <div className="bg-primary h-8" style={{ width: "0.25rem" }} />
            <span className="text-xs text-muted-foreground">4px</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">space-2</div>
            <div className="bg-primary h-8" style={{ width: "0.5rem" }} />
            <span className="text-xs text-muted-foreground">8px</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">space-3</div>
            <div className="bg-primary h-8" style={{ width: "0.75rem" }} />
            <span className="text-xs text-muted-foreground">12px</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">space-4</div>
            <div className="bg-primary h-8" style={{ width: "1rem" }} />
            <span className="text-xs text-muted-foreground">16px</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">space-6</div>
            <div className="bg-primary h-8" style={{ width: "1.5rem" }} />
            <span className="text-xs text-muted-foreground">24px</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-24 text-sm">space-8</div>
            <div className="bg-primary h-8" style={{ width: "2rem" }} />
            <span className="text-xs text-muted-foreground">32px</span>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-6">Border Radius</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="space-y-2">
            <div className="bg-primary h-20 rounded-sm" />
            <p className="text-sm text-center">rounded-sm</p>
          </div>
          <div className="space-y-2">
            <div className="bg-primary h-20 rounded-md" />
            <p className="text-sm text-center">rounded-md</p>
          </div>
          <div className="space-y-2">
            <div className="bg-primary h-20 rounded-lg" />
            <p className="text-sm text-center">rounded-lg</p>
          </div>
          <div className="space-y-2">
            <div className="bg-primary h-20 rounded-xl" />
            <p className="text-sm text-center">rounded-xl</p>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-6">Separator Kullanımı</h3>
        <div className="space-y-4">
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
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-6">Grid Layout</h3>
        <div className="space-y-6">
          <div>
            <p className="text-sm text-muted-foreground mb-3">
              2 Kolon (Mobil: 1, Tablet: 2)
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-muted p-4 rounded-lg">Kolon 1</div>
              <div className="bg-muted p-4 rounded-lg">Kolon 2</div>
            </div>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-3">
              3 Kolon (Mobil: 1, Tablet: 2, Desktop: 3)
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-muted p-4 rounded-lg">Kolon 1</div>
              <div className="bg-muted p-4 rounded-lg">Kolon 2</div>
              <div className="bg-muted p-4 rounded-lg">Kolon 3</div>
            </div>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-3">
              4 Kolon (Mobil: 2, Desktop: 4)
            </p>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-muted p-4 rounded-lg">Kolon 1</div>
              <div className="bg-muted p-4 rounded-lg">Kolon 2</div>
              <div className="bg-muted p-4 rounded-lg">Kolon 3</div>
              <div className="bg-muted p-4 rounded-lg">Kolon 4</div>
            </div>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-6">Tab Kullanımı</h3>
        <Tabs defaultValue="info" className="w-full">
          <TabsList>
            <TabsTrigger value="info">Genel Bilgiler</TabsTrigger>
            <TabsTrigger value="financial">Mali Bilgiler</TabsTrigger>
            <TabsTrigger value="contact">İletişim</TabsTrigger>
          </TabsList>
          <TabsContent value="info" className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Genel bilgiler sekmesi içeriği
            </p>
          </TabsContent>
          <TabsContent value="financial" className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Mali bilgiler sekmesi içeriği
            </p>
          </TabsContent>
          <TabsContent value="contact" className="space-y-4">
            <p className="text-sm text-muted-foreground">
              İletişim sekmesi içeriği
            </p>
          </TabsContent>
        </Tabs>
      </Card>
    </div>
  );
}
