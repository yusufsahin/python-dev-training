import {
  AlertCircle,
  BarChart3,
  Building2,
  Calendar,
  Check,
  Clock,
  CreditCard,
  DollarSign,
  Download,
  Edit,
  Eye,
  FileText,
  Filter,
  Info,
  Mail,
  MapPin,
  Minus,
  Package,
  Phone,
  PieChart,
  Plus,
  Receipt,
  Search,
  Settings,
  ShoppingCart,
  Trash2,
  TrendingUp,
  Upload,
  Users,
  Wallet,
  X,
} from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'

export function IconsShowcase() {
  const iconGroups = [
    {
      title: 'Modül ikonları',
      icons: [
        { Icon: FileText, name: 'Teklif' },
        { Icon: Users, name: 'Cari' },
        { Icon: Package, name: 'Ürün / stok' },
        { Icon: CreditCard, name: 'Ödeme' },
        { Icon: Receipt, name: 'Fatura' },
        { Icon: Wallet, name: 'Kasa / banka' },
        { Icon: ShoppingCart, name: 'Sipariş' },
        { Icon: BarChart3, name: 'Raporlar' },
      ],
    },
    {
      title: 'Aksiyon ikonları',
      icons: [
        { Icon: Plus, name: 'Ekle' },
        { Icon: Edit, name: 'Düzenle' },
        { Icon: Trash2, name: 'Sil' },
        { Icon: Eye, name: 'Görüntüle' },
        { Icon: Download, name: 'İndir' },
        { Icon: Upload, name: 'Yükle' },
        { Icon: Check, name: 'Onayla' },
        { Icon: X, name: 'İptal' },
      ],
    },
    {
      title: 'Durum ikonları',
      icons: [
        { Icon: AlertCircle, name: 'Uyarı' },
        { Icon: Info, name: 'Bilgi' },
        { Icon: Check, name: 'Başarılı' },
        { Icon: X, name: 'Hata' },
        { Icon: Clock, name: 'Bekliyor' },
        { Icon: TrendingUp, name: 'Artış' },
      ],
    },
    {
      title: 'Yardımcı ikonlar',
      icons: [
        { Icon: Search, name: 'Ara' },
        { Icon: Filter, name: 'Filtre' },
        { Icon: Calendar, name: 'Tarih' },
        { Icon: Settings, name: 'Ayarlar' },
        { Icon: Mail, name: 'E-posta' },
        { Icon: Phone, name: 'Telefon' },
        { Icon: MapPin, name: 'Konum' },
        { Icon: Building2, name: 'Şirket' },
      ],
    },
    {
      title: 'Finansal ikonlar',
      icons: [
        { Icon: DollarSign, name: 'Para' },
        { Icon: TrendingUp, name: 'Gelir' },
        { Icon: PieChart, name: 'Dağılım' },
        { Icon: BarChart3, name: 'Analiz' },
        { Icon: Minus, name: 'Düşüş' },
      ],
    },
  ]

  return (
    <div className="space-y-8">
      {iconGroups.map((group) => (
        <Card key={group.title}>
          <CardContent className="p-6">
            <h3 className="mb-6">{group.title}</h3>
            <div className="grid grid-cols-2 gap-6 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8">
              {group.icons.map(({ Icon, name }) => (
                <div key={name} className="flex flex-col items-center gap-2 text-center">
                  <div className="rounded-lg bg-muted p-3">
                    <Icon className="size-6" aria-hidden />
                  </div>
                  <span className="text-xs text-muted-foreground">{name}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      ))}

      <Card>
        <CardContent className="p-6">
          <h3 className="mb-4">İkon boyutları</h3>
          <div className="flex flex-wrap items-center gap-8">
            <div className="flex flex-col items-center gap-2">
              <FileText className="size-4" aria-hidden />
              <span className="text-xs">16px</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <FileText className="size-5" aria-hidden />
              <span className="text-xs">20px</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <FileText className="size-6" aria-hidden />
              <span className="text-xs">24px</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <FileText className="size-8" aria-hidden />
              <span className="text-xs">32px</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-2 p-6 text-sm">
          <h3 className="mb-2">Kullanım</h3>
          <p>
            <strong>Paket:</strong> lucide-react
          </p>
          <p>
            <strong>Boyut:</strong> Buton içinde genelde <code className="text-xs">size-4</code>, metin
            yanında <code className="text-xs">size-5</code>
          </p>
          <p>
            <strong>Renk:</strong> <code className="text-xs">text-muted-foreground</code> vb. ile özelleştirin
          </p>
          <p>
            <strong>Erişilebilirlik:</strong> Dekoratif ikonlarda <code className="text-xs">aria-hidden</code>;
            tek başına kullanımda <code className="text-xs">aria-label</code>
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
