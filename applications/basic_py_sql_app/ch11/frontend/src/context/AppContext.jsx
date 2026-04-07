import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";
import { Toast, ToastContainer } from "react-bootstrap";

const AppContext = createContext(null);

/**
 * apiBase: same-origin in Docker/prod; Vite dev uses proxy. Override with VITE_API_URL.
 */
export function AppProvider({ children }) {
  const apiBase = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

  const [dataRevision, setDataRevision] = useState(0);
  const bumpData = useCallback(() => {
    setDataRevision((r) => r + 1);
  }, []);

  const [toasts, setToasts] = useState([]);
  const notify = useCallback((message, variant = "success") => {
    const id = crypto.randomUUID();
    setToasts((t) => [...t, { id, message, variant }]);
  }, []);

  const dismissToast = useCallback((id) => {
    setToasts((t) => t.filter((x) => x.id !== id));
  }, []);

  const value = useMemo(
    () => ({
      apiBase,
      dataRevision,
      bumpData,
      notify,
    }),
    [apiBase, dataRevision, bumpData, notify]
  );

  return (
    <AppContext.Provider value={value}>
      {children}
      <ToastContainer
        position="top-end"
        className="p-3 toast-container position-fixed"
      >
        {toasts.map((t) => (
          <Toast
            key={t.id}
            bg={t.variant}
            onClose={() => dismissToast(t.id)}
            delay={4500}
            autohide
            animation
          >
            <Toast.Header closeButton>
              <strong className="me-auto">Tasks</strong>
            </Toast.Header>
            <Toast.Body className={t.variant === "light" ? "" : "text-white"}>
              {t.message}
            </Toast.Body>
          </Toast>
        ))}
      </ToastContainer>
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) {
    throw new Error("useApp must be used within AppProvider");
  }
  return ctx;
}
