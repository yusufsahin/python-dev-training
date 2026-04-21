import { Card } from "../ui/card";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Button } from "../ui/button";
import { Textarea } from "../ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Switch } from "../ui/switch";
import { Checkbox } from "../ui/checkbox";
import { RadioGroup, RadioGroupItem } from "../ui/radio-group";

export function FormShowcase() {
  return (
    <div className="space-y-8">
      <Card className="p-6">
        <h3 className="mb-6">Temel Form Elemanları</h3>
        <div className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="customer">Müşteri Adı</Label>
            <Input id="customer" placeholder="Müşteri adını giriniz" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="amount">Tutar (₺)</Label>
            <Input id="amount" type="number" placeholder="0.00" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Açıklama</Label>
            <Textarea id="description" placeholder="Teklif detaylarını yazınız" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="category">Kategori</Label>
            <Select>
              <SelectTrigger id="category">
                <SelectValue placeholder="Kategori seçiniz" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="product">Ürün Satışı</SelectItem>
                <SelectItem value="service">Hizmet</SelectItem>
                <SelectItem value="subscription">Abonelik</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-6">Toggle ve Seçim Elemanları</h3>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <Label htmlFor="auto-send">Otomatik Gönderim</Label>
            <Switch id="auto-send" />
          </div>

          <div className="space-y-3">
            <Label>Fatura Tipi</Label>
            <RadioGroup defaultValue="sales">
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="sales" id="sales" />
                <Label htmlFor="sales" className="font-normal">
                  Satış Faturası
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="purchase" id="purchase" />
                <Label htmlFor="purchase" className="font-normal">
                  Alış Faturası
                </Label>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-3">
            <Label>Özellikler</Label>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Checkbox id="vat" />
                <Label htmlFor="vat" className="font-normal">
                  KDV Dahil
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox id="discount" />
                <Label htmlFor="discount" className="font-normal">
                  İskonto Uygula
                </Label>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-6">Form Durumları</h3>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="normal">Normal</Label>
            <Input id="normal" placeholder="Normal durum" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="disabled">Disabled</Label>
            <Input id="disabled" placeholder="Değiştirilemez" disabled />
          </div>

          <div className="space-y-2">
            <Label htmlFor="error">Hata Durumu</Label>
            <Input
              id="error"
              placeholder="Geçersiz değer"
              className="border-destructive"
            />
            <p className="text-sm text-destructive">Bu alan zorunludur</p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="success">Başarılı</Label>
            <Input
              id="success"
              value="Geçerli değer"
              className="border-green-500"
              readOnly
            />
            <p className="text-sm text-green-600">Doğrulandı</p>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-6">Form Aksiyonları</h3>
        <div className="flex flex-wrap gap-3">
          <Button>Kaydet</Button>
          <Button variant="secondary">İptal</Button>
          <Button variant="outline">Önizle</Button>
        </div>
      </Card>
    </div>
  );
}
