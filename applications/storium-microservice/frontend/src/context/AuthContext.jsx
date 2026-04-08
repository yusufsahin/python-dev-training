"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";

const AuthContext = createContext(null);

const TOKEN_KEY = "storium_token";

function getApiBase() {
  return process.env.NEXT_PUBLIC_API_BASE ?? "";
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const t = typeof window !== "undefined" ? localStorage.getItem(TOKEN_KEY) : null;
    setToken(t);
    if (!t) setLoading(false);
  }, []);

  const refreshMe = useCallback(async (t) => {
    if (!t) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const me = await api("/api/auth/me", { token: t });
      setUser(me);
    } catch {
      setToken(null);
      if (typeof window !== "undefined") localStorage.removeItem(TOKEN_KEY);
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshMe(token);
  }, [token, refreshMe]);

  const login = useCallback(async (username, password) => {
    const form = new URLSearchParams();
    form.set("username", username);
    form.set("password", password);
    const res = await fetch(`${getApiBase()}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form.toString(),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.detail || "Giriş başarısız");
    }
    if (typeof window !== "undefined") localStorage.setItem(TOKEN_KEY, data.access_token);
    setToken(data.access_token);
    return data;
  }, []);

  const register = useCallback(
    async ({ email, username, password }) => {
      await api("/api/auth/register", { method: "POST", body: { email, username, password } });
      await login(username, password);
    },
    [login],
  );

  const logout = useCallback(() => {
    if (typeof window !== "undefined") localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      login,
      register,
      logout,
      refreshMe,
    }),
    [token, user, loading, login, register, logout, refreshMe],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth inside AuthProvider");
  return ctx;
}
