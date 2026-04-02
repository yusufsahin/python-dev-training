import { Container, Nav, Navbar } from "react-bootstrap";
import { Link, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <>
      <Navbar expand="md" bg="primary" variant="dark" className="shadow-sm">
        <Container>
          <Navbar.Brand as={Link} to="/">
            School
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="nav-main" />
          <Navbar.Collapse id="nav-main" className="justify-content-end">
            <Nav>
              <Nav.Link as={Link} to="/departments">
                Departments
              </Nav.Link>
              <Nav.Link as={Link} to="/students">
                Students
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <main className="flex-grow-1">
        <Container className="py-3">
          <Outlet />
        </Container>
      </main>
    </>
  );
}
