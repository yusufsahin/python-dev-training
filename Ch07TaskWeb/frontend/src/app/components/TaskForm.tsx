import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select } from "./ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "./ui/dialog";
import type { TaskFormData, Category } from "../types";
import { PRIORITY_LABELS, STATUS_LABELS } from "../types";

interface TaskFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  categories: Category[];
  initial?: TaskFormData | null;
  taskId?: number | null;
  onSubmit: (data: TaskFormData, taskId?: number) => Promise<void>;
}

const defaultForm: TaskFormData = {
  title: "",
  description: "",
  priority: 2,
  status: "todo",
  due_date: "",
  category_id: null,
};

export function TaskForm({
  open,
  onOpenChange,
  categories,
  initial,
  taskId,
  onSubmit,
}: TaskFormProps) {
  const [form, setForm] = useState<TaskFormData>(defaultForm);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (open) {
      setForm(
        initial
          ? {
              title: initial.title,
              description: initial.description ?? "",
              priority: initial.priority,
              status: initial.status,
              due_date: initial.due_date ?? "",
              category_id: initial.category_id ?? null,
            }
          : defaultForm
      );
    }
  }, [open, initial]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.title.trim()) return;
    setSaving(true);
    try {
      await onSubmit(form, taskId ?? undefined);
      onOpenChange(false);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>{taskId ? "Görevi Düzenle" : "Yeni Görev"}</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="title">Başlık *</Label>
              <Input
                id="title"
                value={form.title}
                onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
                placeholder="Görev başlığı"
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="description">Açıklama</Label>
              <textarea
                id="description"
                className="flex min-h-[80px] w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400"
                value={form.description}
                onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                placeholder="İsteğe bağlı açıklama"
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="priority">Öncelik</Label>
              <Select
                id="priority"
                value={form.priority}
                onChange={(e) => setForm((f) => ({ ...f, priority: Number(e.target.value) }))}
              >
                {Object.entries(PRIORITY_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </Select>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="status">Durum</Label>
              <Select
                id="status"
                value={form.status}
                onChange={(e) => setForm((f) => ({ ...f, status: e.target.value }))}
              >
                {Object.entries(STATUS_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </Select>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="due_date">Son Tarih</Label>
              <Input
                id="due_date"
                type="date"
                value={form.due_date}
                onChange={(e) => setForm((f) => ({ ...f, due_date: e.target.value }))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="category_id">Kategori</Label>
              <Select
                id="category_id"
                value={form.category_id ?? ""}
                onChange={(e) =>
                  setForm((f) => ({
                    ...f,
                    category_id: e.target.value ? Number(e.target.value) : null,
                  }))
                }
              >
                <option value="">Seçiniz</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              İptal
            </Button>
            <Button type="submit" disabled={saving}>
              {saving ? "Kaydediliyor…" : taskId ? "Güncelle" : "Ekle"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
