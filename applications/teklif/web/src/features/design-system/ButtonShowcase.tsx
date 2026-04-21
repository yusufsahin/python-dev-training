import { Download, FileText, Plus, Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

export function ButtonShowcase() {
  return (
    <div className="space-y-8">
      <Card>
        <CardContent className="space-y-4 p-6">
          <h3>Buton varyantları</h3>
          <div className="flex flex-wrap gap-3">
            <Button>Varsayılan</Button>
            <Button variant="secondary">İkincil</Button>
            <Button variant="outline">Çerçeveli</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="destructive">Sil</Button>
            <Button variant="link">Link</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-4 p-6">
          <h3>Buton boyutları</h3>
          <div className="flex flex-wrap items-center gap-3">
            <Button size="sm">Küçük</Button>
            <Button size="default">Normal</Button>
            <Button size="lg">Büyük</Button>
            <Button size="icon" aria-label="Ekle">
              <Plus className="size-4" />
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-4 p-6">
          <h3>İkonlu butonlar</h3>
          <div className="flex flex-wrap gap-3">
            <Button>
              <Plus className="size-4" />
              Yeni teklif
            </Button>
            <Button variant="secondary">
              <FileText className="size-4" />
              Fatura oluştur
            </Button>
            <Button variant="outline">
              <Download className="size-4" />
              Export
            </Button>
            <Button variant="destructive">
              <Trash2 className="size-4" />
              Sil
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-4 p-6">
          <h3>Disabled</h3>
          <div className="flex flex-wrap gap-3">
            <Button disabled>Varsayılan</Button>
            <Button variant="secondary" disabled>
              İkincil
            </Button>
            <Button variant="outline" disabled>
              Çerçeveli
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-3 p-6 text-sm">
          <h3>Kullanım önerileri</h3>
          <p>
            <strong>Primary (varsayılan):</strong> Ana CTA — «Teklif oluştur», «Kaydet», «Onayla»
          </p>
          <p>
            <strong>Secondary:</strong> İkincil aksiyon — «İptal», «Geri», «Düzenle»
          </p>
          <p>
            <strong>Outline:</strong> «Export», «Filtrele», «Önizle»
          </p>
          <p>
            <strong>Destructive:</strong> Silme ve geri alınamaz işlemler
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
