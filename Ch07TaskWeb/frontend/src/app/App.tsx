import { useState, useEffect, useCallback } from "react";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Select } from "./components/ui/select";
import { TaskForm } from "./components/TaskForm";
import { CategoryManager } from "./components/CategoryManager";
import { TaskTable } from "./components/TaskTable";
import type { Task, Category, TaskFormData } from "./types";
import { STATUS_LABELS, PRIORITY_LABELS } from "./types";
import * as api from "../api/client";

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [filters, setFilters] = useState<{
    status: string;
    priority: string;
    category_id: string;
    search: string;
  }>({
    status: "",
    priority: "",
    category_id: "",
    search: "",
  });
  const [formOpen, setFormOpen] = useState(false);
  const [categoryManagerOpen, setCategoryManagerOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);

  const loadTasks = useCallback(async () => {
    setLoading(true);
    try {
      const list = await api.getTasks({
        status: filters.status || undefined,
        priority: filters.priority ? Number(filters.priority) : undefined,
        category_id: filters.category_id ? Number(filters.category_id) : undefined,
        search: filters.search || undefined,
      });
      setTasks(list);
    } finally {
      setLoading(false);
    }
  }, [filters.status, filters.priority, filters.category_id, filters.search]);

  const loadCategories = useCallback(async () => {
    const list = await api.getCategories();
    setCategories(list);
  }, []);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  useEffect(() => {
    loadCategories();
  }, [loadCategories]);

  const openCreateForm = () => {
    setSelectedTask(null);
    setFormOpen(true);
  };

  const openEditForm = (task: Task) => {
    setSelectedTask(task);
    setFormOpen(true);
  };

  const handleFormSubmit = async (data: TaskFormData, taskId?: number) => {
    if (taskId) {
      await api.updateTask(taskId, data);
    } else {
      await api.createTask(data);
    }
    await loadTasks();
  };

  const handleDeleteTask = async (task: Task) => {
    if (!window.confirm(`"${task.title}" görevini silmek istediğinize emin misiniz?`)) return;
    await api.deleteTask(task.id);
    await loadTasks();
  };

  return (
    <div className="min-h-screen p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Görev Yöneticisi</h1>

      <div className="flex flex-wrap gap-4 mb-4">
        <div className="flex items-center gap-2">
          <Label htmlFor="filter-status" className="text-slate-600">Durum</Label>
          <Select
            id="filter-status"
            value={filters.status}
            onChange={(e) => setFilters((f) => ({ ...f, status: e.target.value }))}
            className="w-[140px]"
          >
            <option value="">Tümü</option>
            {Object.entries(STATUS_LABELS).map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </Select>
        </div>
        <div className="flex items-center gap-2">
          <Label htmlFor="filter-priority" className="text-slate-600">Öncelik</Label>
          <Select
            id="filter-priority"
            value={filters.priority}
            onChange={(e) => setFilters((f) => ({ ...f, priority: e.target.value }))}
            className="w-[120px]"
          >
            <option value="">Tümü</option>
            {Object.entries(PRIORITY_LABELS).map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </Select>
        </div>
        <div className="flex items-center gap-2">
          <Label htmlFor="filter-category" className="text-slate-600">Kategori</Label>
          <Select
            id="filter-category"
            value={filters.category_id}
            onChange={(e) => setFilters((f) => ({ ...f, category_id: e.target.value }))}
            className="w-[140px]"
          >
            <option value="">Tümü</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </Select>
        </div>
        <div className="flex items-center gap-2">
          <Label htmlFor="filter-search" className="text-slate-600">Arama</Label>
          <Input
            id="filter-search"
            placeholder="Başlık / açıklama"
            value={filters.search}
            onChange={(e) => setFilters((f) => ({ ...f, search: e.target.value }))}
            className="w-[180px]"
          />
        </div>
        <div className="flex gap-2 ml-auto">
          <Button variant="outline" onClick={() => setCategoryManagerOpen(true)}>
            Kategori Yönet
          </Button>
          <Button onClick={openCreateForm}>Yeni Görev</Button>
        </div>
      </div>

      <div className="rounded-md border border-slate-200 bg-white">
        {loading ? (
          <p className="p-4 text-slate-500">Yükleniyor…</p>
        ) : (
          <TaskTable
            tasks={tasks}
            onEdit={openEditForm}
            onDelete={handleDeleteTask}
          />
        )}
      </div>

      <TaskForm
        open={formOpen}
        onOpenChange={setFormOpen}
        categories={categories}
        initial={
          selectedTask
            ? {
                title: selectedTask.title,
                description: selectedTask.description,
                priority: selectedTask.priority,
                status: selectedTask.status,
                due_date: selectedTask.due_date ?? "",
                category_id: selectedTask.category_id,
              }
            : null
        }
        taskId={selectedTask?.id ?? null}
        onSubmit={handleFormSubmit}
      />

      <CategoryManager
        open={categoryManagerOpen}
        onOpenChange={setCategoryManagerOpen}
        onCategoriesChange={loadCategories}
      />
    </div>
  );
}
