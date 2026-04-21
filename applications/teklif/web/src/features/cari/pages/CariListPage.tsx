import { MoreHorizontal, Pencil, Plus, Trash2 } from 'lucide-react'
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
import { useListCarilerQuery } from '@/store/api/baseApi'
import { replaceModal } from '@/store/slices/modalSlice'
import { useAppDispatch } from '@/store/hooks'

export function CariListPage() {
  const dispatch = useAppDispatch()
  const { data: rows = [], isFetching, isError, refetch } = useListCarilerQuery()

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-4 py-6 sm:px-6">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">Cariler</h1>
          <p className="text-sm text-muted-foreground">
            Epic 1 — UI-first örnek liste. CRUD işlemleri modallar üzerinden.
          </p>
        </div>
        <Button
          className="w-full shrink-0 sm:w-auto"
          onClick={() => dispatch(replaceModal({ key: 'cari:create' }))}
        >
          <Plus className="size-4" />
          Yeni cari
        </Button>
      </header>

      {isError ? (
        <Card>
          <CardHeader>
            <CardTitle>Yüklenemedi</CardTitle>
            <CardDescription>Mock API hata verdi. Tekrar deneyin.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button variant="secondary" onClick={() => void refetch()}>
              Yenile
            </Button>
          </CardContent>
        </Card>
      ) : null}

      {/* Mobil: kart listesi */}
      <div className="flex flex-col gap-3 md:hidden">
        {isFetching ? (
          <p className="text-sm text-muted-foreground">Yükleniyor…</p>
        ) : (
          rows.map((r) => (
            <Card key={r.id}>
              <CardHeader className="pb-2">
                <CardTitle className="text-base">{r.unvan}</CardTitle>
                <CardDescription className="text-xs">
                  {r.vergiNo} · {r.telefon}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex flex-wrap items-center justify-between gap-2 pt-0">
                <Badge variant="secondary">{r.eposta}</Badge>
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() =>
                      dispatch(replaceModal({ key: 'cari:edit', cariId: r.id }))
                    }
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
                          key: 'cari:delete',
                          cariId: r.id,
                          label: r.unvan,
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

      {/* md+: tablo */}
      <Card className="hidden overflow-hidden md:block">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Ünvan</TableHead>
              <TableHead className="hidden lg:table-cell">Vergi no</TableHead>
              <TableHead className="hidden xl:table-cell">E-posta</TableHead>
              <TableHead className="hidden lg:table-cell">Telefon</TableHead>
              <TableHead className="w-[72px] text-right">İşlem</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isFetching ? (
              <TableRow>
                <TableCell colSpan={5} className="text-muted-foreground">
                  Yükleniyor…
                </TableCell>
              </TableRow>
            ) : (
              rows.map((r) => (
                <TableRow key={r.id}>
                  <TableCell className="font-medium">{r.unvan}</TableCell>
                  <TableCell className="hidden lg:table-cell">{r.vergiNo}</TableCell>
                  <TableCell className="hidden xl:table-cell">{r.eposta}</TableCell>
                  <TableCell className="hidden lg:table-cell">{r.telefon}</TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button size="icon" variant="ghost" aria-label="İşlemler">
                          <MoreHorizontal className="size-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          onClick={() =>
                            dispatch(replaceModal({ key: 'cari:edit', cariId: r.id }))
                          }
                        >
                          <Pencil className="size-4" />
                          Düzenle
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          variant="destructive"
                          onClick={() =>
                            dispatch(
                              replaceModal({
                                key: 'cari:delete',
                                cariId: r.id,
                                label: r.unvan,
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
