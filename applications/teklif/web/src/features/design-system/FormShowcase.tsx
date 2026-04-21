import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'

export function FormShowcase() {
  return (
    <div className="space-y-8">
      <Card>
        <CardContent className="space-y-6 p-6">
          <h3>Temel form elemanları</h3>
          <div className="space-y-2">
            <Label htmlFor="ds-customer">Müşteri adı</Label>
            <Input id="ds-customer" placeholder="Müşteri adını giriniz" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="ds-amount">Tutar (₺)</Label>
            <Input id="ds-amount" type="number" placeholder="0.00" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="ds-description">Açıklama</Label>
            <Textarea id="ds-description" placeholder="Teklif detaylarını yazınız" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="ds-category">Kategori</Label>
            <Select>
              <SelectTrigger id="ds-category" className="w-full">
                <SelectValue placeholder="Kategori seçiniz" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="product">Ürün satışı</SelectItem>
                <SelectItem value="service">Hizmet</SelectItem>
                <SelectItem value="subscription">Abonelik</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-6 p-6">
          <h3>Toggle ve seçim</h3>
          <div className="flex items-center justify-between gap-4">
            <Label htmlFor="ds-auto-send">Otomatik gönderim</Label>
            <Switch id="ds-auto-send" />
          </div>

          <div className="space-y-3">
            <Label>Fatura tipi</Label>
            <RadioGroup defaultValue="sales" className="space-y-2">
              <div className="flex items-center gap-2">
                <RadioGroupItem value="sales" id="ds-sales" />
                <Label htmlFor="ds-sales" className="font-normal">
                  Satış faturası
                </Label>
              </div>
              <div className="flex items-center gap-2">
                <RadioGroupItem value="purchase" id="ds-purchase" />
                <Label htmlFor="ds-purchase" className="font-normal">
                  Alış faturası
                </Label>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-3">
            <Label>Özellikler</Label>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Checkbox id="ds-vat" />
                <Label htmlFor="ds-vat" className="font-normal">
                  KDV dahil
                </Label>
              </div>
              <div className="flex items-center gap-2">
                <Checkbox id="ds-discount" />
                <Label htmlFor="ds-discount" className="font-normal">
                  İskonto uygula
                </Label>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-4 p-6">
          <h3>Form durumları</h3>
          <div className="space-y-2">
            <Label htmlFor="ds-normal">Normal</Label>
            <Input id="ds-normal" placeholder="Normal durum" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="ds-disabled-input">Disabled</Label>
            <Input id="ds-disabled-input" placeholder="Değiştirilemez" disabled />
          </div>

          <div className="space-y-2">
            <Label htmlFor="ds-error">Hata</Label>
            <Input id="ds-error" placeholder="Geçersiz değer" aria-invalid className="border-destructive" />
            <p className="text-sm text-destructive">Bu alan zorunludur</p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="ds-success">Başarılı</Label>
            <Input id="ds-success" defaultValue="Geçerli değer" readOnly className="border-green-600" />
            <p className="text-sm text-green-600">Doğrulandı</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="flex flex-wrap gap-3 p-6">
          <h3 className="sr-only">Form aksiyonları</h3>
          <Button>Kaydet</Button>
          <Button variant="secondary">İptal</Button>
          <Button variant="outline">Önizle</Button>
        </CardContent>
      </Card>
    </div>
  )
}
