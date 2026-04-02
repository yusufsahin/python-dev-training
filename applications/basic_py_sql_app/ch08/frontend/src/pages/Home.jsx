import { useEffect, useMemo, useState } from "react";
import { Button, Card, Col, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
import { createApiClient } from "../api/client.js";
import { useApp } from "../context/AppContext.jsx";

export default function Home() {
  const { apiBase, notify } = useApp();
  const api = useMemo(() => createApiClient(apiBase), [apiBase]);
  const [counts, setCounts] = useState({ dept: 0, stu: 0 });

  useEffect(() => {
    let cancel = false;
    (async () => {
      try {
        const [depts, stus] = await Promise.all([
          api.listDepartments(),
          api.listStudents(),
        ]);
        if (!cancel) {
          setCounts({ dept: depts.length, stu: stus.length });
        }
      } catch (e) {
        if (!cancel) notify(e.message || "Yüklenemedi", "danger");
      }
    })();
    return () => {
      cancel = true;
    };
  }, [api, notify]);

  return (
    <Row className="g-4">
      <Col lg={8}>
        <h1 className="h3 ds-page-title mb-3">Overview</h1>
        <p className="text-secondary mb-4">Quick counts for your school directory.</p>
        <Row className="g-3">
          <Col sm={6}>
            <Card className="ds-card h-100">
              <Card.Body>
                <p className="text-secondary small text-uppercase mb-1">
                  Departments
                </p>
                <p className="display-6 fw-semibold text-primary mb-0">
                  {counts.dept}
                </p>
              </Card.Body>
            </Card>
          </Col>
          <Col sm={6}>
            <Card className="ds-card h-100">
              <Card.Body>
                <p className="text-secondary small text-uppercase mb-1">
                  Students
                </p>
                <p className="display-6 fw-semibold text-primary mb-0">
                  {counts.stu}
                </p>
              </Card.Body>
            </Card>
          </Col>
        </Row>
        <div className="d-flex flex-wrap gap-2 mt-4">
          <Button as={Link} to="/departments" variant="primary">
            Manage departments
          </Button>
          <Button as={Link} to="/students" variant="outline-primary">
            Manage students
          </Button>
        </div>
      </Col>
    </Row>
  );
}
