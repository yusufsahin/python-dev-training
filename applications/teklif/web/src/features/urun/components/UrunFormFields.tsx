import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import type { UseFormReturn } from 'react-hook-form'
import type { UrunFormValues } from '@/features/urun/schemas/urunFormSchema'

const birimler = ['Adet', 'Kg', 'Saat', 'Paket', 'Ay', 'm²', 'Metre', 'Litre', 'Set'] as const

export function UrunFormFields({ form }: { form: UseFormReturn<UrunFormValues> }) {
  return (
    <div className="grid gap-4">
      <FormField
        control={form.control}
        name="tur"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Tür</FormLabel>
            <FormControl>
              <RadioGroup
                onValueChange={field.onChange}
                value={field.value}
                className="flex flex-wrap gap-4"
              >
                <div className="flex items-center gap-2">
                  <RadioGroupItem value="URUN" id="urun-tur-urun" />
                  <Label htmlFor="urun-tur-urun" className="font-normal">
                    Ürün
                  </Label>
                </div>
                <div className="flex items-center gap-2">
                  <RadioGroupItem value="HIZMET" id="urun-tur-hizmet" />
                  <Label htmlFor="urun-tur-hizmet" className="font-normal">
                    Hizmet
                  </Label>
                </div>
              </RadioGroup>
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="ad"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Ad</FormLabel>
            <FormControl>
              <Input placeholder="Ürün veya hizmet adı" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <div className="grid gap-4 sm:grid-cols-2">
        <FormField
          control={form.control}
          name="sku"
          render={({ field }) => (
            <FormItem>
              <FormLabel>SKU</FormLabel>
              <FormControl>
                <Input placeholder="Stok kodu" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="barkod"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Barkod</FormLabel>
              <FormControl>
                <Input placeholder="İsteğe bağlı" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <FormField
          control={form.control}
          name="birim"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Birim</FormLabel>
              <Select onValueChange={field.onChange} value={field.value}>
                <FormControl>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Birim seçin" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {birimler.map((b) => (
                    <SelectItem key={b} value={b}>
                      {b}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="kdvOrani"
          render={({ field }) => (
            <FormItem>
              <FormLabel>KDV (%)</FormLabel>
              <Select
                onValueChange={(v) => field.onChange(Number(v))}
                value={String(field.value)}
              >
                <FormControl>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="KDV" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {[0, 1, 8, 10, 18, 20].map((k) => (
                    <SelectItem key={k} value={String(k)}>
                      %{k}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <FormField
          control={form.control}
          name="satisFiyati"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Satış fiyatı (₺)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  inputMode="decimal"
                  min={0}
                  step="0.01"
                  value={Number.isFinite(field.value) ? field.value : 0}
                  onChange={(e) => {
                    const v = e.target.value
                    field.onChange(v === '' ? 0 : parseFloat(v))
                  }}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="alisFiyati"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Alış fiyatı (₺)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  inputMode="decimal"
                  min={0}
                  step="0.01"
                  value={Number.isFinite(field.value) ? field.value : 0}
                  onChange={(e) => {
                    const v = e.target.value
                    field.onChange(v === '' ? 0 : parseFloat(v))
                  }}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </div>

      <FormField
        control={form.control}
        name="kategori"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Kategori</FormLabel>
            <FormControl>
              <Input placeholder="Örn. Yazılım, Ofis, Hammadde" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="fiyatListesiAdi"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Fiyat listesi</FormLabel>
            <FormControl>
              <Input placeholder="Örn. Genel, Bayi A" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="dovizKodu"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Para birimi (MVP)</FormLabel>
            <FormControl>
              <Input {...field} disabled className="bg-muted" />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="aktif"
        render={({ field }) => (
          <FormItem className="flex flex-row items-center justify-between rounded-lg border p-3">
            <div className="space-y-0.5">
              <FormLabel>Aktif</FormLabel>
              <p className="text-xs text-muted-foreground">Pasif kalemler teklifte önerilmez.</p>
            </div>
            <FormControl>
              <Switch checked={field.value} onCheckedChange={field.onChange} />
            </FormControl>
          </FormItem>
        )}
      />
    </div>
  )
}
