import { useEffect, useMemo, useState } from "react";
import { Button, Card, Col, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
import { createApiClient } from "../api/client.js";
import { useApp } from "../context/AppContext.jsx";

export default function Home() {
  const { apiBase, dataRevision, notify } = useApp();
  const api = useMemo(() => createApiClient(apiBase), [apiBase]);
  const [count, setCount] = useState(0);

  useEffect(() => {
    let cancel = false;
    (async () => {
      try {
        const tasks = await api.listTasks();
        if (!cancel) setCount(tasks.length);
      } catch (e) {
        if (!cancel) notify(e.message || "Failed to load.", "danger");
      }
    })();
    return () => {
      cancel = true;
    };
  }, [api, notify, dataRevision]);

  return (
    <Row className="g-4">
      <Col lg={8}>
        <h1 className="h3 ds-page-title mb-3">Overview</h1>
        <p className="text-secondary mb-4">
          FastAPI + Motor (MongoDB) backend, React + Context API. Same task
          model as ch09/ch10: title, status, start/end dates.
        </p>
        <Card className="ds-card mb-4">
          <Card.Body>
            <p className="text-secondary small text-uppercase mb-1">Tasks</p>
            <p className="display-6 fw-semibold text-primary mb-0">{count}</p>
          </Card.Body>
        </Card>
        <div className="d-flex flex-wrap gap-2">
          <Button as={Link} to="/tasks" variant="primary">
            Manage tasks
          </Button>
        </div>
      </Col>
    </Row>
  );
}
