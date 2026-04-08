import { AppChrome } from "@/components/AppChrome";
import { Providers } from "@/components/Providers";
import "./globals.css";

export const metadata = {
  title: "Storium",
  description: "Storium e-ticaret",
};

export default function RootLayout({ children }) {
  return (
    <html lang="tr">
      <body>
        <Providers>
          <AppChrome>{children}</AppChrome>
        </Providers>
      </body>
    </html>
  );
}
