import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Departments from "./pages/Departments.jsx";
import Home from "./pages/Home.jsx";
import Students from "./pages/Students.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="departments" element={<Departments />} />
        <Route path="students" element={<Students />} />
      </Route>
    </Routes>
  );
}
