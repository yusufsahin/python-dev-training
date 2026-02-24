import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";
import type { Category } from "../types";
import * as api from "../../api/client";

export function CategoryManager({
  open,
  onOpenChange,
  onCategoriesChange,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCategoriesChange?: () => void;
}) {
  const [categories, setCategories] = useState<Category[]>([]);
  const [newName, setNewName] = useState("");
  const [newColor, setNewColor] = useState("#808080");
  const [loading, setLoading] = useState(false);
  const [adding, setAdding] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const list = await api.getCategories();
      setCategories(list);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (open) load();
  }, [open]);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    setAdding(true);
    try {
      await api.createCategory(newName.trim(), newColor);
      setNewName("");
      setNewColor("#808080");
      await load();
      onCategoriesChange?.();
    } finally {
      setAdding(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm("Bu kategoriyi silmek istediğinize emin misiniz?")) return;
    try {
      await api.deleteCategory(id);
      await load();
      onCategoriesChange?.();
    } catch (err) {
      alert((err as Error).message);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Kategori Yönetimi</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleAdd} className="flex flex-wrap items-end gap-2 mb-4">
          <div className="flex-1 min-w-[120px]">
            <Label htmlFor="cat-name" className="sr-only">
              Kategori adı
            </Label>
            <Input
              id="cat-name"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="Kategori adı"
            />
          </div>
          <div className="w-24">
            <Label htmlFor="cat-color" className="sr-only">
              Renk
            </Label>
            <input
              id="cat-color"
              type="color"
              value={newColor}
              onChange={(e) => setNewColor(e.target.value)}
              className="h-10 w-full rounded border border-slate-200 cursor-pointer"
            />
          </div>
          <Button type="submit" disabled={adding || !newName.trim()}>
            Kategori Ekle
          </Button>
        </form>
        {loading ? (
          <p className="text-sm text-slate-500">Yükleniyor…</p>
        ) : (
          <ul className="space-y-2">
            {categories.map((c) => (
              <li
                key={c.id}
                className="flex items-center justify-between rounded-md border border-slate-200 px-3 py-2"
              >
                <span className="flex items-center gap-2">
                  <span
                    className="inline-block h-4 w-4 rounded-full border border-slate-300"
                    style={{ backgroundColor: c.color }}
                  />
                  {c.name}
                </span>
                <Button
                  type="button"
                  variant="destructive"
                  size="sm"
                  onClick={() => handleDelete(c.id)}
                >
                  Sil
                </Button>
              </li>
            ))}
            {categories.length === 0 && (
              <p className="text-sm text-slate-500">Henüz kategori yok.</p>
            )}
          </ul>
        )}
      </DialogContent>
    </Dialog>
  );
}
