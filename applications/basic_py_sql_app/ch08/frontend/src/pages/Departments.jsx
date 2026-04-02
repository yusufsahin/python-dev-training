import { useEffect, useMemo, useState } from "react";
import {
  Button,
  Form,
  Modal,
  Table,
} from "react-bootstrap";
import { createApiClient } from "../api/client.js";
import { useApp } from "../context/AppContext.jsx";

export default function Departments() {
  const { apiBase, dataRevision, bumpData, notify } = useApp();
  const api = useMemo(() => createApiClient(apiBase), [apiBase]);

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  const [showCreate, setShowCreate] = useState(false);
  const [showEdit, setShowEdit] = useState(false);
  const [showDelete, setShowDelete] = useState(false);

  const [createName, setCreateName] = useState("");
  const [editId, setEditId] = useState(null);
  const [editName, setEditName] = useState("");
  const [deleteRow, setDeleteRow] = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const data = await api.listDepartments();
      setRows(data);
    } catch (e) {
      notify(e.message || "Liste alınamadı", "danger");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [dataRevision, apiBase]);

  const openEdit = (d) => {
    setEditId(d.id);
    setEditName(d.name);
    setShowEdit(true);
  };

  const openDelete = (d) => {
    setDeleteRow(d);
    setShowDelete(true);
  };

  const submitCreate = async (e) => {
    e.preventDefault();
    try {
      await api.createDepartment({ name: createName });
      notify("Department created.");
      setShowCreate(false);
      setCreateName("");
      bumpData();
    } catch (err) {
      notify(err.message, "danger");
    }
  };

  const submitEdit = async (e) => {
    e.preventDefault();
    try {
      await api.updateDepartment(editId, { name: editName });
      notify("Department updated.");
      setShowEdit(false);
      bumpData();
    } catch (err) {
      notify(err.message, "danger");
    }
  };

  const submitDelete = async () => {
    if (!deleteRow) return;
    try {
      await api.deleteDepartment(deleteRow.id);
      notify("Department deleted.");
      setShowDelete(false);
      setDeleteRow(null);
      bumpData();
    } catch (err) {
      notify(err.message, "danger");
    }
  };

  return (
    <>
      <div className="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-4">
        <h1 className="h3 ds-page-title mb-0">Departments</h1>
        <Button variant="primary" onClick={() => setShowCreate(true)}>
          New department
        </Button>
      </div>

      <div className="card ds-card">
        <div className="card-body p-0">
          <div className="table-responsive">
            <Table hover className="mb-0 align-middle">
              <thead className="table-light">
                <tr>
                  <th className="ps-4">ID</th>
                  <th>Name</th>
                  <th className="text-end pe-4" style={{ width: "11rem" }}>
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={3} className="text-center py-5 text-secondary">
                      Loading…
                    </td>
                  </tr>
                ) : rows.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="text-center py-5 text-secondary">
                      No departments yet.
                    </td>
                  </tr>
                ) : (
                  rows.map((d) => (
                    <tr key={d.id}>
                      <td className="ps-4 text-secondary">{d.id}</td>
                      <td className="fw-medium">{d.name}</td>
                      <td className="text-end pe-4">
                        <Button
                          variant="outline-primary"
                          size="sm"
                          className="me-1"
                          onClick={() => openEdit(d)}
                        >
                          Edit
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => openDelete(d)}
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

      <Modal show={showCreate} onHide={() => setShowCreate(false)} centered>
        <Form onSubmit={submitCreate}>
          <Modal.Header closeButton>
            <Modal.Title>New department</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group>
              <Form.Label>Name</Form.Label>
              <Form.Control
                value={createName}
                onChange={(e) => setCreateName(e.target.value)}
                required
                maxLength={100}
                autoComplete="organization"
              />
            </Form.Group>
          </Modal.Body>
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

      <Modal show={showEdit} onHide={() => setShowEdit(false)} centered>
        <Form onSubmit={submitEdit}>
          <Modal.Header closeButton>
            <Modal.Title>Edit department</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group>
              <Form.Label>Name</Form.Label>
              <Form.Control
                value={editName}
                onChange={(e) => setEditName(e.target.value)}
                required
                maxLength={100}
              />
            </Form.Group>
          </Modal.Body>
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
          <Modal.Title>Delete department</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="mb-0">
            Delete <strong>{deleteRow?.name}</strong>? This cannot be undone.
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
