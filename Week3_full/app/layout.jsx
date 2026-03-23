import "./globals.css";
import Navbar from "../components/Navbar";
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata = {
  title: "SaaS Admin Dashboard",
  description: "Admin dashboard built with Next.js",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${inter.className}`}>

        <Navbar />

        <main className="min-h-screen bg-white-100 ">
          {children}
        </main>

      </body>
    </html>
  );
}