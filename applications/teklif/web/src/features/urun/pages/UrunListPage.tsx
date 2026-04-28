import { MoreHorizontal, Package, Pencil, Plus, Trash2 } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useListUrunlerQuery } from '@/store/api/baseApi'
import { getErrorMessage } from '@/store/api/getErrorMessage'
import { replaceModal } from '@/store/slices/modalSlice'
import { useAppDispatch } from '@/store/hooks'

const tl = new Intl.NumberFormat('tr-TR', {
  style: 'currency',
  currency: 'TRY',
  minimumFractionDigits: 2,
})

export function UrunListPage() {
  const dispatch = useAppDispatch()
  const { data: rows = [], isFetching, isError, refetch, error } = useListUrunlerQuery()
  const errorMessage = getErrorMessage(error, 'Ürün/hizmet listesi yüklenemedi.')

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-4 py-6 sm:px-6">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">Ürün / hizmet</h1>
          <p className="text-sm text-muted-foreground">
            Epic 2 — Katalog kartları; CRUD modallarla yönetim (mock).
          </p>
        </div>
        <Button
          className="w-full shrink-0 sm:w-auto"
          onClick={() => dispatch(replaceModal({ key: 'urun:create' }))}
        >
          <Plus className="size-4" />
          Yeni kart
        </Button>
      </header>

      {isError ? (
        <Card>
          <CardHeader>
            <CardTitle>Yüklenemedi</CardTitle>
            <CardDescription>{errorMessage}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button variant="secondary" onClick={() => void refetch()}>
              Yenile
            </Button>
          </CardContent>
        </Card>
      ) : null}

      <div className="flex flex-col gap-3 md:hidden">
        {isFetching ? (
          <p className="text-sm text-muted-foreground">Yükleniyor…</p>
        ) : (
          rows.map((r) => (
            <Card key={r.id}>
              <CardHeader className="pb-2">
                <div className="flex items-start justify-between gap-2">
                  <CardTitle className="text-base">{r.ad}</CardTitle>
                  <Badge variant={r.tur === 'URUN' ? 'default' : 'secondary'}>
                    {r.tur === 'URUN' ? 'Ürün' : 'Hizmet'}
                  </Badge>
                </div>
                <CardDescription className="text-xs">
                  {r.sku} · {r.birim} · KDV %{r.kdvOrani}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex flex-col gap-2 pt-0">
                <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
                  <span>{r.kategori}</span>
                  <span>·</span>
                  <span>{r.fiyatListesiAdi}</span>
                  {!r.aktif ? (
                    <Badge variant="outline" className="text-xs">
                      Pasif
                    </Badge>
                  ) : null}
                </div>
                <p className="text-sm font-medium">{tl.format(r.satisFiyati)}</p>
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => dispatch(replaceModal({ key: 'urun:edit', urunId: r.id }))}
                  >
                    <Pencil className="size-3.5" />
                    Düzenle
                  </Button>
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() =>
                      dispatch(
                        replaceModal({
                          key: 'urun:delete',
                          urunId: r.id,
                          label: r.ad,
                        }),
                      )
                    }
                  >
                    <Trash2 className="size-3.5" />
                    Sil
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      <Card className="hidden overflow-hidden md:block">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Ad</TableHead>
              <TableHead className="hidden lg:table-cell">Tür</TableHead>
              <TableHead>SKU</TableHead>
              <TableHead className="hidden xl:table-cell">Birim</TableHead>
              <TableHead className="text-right">KDV</TableHead>
              <TableHead className="hidden lg:table-cell text-right">Satış</TableHead>
              <TableHead className="hidden xl:table-cell">Kategori</TableHead>
              <TableHead className="w-[72px] text-right">İşlem</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isFetching ? (
              <TableRow>
                <TableCell colSpan={8} className="text-muted-foreground">
                  Yükleniyor…
                </TableCell>
              </TableRow>
            ) : (
              rows.map((r) => (
                <TableRow key={r.id} className={!r.aktif ? 'opacity-70' : undefined}>
                  <TableCell>
                    <div className="flex items-center gap-2 font-medium">
                      <Package className="size-4 shrink-0 text-muted-foreground" aria-hidden />
                      {r.ad}
                      {!r.aktif ? (
                        <Badge variant="outline" className="text-[10px]">
                          Pasif
                        </Badge>
                      ) : null}
                    </div>
                  </TableCell>
                  <TableCell className="hidden lg:table-cell">
                    <Badge variant={r.tur === 'URUN' ? 'default' : 'secondary'}>
                      {r.tur === 'URUN' ? 'Ürün' : 'Hizmet'}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-mono text-xs">{r.sku}</TableCell>
                  <TableCell className="hidden xl:table-cell">{r.birim}</TableCell>
                  <TableCell className="text-right">%{r.kdvOrani}</TableCell>
                  <TableCell className="hidden text-right font-medium lg:table-cell">
                    {tl.format(r.satisFiyati)}
                  </TableCell>
                  <TableCell className="hidden xl:table-cell">{r.kategori}</TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button size="icon" variant="ghost" aria-label="İşlemler">
                          <MoreHorizontal className="size-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          onClick={() => dispatch(replaceModal({ key: 'urun:edit', urunId: r.id }))}
                        >
                          <Pencil className="size-4" />
                          Düzenle
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          variant="destructive"
                          onClick={() =>
                            dispatch(
                              replaceModal({
                                key: 'urun:delete',
                                urunId: r.id,
                                label: r.ad,
                              }),
                            )
                          }
                        >
                          <Trash2 className="size-4" />
                          Sil
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </Card>
    </div>
  )
}
