import { FileText, Plus } from 'lucide-react'
import { useMemo, useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  useCreateTeklifMutation,
  useListCarilerQuery,
  useListTekliflerQuery,
  useListUrunlerQuery,
  useUpdateTeklifDurumMutation,
} from '@/store/api/baseApi'
import { getErrorMessage } from '@/store/api/getErrorMessage'

const tl = new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' })

export function TeklifListPage() {
  const { data: cariler = [] } = useListCarilerQuery()
  const { data: urunler = [] } = useListUrunlerQuery()
  const { data: teklifler = [], isFetching, isError, refetch, error } = useListTekliflerQuery()
  const [createTeklif, { isLoading: isCreating }] = useCreateTeklifMutation()
  const [updateDurum, { isLoading: isUpdatingDurum }] = useUpdateTeklifDurumMutation()
  const [createError, setCreateError] = useState<string | null>(null)

  const [cariId, setCariId] = useState('')
  const [urunId, setUrunId] = useState('')
  const [miktar, setMiktar] = useState(1)

  const seciliUrun = useMemo(() => urunler.find((u) => u.id === urunId), [urunId, urunler])

  const apiErrorMessage = getErrorMessage(error, 'Teklifler yüklenemedi.')

  const handleCreate = async () => {
    if (!cariId || !seciliUrun) {
      setCreateError('Cari ve ürün seçimi zorunludur.')
      return
    }
    try {
      setCreateError(null)
      await createTeklif({
        cariId,
        paraBirimi: 'TRY',
        kalemler: [
          {
            urunId: seciliUrun.id,
            miktar,
            birimFiyat: seciliUrun.satisFiyati,
            kdvOrani: seciliUrun.kdvOrani,
          },
        ],
      }).unwrap()
      setMiktar(1)
    } catch (e) {
      setCreateError(getErrorMessage(e, 'Teklif oluşturulamadı.'))
    }
  }

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-4 py-6 sm:px-6">
      <header className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">Teklifler</h1>
          <p className="text-sm text-muted-foreground">Cari ve ürünlerden hızlı teklif oluşturma.</p>
        </div>
      </header>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Yeni teklif oluştur</CardTitle>
          <CardDescription>İlk sürümde tek kalemli hızlı teklif.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <Label>Cari</Label>
            <Select value={cariId} onValueChange={setCariId}>
              <SelectTrigger>
                <SelectValue placeholder="Cari seçin" />
              </SelectTrigger>
              <SelectContent>
                {cariler.map((c) => (
                  <SelectItem key={c.id} value={c.id}>
                    {c.unvan}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label>Ürün / hizmet</Label>
            <Select value={urunId} onValueChange={setUrunId}>
              <SelectTrigger>
                <SelectValue placeholder="Ürün seçin" />
              </SelectTrigger>
              <SelectContent>
                {urunler.map((u) => (
                  <SelectItem key={u.id} value={u.id}>
                    {u.ad}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label>Miktar</Label>
            <Input
              type="number"
              min={1}
              step="1"
              value={miktar}
              onChange={(e) => setMiktar(Math.max(1, Number(e.target.value || 1)))}
            />
          </div>
          {createError ? (
            <p className="sm:col-span-3 text-sm text-destructive">{createError}</p>
          ) : null}
          <div className="sm:col-span-3">
            <Button onClick={() => void handleCreate()} disabled={isCreating} className="gap-2">
              <Plus className="size-4" />
              {isCreating ? 'Oluşturuluyor…' : 'Teklif oluştur'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {isError ? (
        <Card>
          <CardHeader>
            <CardTitle>Teklifler yüklenemedi</CardTitle>
            <CardDescription>{apiErrorMessage}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button variant="secondary" onClick={() => void refetch()}>
              Yenile
            </Button>
          </CardContent>
        </Card>
      ) : null}

      <div className="grid gap-3">
        {isFetching ? (
          <p className="text-sm text-muted-foreground">Yükleniyor…</p>
        ) : (
          teklifler.map((t) => (
            <Card key={t.id}>
              <CardContent className="flex flex-wrap items-center justify-between gap-3 py-4">
                <div className="flex items-center gap-3">
                  <FileText className="size-4 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">{t.id.slice(0, 8)}</p>
                    <p className="text-xs text-muted-foreground">
                      {new Date(t.createdAt).toLocaleString('tr-TR')}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Badge variant="secondary">{t.durum}</Badge>
                  <p className="text-sm font-semibold">{tl.format(t.genelToplam)}</p>
                  <Select
                    value={t.durum}
                    onValueChange={(durum) => {
                      void updateDurum({ id: t.id, durum: durum as typeof t.durum })
                    }}
                    disabled={isUpdatingDurum}
                  >
                    <SelectTrigger className="w-[140px]">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="TASLAK">TASLAK</SelectItem>
                      <SelectItem value="GONDERILDI">GONDERILDI</SelectItem>
                      <SelectItem value="ONAYLANDI">ONAYLANDI</SelectItem>
                      <SelectItem value="IPTAL">IPTAL</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}
