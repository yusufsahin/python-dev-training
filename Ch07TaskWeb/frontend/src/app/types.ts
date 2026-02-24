export interface Category {
  id: number;
  name: string;
  color: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  priority: number;
  status: string;
  due_date: string | null;
  category_id: number | null;
  created_at: string;
  updated_at: string;
  category_name?: string | null;
  category_color?: string | null;
}

export interface TaskFormData {
  title: string;
  description: string;
  priority: number;
  status: string;
  due_date: string;
  category_id: number | null;
}

export const PRIORITY_LABELS: Record<number, string> = {
  1: "Düşük",
  2: "Normal",
  3: "Yüksek",
  4: "Acil",
};

export const STATUS_LABELS: Record<string, string> = {
  todo: "Yapılacak",
  in_progress: "Devam",
  done: "Tamamlandı",
  cancelled: "İptal",
};
