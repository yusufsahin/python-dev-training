import { Card, CardContent } from '@/components/ui/card'

export function TypographyShowcase() {
  return (
    <div className="space-y-6">
      <Card>
        <CardContent className="p-6">
          <h1>Başlık 1 — Ana sayfa başlıkları</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            font-size: var(--text-2xl), font-weight: medium
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <h2>Başlık 2 — Bölüm başlıkları</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            font-size: var(--text-xl), font-weight: medium
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <h3>Başlık 3 — Alt bölüm başlıkları</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            font-size: var(--text-lg), font-weight: medium
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <h4>Başlık 4 — Kart başlıkları</h4>
          <p className="mt-1 text-sm text-muted-foreground">
            font-size: var(--text-base), font-weight: medium
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <p>
            Normal paragraf metni. Açıklamalar, bilgilendirme metinleri ve genel içerik için
            kullanılır.
          </p>
          <p className="mt-1 text-sm text-muted-foreground">
            font-size: var(--text-base), font-weight: normal
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <p className="text-sm text-muted-foreground">
            Küçük metin. Form yardım metinleri ve meta bilgiler için kullanılır.
          </p>
          <p className="mt-1 text-xs text-muted-foreground">Tailwind: text-sm</p>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <p className="text-xs text-muted-foreground">
            Çok küçük metin. Zaman damgası, etiketler ve kod snippet&apos;leri için kullanılır.
          </p>
          <p className="mt-1 text-xs text-muted-foreground">Tailwind: text-xs</p>
        </CardContent>
      </Card>
    </div>
  )
}
