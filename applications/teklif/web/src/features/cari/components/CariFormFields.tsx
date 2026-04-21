import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import type { UseFormReturn } from 'react-hook-form'
import type { CariFormValues } from '@/features/cari/schemas/cariFormSchema'

export function CariFormFields({ form }: { form: UseFormReturn<CariFormValues> }) {
  return (
    <div className="grid gap-4">
      <FormField
        control={form.control}
        name="unvan"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Ünvan</FormLabel>
            <FormControl>
              <Input autoComplete="organization" placeholder="Ticari ünvan" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="vergiNo"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Vergi no / TCKN</FormLabel>
            <FormControl>
              <Input inputMode="numeric" placeholder="10 veya 11 hane" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="eposta"
        render={({ field }) => (
          <FormItem>
            <FormLabel>E-posta</FormLabel>
            <FormControl>
              <Input type="email" autoComplete="email" placeholder="ornek@sirket.com" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="telefon"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Telefon</FormLabel>
            <FormControl>
              <Input type="tel" autoComplete="tel" placeholder="+90 …" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </div>
  )
}
