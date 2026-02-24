import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import type { Task } from "../types";
import { PRIORITY_LABELS, STATUS_LABELS } from "../types";

interface TaskTableProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
}

export function TaskTable({ tasks, onEdit, onDelete }: TaskTableProps) {
  const priorityVariant = (p: number) =>
    p >= 4 ? "destructive" : p >= 3 ? "default" : "secondary";

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Başlık</TableHead>
          <TableHead>Öncelik</TableHead>
          <TableHead>Durum</TableHead>
          <TableHead>Son Tarih</TableHead>
          <TableHead>Kategori</TableHead>
          <TableHead className="w-[100px]"></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {tasks.map((task) => (
          <TableRow
            key={task.id}
            className="cursor-pointer"
            onClick={() => onEdit(task)}
          >
            <TableCell className="font-medium">{task.title}</TableCell>
            <TableCell>
              <Badge variant={priorityVariant(task.priority)}>
                {PRIORITY_LABELS[task.priority] ?? task.priority}
              </Badge>
            </TableCell>
            <TableCell>
              <Badge variant="outline">
                {STATUS_LABELS[task.status] ?? task.status}
              </Badge>
            </TableCell>
            <TableCell>{task.due_date ?? "—"}</TableCell>
            <TableCell>
              {task.category_name ? (
                <span className="flex items-center gap-1.5">
                  <span
                    className="inline-block h-3 w-3 rounded-full border border-slate-300"
                    style={{ backgroundColor: task.category_color ?? "#808080" }}
                  />
                  {task.category_name}
                </span>
              ) : (
                "—"
              )}
            </TableCell>
            <TableCell onClick={(e) => e.stopPropagation()}>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => onDelete(task)}
              >
                Sil
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
