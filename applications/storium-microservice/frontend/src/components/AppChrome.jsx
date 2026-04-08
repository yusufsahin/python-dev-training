"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { useCartUi } from "@/context/CartUiContext";

export function AppChrome({ children }) {
  const { user, logout, loading } = useAuth();
  const { cartCount } = useCartUi();

  return (
    <>
      <header className="app-header">
        <Link href="/">
          <strong>Storium</strong>
        </Link>
        <nav>
          <Link href="/">Ana sayfa</Link>
          <Link href="/cart">Sepet ({cartCount})</Link>
          {loading ? (
            <span>...</span>
          ) : user ? (
            <>
              <Link href="/orders">Siparişlerim</Link>
              <span>{user.username}</span>
              <button type="button" onClick={() => logout()}>
                Çıkış
              </button>
            </>
          ) : (
            <>
              <Link href="/login">Giriş</Link>
              <Link href="/register">Kayıt</Link>
            </>
          )}
        </nav>
      </header>
      <main className="app-main">{children}</main>
    </>
  );
}
