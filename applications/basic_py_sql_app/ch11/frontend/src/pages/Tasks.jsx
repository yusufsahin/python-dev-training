import { useEffect, useMemo, useState } from "react";
import {
  Button,
  Col,
  Form,
  Modal,
  Row,
  Table,
} from "react-bootstrap";
import { createApiClient } from "../api/client.js";
import { useApp } from "../context/AppContext.jsx";

const EMPTY_FORM = {
  title: "",
  status: "todo",
  start_date: "",
  end_date: "",
};

function statusLabel(s) {
  const m = { todo: "Todo", in_progress: "In progress", done: "Done" };
  return m[s] || s;
}

function toYmd(d) {
  if (!d) return "";
  if (typeof d === "string") return d.slice(0, 10);
  return d;
}

export default function Tasks() {
  const { apiBase, dataRevision, bumpData, notify } = useApp();
  const api = useMemo(() => createApiClient(apiBase), [apiBase]);

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  const [showCreate, setShowCreate] = useState(false);
  const [showEdit, setShowEdit] = useState(false);
  const [showDelete, setShowDelete] = useState(false);

  const [createForm, setCreateForm] = useState(() => ({ ...EMPTY_FORM }));
  const [editForm, setEditForm] = useState(() => ({ ...EMPTY_FORM, id: "" }));
  const [deleteRow, setDeleteRow] = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const tasks = await api.listTasks();
      setRows(tasks);
    } catch (e) {
      notify(e.message || "Could not load tasks.", "danger");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [dataRevision, api]);

  const openEdit = (t) => {
    setEditForm({
      id: t.id,
      title: t.title,
      status: t.status,
      start_date: toYmd(t.start_date),
      end_date: toYmd(t.end_date),
    });
    setShowEdit(true);
  };

  const openDelete = (t) => {
    setDeleteRow(t);
    setShowDelete(true);
  };

  const submitCreate = async (e) => {
    e.preventDefault();
    try {
      const body = {
        title: createForm.title,
        status: createForm.status,
        start_date: createForm.start_date || null,
        end_date: createForm.end_date || null,
      };
      await api.createTask(body);
      notify("Task created.");
      setShowCreate(false);
      setCreateForm({ ...EMPTY_FORM });
      bumpData();
    } catch (err) {
      notify(err.message, "danger");
    }
  };

  const submitEdit = async (e) => {
    e.preventDefault();
    try {
      await api.updateTask(editForm.id, {
        title: editForm.title,
        status: editForm.status,
        start_date: editForm.start_date || null,
        end_date: editForm.end_date || null,
      });
      notify("Task updated.");
      setShowEdit(false);
      bumpData();
    } catch (err) {
      notify(err.message, "danger");
    }
  };

  const submitDelete = async () => {
    if (!deleteRow) return;
    try {
      await api.deleteTask(deleteRow.id);
      notify("Task deleted.");
      setShowDelete(false);
      setDeleteRow(null);
      bumpData();
    } catch (err) {
      notify(err.message, "danger");
    }
  };

  const formFields = (form, setForm) => (
    <Row className="g-3">
      <Col md={12}>
        <Form.Group>
          <Form.Label>Title</Form.Label>
          <Form.Control
            value={form.title}
            onChange={(e) =>
              setForm((f) => ({ ...f, title: e.target.value }))
            }
            required
            maxLength={200}
          />
        </Form.Group>
      </Col>
      <Col md={4}>
        <Form.Group>
          <Form.Label>Status</Form.Label>
          <Form.Select
            value={form.status}
            onChange={(e) =>
              setForm((f) => ({ ...f, status: e.target.value }))
            }
            required
          >
            <option value="todo">Todo</option>
            <option value="in_progress">In progress</option>
            <option value="done">Done</option>
          </Form.Select>
        </Form.Group>
      </Col>
      <Col md={4}>
        <Form.Group>
          <Form.Label>Start date</Form.Label>
          <Form.Control
            type="date"
            value={form.start_date}
            onChange={(e) =>
              setForm((f) => ({ ...f, start_date: e.target.value }))
            }
          />
        </Form.Group>
      </Col>
      <Col md={4}>
        <Form.Group>
          <Form.Label>End date</Form.Label>
          <Form.Control
            type="date"
            value={form.end_date}
            onChange={(e) =>
              setForm((f) => ({ ...f, end_date: e.target.value }))
            }
          />
        </Form.Group>
      </Col>
    </Row>
  );

  return (
    <>
      <div className="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-4">
        <h1 className="h3 ds-page-title mb-0">Tasks</h1>
        <Button
          variant="primary"
          onClick={() => {
            setCreateForm({ ...EMPTY_FORM });
            setShowCreate(true);
          }}
        >
          New task
        </Button>
      </div>

      <div className="card ds-card">
        <div className="card-body p-0">
          <div className="table-responsive">
            <Table hover className="mb-0 align-middle">
              <thead className="table-light">
                <tr>
                  <th className="ps-4">ID</th>
                  <th>Title</th>
                  <th>Status</th>
                  <th>Start</th>
                  <th>End</th>
                  <th className="text-end pe-4" style={{ width: "12rem" }}>
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={6} className="text-center py-5 text-secondary">
                      Loading…
                    </td>
                  </tr>
                ) : rows.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="text-center py-5 text-secondary">
                      No tasks yet.
                    </td>
                  </tr>
                ) : (
                  rows.map((t) => (
                    <tr key={t.id}>
                      <td className="ps-4 text-secondary task-id-cell" title={t.id}>
                        {t.id}
                      </td>
                      <td className="fw-medium">{t.title}</td>
                      <td>
                        <span className="badge text-bg-secondary">
                          {statusLabel(t.status)}
                        </span>
                      </td>
                      <td>{toYmd(t.start_date) || "—"}</td>
                      <td>{toYmd(t.end_date) || "—"}</td>
                      <td className="text-end pe-4">
                        <Button
                          variant="outline-primary"
                          size="sm"
                          className="me-1"
                          onClick={() => openEdit(t)}
                        >
                          Edit
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => openDelete(t)}
                        >
                          Delete
                        </Button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </Table>
          </div>
        </div>
      </div>

      <Modal show={showCreate} onHide={() => setShowCreate(false)} centered size="lg">
        <Form onSubmit={submitCreate}>
          <Modal.Header closeButton>
            <Modal.Title>New task</Modal.Title>
          </Modal.Header>
          <Modal.Body>{formFields(createForm, setCreateForm)}</Modal.Body>
          <Modal.Footer>
            <Button variant="outline-secondary" type="button" onClick={() => setShowCreate(false)}>
              Cancel
            </Button>
            <Button variant="primary" type="submit">
              Create
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      <Modal show={showEdit} onHide={() => setShowEdit(false)} centered size="lg">
        <Form onSubmit={submitEdit}>
          <Modal.Header closeButton>
            <Modal.Title>Edit task</Modal.Title>
          </Modal.Header>
          <Modal.Body>{formFields(editForm, setEditForm)}</Modal.Body>
          <Modal.Footer>
            <Button variant="outline-secondary" type="button" onClick={() => setShowEdit(false)}>
              Cancel
            </Button>
            <Button variant="primary" type="submit">
              Save
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      <Modal show={showDelete} onHide={() => setShowDelete(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Delete task</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="mb-0">
            Delete <strong>{deleteRow?.title}</strong>? This cannot be undone.
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="outline-secondary" onClick={() => setShowDelete(false)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={submitDelete}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
