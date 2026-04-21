import { Card } from "../ui/card";
import {
  FileText,
  Users,
  Package,
  CreditCard,
  TrendingUp,
  Settings,
  Download,
  Upload,
  Trash2,
  Edit,
  Eye,
  Plus,
  Minus,
  X,
  Check,
  AlertCircle,
  Info,
  Search,
  Filter,
  Calendar,
  Clock,
  Mail,
  Phone,
  MapPin,
  DollarSign,
  BarChart3,
  PieChart,
  Home,
  Building2,
  ShoppingCart,
  Receipt,
  Wallet,
} from "lucide-react";

export function IconsShowcase() {
  const iconGroups = [
    {
      title: "Modül İkonları",
      icons: [
        { Icon: FileText, name: "Teklif" },
        { Icon: Users, name: "Cari" },
        { Icon: Package, name: "Ürün/Stok" },
        { Icon: CreditCard, name: "Ödeme" },
        { Icon: Receipt, name: "Fatura" },
        { Icon: Wallet, name: "Kasa/Banka" },
        { Icon: ShoppingCart, name: "Sipariş" },
        { Icon: BarChart3, name: "Raporlar" },
      ],
    },
    {
      title: "Aksiyon İkonları",
      icons: [
        { Icon: Plus, name: "Ekle" },
        { Icon: Edit, name: "Düzenle" },
        { Icon: Trash2, name: "Sil" },
        { Icon: Eye, name: "Görüntüle" },
        { Icon: Download, name: "İndir" },
        { Icon: Upload, name: "Yükle" },
        { Icon: Check, name: "Onayla" },
        { Icon: X, name: "İptal" },
      ],
    },
    {
      title: "Durum İkonları",
      icons: [
        { Icon: AlertCircle, name: "Uyarı" },
        { Icon: Info, name: "Bilgi" },
        { Icon: Check, name: "Başarılı" },
        { Icon: X, name: "Hata" },
        { Icon: Clock, name: "Bekliyor" },
        { Icon: TrendingUp, name: "Artış" },
      ],
    },
    {
      title: "Yardımcı İkonları",
      icons: [
        { Icon: Search, name: "Ara" },
        { Icon: Filter, name: "Filtre" },
        { Icon: Calendar, name: "Tarih" },
        { Icon: Settings, name: "Ayarlar" },
        { Icon: Mail, name: "E-posta" },
        { Icon: Phone, name: "Telefon" },
        { Icon: MapPin, name: "Konum" },
        { Icon: Building2, name: "Şirket" },
      ],
    },
    {
      title: "Finansal İkonlar",
      icons: [
        { Icon: DollarSign, name: "Para" },
        { Icon: TrendingUp, name: "Gelir" },
        { Icon: PieChart, name: "Dağılım" },
        { Icon: BarChart3, name: "Analiz" },
      ],
    },
  ];

  return (
    <div className="space-y-8">
      {iconGroups.map((group) => (
        <Card key={group.title} className="p-6">
          <h3 className="mb-6">{group.title}</h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-6">
            {group.icons.map(({ Icon, name }) => (
              <div key={name} className="flex flex-col items-center gap-2 text-center">
                <div className="p-3 rounded-lg bg-muted">
                  <Icon className="h-6 w-6" />
                </div>
                <span className="text-xs text-muted-foreground">{name}</span>
              </div>
            ))}
          </div>
        </Card>
      ))}

      <Card className="p-6">
        <h3 className="mb-4">İkon Boyutları</h3>
        <div className="flex items-center gap-8">
          <div className="flex flex-col items-center gap-2">
            <FileText className="h-4 w-4" />
            <span className="text-xs">Small (16px)</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <FileText className="h-5 w-5" />
            <span className="text-xs">Default (20px)</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <FileText className="h-6 w-6" />
            <span className="text-xs">Medium (24px)</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <FileText className="h-8 w-8" />
            <span className="text-xs">Large (32px)</span>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="mb-4">Kullanım Önerileri</h3>
        <div className="space-y-2 text-sm">
          <p>
            <strong>Paket:</strong> Tüm ikonlar için lucide-react paketi
            kullanılmaktadır.
          </p>
          <p>
            <strong>Boyut:</strong> Varsayılan h-5 w-5 (20px), buton içinde h-4 w-4
            (16px) kullanınız.
          </p>
          <p>
            <strong>Renk:</strong> İkonlar otomatik olarak metin rengini alır,
            text-* sınıfları ile özelleştirilebilir.
          </p>
          <p>
            <strong>Erişilebilirlik:</strong> Tek başına kullanılan ikonlara
            aria-label ekleyiniz.
          </p>
        </div>
      </Card>
    </div>
  );
}
