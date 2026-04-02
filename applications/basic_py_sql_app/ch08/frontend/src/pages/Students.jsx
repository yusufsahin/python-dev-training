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

const EMPTY_STUDENT_FORM = {
  student_number: "",
  first_name: "",
  last_name: "",
  birth_date: "",
  department_id: "",
};

function toYmd(d) {
  if (!d) return "";
  if (typeof d === "string") return d.slice(0, 10);
  return d;
}

export default function Students() {
  const { apiBase, dataRevision, bumpData, notify } = useApp();
  const api = useMemo(() => createApiClient(apiBase), [apiBase]);

  const [rows, setRows] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);

  const [showCreate, setShowCreate] = useState(false);
  const [showEdit, setShowEdit] = useState(false);
  const [showDelete, setShowDelete] = useState(false);

  const [createForm, setCreateForm] = useState(() => ({ ...EMPTY_STUDENT_FORM }));
  const [editForm, setEditForm] = useState(() => ({
    ...EMPTY_STUDENT_FORM,
    id: null,
  }));
  const [deleteRow, setDeleteRow] = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const [stus, depts] = await Promise.all([
        api.listStudents(),
        api.listDepartments(),
      ]);
      setRows(stus);
      setDepartments(depts);
    } catch (e) {
      notify(e.message || "Liste alınamadı", "danger");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [dataRevision, apiBase]);

  const openEdit = (s) => {
    setEditForm({
      id: s.id,
      student_number: s.student_number,
      first_name: s.first_name,
      last_name: s.last_name,
      birth_date: toYmd(s.birth_date),
      department_id: String(s.department_id),
    });
    setShowEdit(true);
  };

  const openDelete = (s) => {
    setDeleteRow(s);
    setShowDelete(true);
  };

  const submitCreate = async (e) => {
    e.preventDefault();
    try {
      await api.createStudent({
        student_number: createForm.student_number,
        first_name: createForm.first_name,
        last_name: createForm.last_name,
        birth_date: createForm.birth_date,
        department_id: Number(createForm.department_id),
      });
      notify("Student created.");
      setShowCreate(false);
      setCreateForm({ ...EMPTY_STUDENT_FORM });
      bumpData();
    } catch (err) {
      notify(err.message, "danger");
    }
  };

  const submitEdit = async (e) => {
    e.preventDefault();
    try {
      await api.updateStudent(editForm.id, {
        student_number: editForm.student_number,
        first_name: editForm.first_name,
        last_name: editForm.last_name,
        birth_date: editForm.birth_date,
        department_id: Number(editForm.department_id),
      });
      notify("Student updated.");
      setShowEdit(false);
      bumpData();
    } catch (err) {
      notify(err.message, "danger");
    }
  };

  const submitDelete = async () => {
    if (!deleteRow) return;
    try {
      await api.deleteStudent(deleteRow.id);
      notify("Student deleted.");
      setShowDelete(false);
      setDeleteRow(null);
      bumpData();
    } catch (err) {
      notify(err.message, "danger");
    }
  };

  const deptOptions = departments.map((d) => (
    <option key={d.id} value={d.id}>
      {d.name}
    </option>
  ));

  const studentFormFields = (form, setForm) => (
    <Row className="g-3">
      <Col md={6}>
        <Form.Group>
          <Form.Label>Student number</Form.Label>
          <Form.Control
            value={form.student_number}
            onChange={(e) =>
              setForm((f) => ({ ...f, student_number: e.target.value }))
            }
            required
            maxLength={20}
            placeholder="e.g. 2024001"
          />
        </Form.Group>
      </Col>
      <Col md={6}>
        <Form.Group>
          <Form.Label>Department</Form.Label>
          <Form.Select
            value={form.department_id}
            onChange={(e) =>
              setForm((f) => ({ ...f, department_id: e.target.value }))
            }
            required
          >
            <option value="">Select…</option>
            {deptOptions}
          </Form.Select>
        </Form.Group>
      </Col>
      <Col md={6}>
        <Form.Group>
          <Form.Label>First name</Form.Label>
          <Form.Control
            value={form.first_name}
            onChange={(e) =>
              setForm((f) => ({ ...f, first_name: e.target.value }))
            }
            required
            maxLength={50}
          />
        </Form.Group>
      </Col>
      <Col md={6}>
        <Form.Group>
          <Form.Label>Last name</Form.Label>
          <Form.Control
            value={form.last_name}
            onChange={(e) =>
              setForm((f) => ({ ...f, last_name: e.target.value }))
            }
            required
            maxLength={50}
          />
        </Form.Group>
      </Col>
      <Col md={6}>
        <Form.Group>
          <Form.Label>Birth date</Form.Label>
          <Form.Control
            type="date"
            value={form.birth_date}
            onChange={(e) =>
              setForm((f) => ({ ...f, birth_date: e.target.value }))
            }
            required
          />
        </Form.Group>
      </Col>
    </Row>
  );

  return (
    <>
      <div className="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-4">
        <h1 className="h3 ds-page-title mb-0">Students</h1>
        <Button
          variant="primary"
          onClick={() => {
            setCreateForm({ ...EMPTY_STUDENT_FORM });
            setShowCreate(true);
          }}
        >
          New student
        </Button>
      </div>

      <div className="card ds-card">
        <div className="card-body p-0">
          <div className="table-responsive">
            <Table hover className="mb-0 align-middle">
              <thead className="table-light">
                <tr>
                  <th className="ps-4">ID</th>
                  <th>Number</th>
                  <th>Name</th>
                  <th>Birth date</th>
                  <th>Department</th>
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
                      No students yet.
                    </td>
                  </tr>
                ) : (
                  rows.map((s) => (
                    <tr key={s.id}>
                      <td className="ps-4 text-secondary">{s.id}</td>
                      <td className="font-monospace small">{s.student_number}</td>
                      <td className="fw-medium">
                        {s.first_name} {s.last_name}
                      </td>
                      <td>{toYmd(s.birth_date)}</td>
                      <td>{s.department?.name}</td>
                      <td className="text-end pe-4">
                        <Button
                          variant="outline-primary"
                          size="sm"
                          className="me-1"
                          onClick={() => openEdit(s)}
                        >
                          Edit
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => openDelete(s)}
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

      <Modal
        show={showCreate}
        onHide={() => setShowCreate(false)}
        centered
        size="lg"
      >
        <Form onSubmit={submitCreate}>
          <Modal.Header closeButton>
            <Modal.Title>New student</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {studentFormFields(createForm, setCreateForm)}
          </Modal.Body>
          <Modal.Footer>
            <Button
              variant="outline-secondary"
              type="button"
              onClick={() => setShowCreate(false)}
            >
              Cancel
            </Button>
            <Button variant="primary" type="submit">
              Create
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      <Modal
        show={showEdit}
        onHide={() => setShowEdit(false)}
        centered
        size="lg"
      >
        <Form onSubmit={submitEdit}>
          <Modal.Header closeButton>
            <Modal.Title>Edit student</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {studentFormFields(editForm, setEditForm)}
          </Modal.Body>
          <Modal.Footer>
            <Button
              variant="outline-secondary"
              type="button"
              onClick={() => setShowEdit(false)}
            >
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
          <Modal.Title>Delete student</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="mb-0">
            Delete{" "}
            <strong>
              {deleteRow?.first_name} {deleteRow?.last_name}
            </strong>
            ? This cannot be undone.
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
