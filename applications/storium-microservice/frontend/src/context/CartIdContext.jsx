"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

const CartIdContext = createContext(null);
const CART_ID_KEY = "storium_cart_id";

function makeId() {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `cart-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export function CartIdProvider({ children }) {
  const [cartId, setCartIdState] = useState("");

  useEffect(() => {
    let id = localStorage.getItem(CART_ID_KEY);
    if (!id) {
      id = makeId();
      localStorage.setItem(CART_ID_KEY, id);
    }
    setCartIdState(id);
  }, []);

  const setCartId = (id) => {
    localStorage.setItem(CART_ID_KEY, id);
    setCartIdState(id);
  };

  const resetCartId = () => {
    const id = makeId();
    localStorage.setItem(CART_ID_KEY, id);
    setCartIdState(id);
    return id;
  };

  const value = useMemo(() => ({ cartId, setCartId, resetCartId }), [cartId]);

  return <CartIdContext.Provider value={value}>{children}</CartIdContext.Provider>;
}

export function useCartId() {
  const ctx = useContext(CartIdContext);
  if (!ctx) throw new Error("useCartId inside CartIdProvider");
  return ctx;
}
