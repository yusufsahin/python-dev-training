import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

export function DataDisplayShowcase() {
  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle>Teklif listesi</CardTitle>
          <CardDescription>Son 30 günde oluşturulan teklifler</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Teklif no</TableHead>
                <TableHead>Müşteri</TableHead>
                <TableHead>Tutar</TableHead>
                <TableHead>Durum</TableHead>
                <TableHead className="text-right">Tarih</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell className="font-medium">TKL-2026-001</TableCell>
                <TableCell>Acme A.Ş.</TableCell>
                <TableCell>₺125.450,00</TableCell>
                <TableCell>
                  <Badge variant="default">Onaylandı</Badge>
                </TableCell>
                <TableCell className="text-right">21.04.2026</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="font-medium">TKL-2026-002</TableCell>
                <TableCell>Beta Ltd.</TableCell>
                <TableCell>₺48.900,00</TableCell>
                <TableCell>
                  <Badge variant="secondary">Gönderildi</Badge>
                </TableCell>
                <TableCell className="text-right">20.04.2026</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="font-medium">TKL-2026-003</TableCell>
                <TableCell>Gamma Yazılım</TableCell>
                <TableCell>₺210.000,00</TableCell>
                <TableCell>
                  <Badge variant="outline">Taslak</Badge>
                </TableCell>
                <TableCell className="text-right">19.04.2026</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="font-medium">TKL-2026-004</TableCell>
                <TableCell>Delta Teknoloji</TableCell>
                <TableCell>₺89.250,00</TableCell>
                <TableCell>
                  <Badge className="bg-red-500 text-white hover:bg-red-500/90">Reddedildi</Badge>
                </TableCell>
                <TableCell className="text-right">18.04.2026</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Toplam satış</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₺473.600</div>
            <p className="text-xs text-muted-foreground">+20,1% geçen aya göre</p>
            <Progress value={75} className="mt-3" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Bekleyen tahsilat</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₺127.350</div>
            <p className="text-xs text-muted-foreground">15 fatura</p>
            <Progress value={45} className="mt-3" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Yeni müşteri</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">+24</div>
            <p className="text-xs text-muted-foreground">Bu ay</p>
            <Progress value={60} className="mt-3" />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Durum rozetleri</CardTitle>
          <CardDescription>Teklif, fatura ve ödeme durumları</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            <Badge>Onaylandı</Badge>
            <Badge variant="secondary">Gönderildi</Badge>
            <Badge variant="outline">Taslak</Badge>
            <Badge variant="destructive">İptal</Badge>
            <Badge className="bg-green-600 text-white hover:bg-green-600/90">Ödendi</Badge>
            <Badge className="bg-yellow-500 text-black hover:bg-yellow-500/90">Beklemede</Badge>
            <Badge className="bg-orange-500 text-white hover:bg-orange-500/90">Gecikti</Badge>
            <Badge className="bg-blue-600 text-white hover:bg-blue-600/90">İşlemde</Badge>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Avatar</CardTitle>
          <CardDescription>Kullanıcı ve müşteri kısaltmaları</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap items-center gap-4">
            <Avatar>
              <AvatarFallback>AA</AvatarFallback>
            </Avatar>
            <Avatar>
              <AvatarFallback className="bg-primary text-primary-foreground">BL</AvatarFallback>
            </Avatar>
            <Avatar>
              <AvatarFallback className="bg-secondary text-secondary-foreground">GY</AvatarFallback>
            </Avatar>
            <Avatar>
              <AvatarFallback className="bg-muted text-muted-foreground">DT</AvatarFallback>
            </Avatar>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
