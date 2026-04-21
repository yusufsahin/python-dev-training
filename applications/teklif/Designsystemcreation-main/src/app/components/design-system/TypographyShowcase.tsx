import { Card } from "../ui/card";

export function TypographyShowcase() {
  return (
    <div className="space-y-6">
      <Card className="p-6">
        <h1>Başlık 1 - Ana Sayfa Başlıkları</h1>
        <p className="text-sm text-muted-foreground mt-1">
          font-size: 2xl, font-weight: medium
        </p>
      </Card>

      <Card className="p-6">
        <h2>Başlık 2 - Bölüm Başlıkları</h2>
        <p className="text-sm text-muted-foreground mt-1">
          font-size: xl, font-weight: medium
        </p>
      </Card>

      <Card className="p-6">
        <h3>Başlık 3 - Alt Bölüm Başlıkları</h3>
        <p className="text-sm text-muted-foreground mt-1">
          font-size: lg, font-weight: medium
        </p>
      </Card>

      <Card className="p-6">
        <h4>Başlık 4 - Kart Başlıkları</h4>
        <p className="text-sm text-muted-foreground mt-1">
          font-size: base, font-weight: medium
        </p>
      </Card>

      <Card className="p-6">
        <p>
          Normal paragraf metni. Açıklamalar, bilgilendirme metinleri ve genel
          içerik için kullanılır.
        </p>
        <p className="text-sm text-muted-foreground mt-1">
          font-size: base, font-weight: normal
        </p>
      </Card>

      <Card className="p-6">
        <p className="text-sm text-muted-foreground">
          Küçük metin. Form yardım metinleri, açıklayıcı bilgiler ve
          meta bilgiler için kullanılır.
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          font-size: sm
        </p>
      </Card>

      <Card className="p-6">
        <p className="text-xs text-muted-foreground">
          Çok küçük metin. Timestamp, etiketler ve kod snippet'leri için kullanılır.
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          font-size: xs
        </p>
      </Card>
    </div>
  );
}
