import { Button } from "../ui/button";
import { Card } from "../ui/card";
import { FileText, Download, Trash2, Plus } from "lucide-react";

export function ButtonShowcase() {
  return (
    <div className="space-y-8">
      <Card className="p-6">
        <h3 className="mb-4">Buton Varyantları</h3>
        <div className="flex flex-wrap gap-3">
          <Button>Varsayılan</Button>
          <Button variant="secondary">İkincil</Button>
          <Button variant="outline">Çerçeveli</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="destructive">Sil</Button>
          <Button variant="link">Link</Button>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-4">Buton Boyutları</h3>
        <div className="flex flex-wrap items-center gap-3">
          <Button size="sm">Küçük</Button>
          <Button size="default">Normal</Button>
          <Button size="lg">Büyük</Button>
          <Button size="icon">
            <Plus className="h-4 w-4" />
          </Button>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-4">İkonlu Butonlar</h3>
        <div className="flex flex-wrap gap-3">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Yeni Teklif
          </Button>
          <Button variant="secondary">
            <FileText className="mr-2 h-4 w-4" />
            Fatura Oluştur
          </Button>
          <Button variant="outline">
            <Download className="mr-2 h-4 w-4" />
            Export
          </Button>
          <Button variant="destructive">
            <Trash2 className="mr-2 h-4 w-4" />
            Sil
          </Button>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-4">Disabled Durumlar</h3>
        <div className="flex flex-wrap gap-3">
          <Button disabled>Varsayılan</Button>
          <Button variant="secondary" disabled>
            İkincil
          </Button>
          <Button variant="outline" disabled>
            Çerçeveli
          </Button>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-4">Kullanım Önerileri</h3>
        <div className="space-y-3 text-sm">
          <div>
            <strong>Primary (Varsayılan):</strong> Ana CTA butonları - "Teklif
            Oluştur", "Kaydet", "Onayla"
          </div>
          <div>
            <strong>Secondary:</strong> İkincil aksiyonlar - "İptal", "Geri",
            "Düzenle"
          </div>
          <div>
            <strong>Outline:</strong> Alternatif aksiyonlar - "Export", "Filtrele",
            "Önizle"
          </div>
          <div>
            <strong>Destructive:</strong> Silme ve geri alınamaz işlemler - "Sil",
            "İptal Et", "Reddet"
          </div>
        </div>
      </Card>
    </div>
  );
}
