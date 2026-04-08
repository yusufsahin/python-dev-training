"use client";

import { AuthProvider } from "@/context/AuthContext";
import { CartIdProvider } from "@/context/CartIdContext";
import { CartUiProvider } from "@/context/CartUiContext";

export function Providers({ children }) {
  return (
    <AuthProvider>
      <CartIdProvider>
        <CartUiProvider>{children}</CartUiProvider>
      </CartIdProvider>
    </AuthProvider>
  );
}
