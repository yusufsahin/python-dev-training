"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import { useCartId } from "@/context/CartIdContext";

const CartUiContext = createContext(null);

export function CartUiProvider({ children }) {
  const { cartId } = useCartId();
  const [cartCount, setCartCount] = useState(0);

  const refreshCartCount = useCallback(async () => {
    if (!cartId) return;
    try {
      const cart = await api("/api/cart", {
        headers: { "X-Cart-Id": cartId },
      });
      setCartCount(cart.item_count ?? 0);
    } catch {
      setCartCount(0);
    }
  }, [cartId]);

  useEffect(() => {
    if (!cartId) return;
    let cancelled = false;
    (async () => {
      try {
        const cart = await api("/api/cart", {
          headers: { "X-Cart-Id": cartId },
        });
        if (!cancelled) setCartCount(cart.item_count ?? 0);
      } catch {
        if (!cancelled) setCartCount(0);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [cartId]);

  const value = useMemo(
    () => ({ cartCount, refreshCartCount, setCartCount }),
    [cartCount, refreshCartCount],
  );

  return <CartUiContext.Provider value={value}>{children}</CartUiContext.Provider>;
}

export function useCartUi() {
  const ctx = useContext(CartUiContext);
  if (!ctx) throw new Error("useCartUi inside CartUiProvider");
  return ctx;
}
