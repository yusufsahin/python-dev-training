import { Card, CardContent } from '@/components/ui/card'

export function ColorPalette() {
  const colors = [
    { name: 'Primary', var: '--primary', desc: 'Ana marka rengi, CTA butonlar' },
    { name: 'Secondary', var: '--secondary', desc: 'İkincil aksiyonlar' },
    { name: 'Accent', var: '--accent', desc: 'Vurgu alanları' },
    { name: 'Muted', var: '--muted', desc: 'Arkaplan ve disabled alanlar' },
    { name: 'Destructive', var: '--destructive', desc: 'Silme, iptal işlemleri' },
    { name: 'Background', var: '--background', desc: 'Ana arkaplan' },
    { name: 'Card', var: '--card', desc: 'Kart arkaplanları' },
    { name: 'Border', var: '--border', desc: 'Çerçeveler' },
  ]

  const chartColors = [
    { name: 'Chart 1', var: '--chart-1' },
    { name: 'Chart 2', var: '--chart-2' },
    { name: 'Chart 3', var: '--chart-3' },
    { name: 'Chart 4', var: '--chart-4' },
    { name: 'Chart 5', var: '--chart-5' },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h2 className="mb-4">Temel renkler</h2>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
          {colors.map((color) => (
            <Card key={color.name}>
              <CardContent className="p-4">
                <div
                  className="mb-3 h-24 w-full rounded-lg"
                  style={{ backgroundColor: `var(${color.var})` }}
                />
                <h4 className="mb-1">{color.name}</h4>
                <p className="text-sm text-muted-foreground">{color.desc}</p>
                <code className="mt-2 block text-xs text-muted-foreground">{color.var}</code>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      <div>
        <h2 className="mb-4">Grafik renkleri</h2>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-5">
          {chartColors.map((color) => (
            <Card key={color.name}>
              <CardContent className="p-4">
                <div
                  className="mb-2 h-16 w-full rounded-lg"
                  style={{ backgroundColor: `var(${color.var})` }}
                />
                <p className="text-sm">{color.name}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
