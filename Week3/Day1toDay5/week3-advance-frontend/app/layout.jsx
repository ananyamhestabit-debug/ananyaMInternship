import "./globals.css";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export const metadata = {
  title: "SaaS Admin Dashboard",
  description: "Admin dashboard built with Next.js",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Navbar />

        {/* Responsive Layout */}
        <div className="flex flex-col md:flex-row">
          <Sidebar />

          <main className="flex-1 p-4 sm:p-6 bg-gray-100">
            {children}
          </main>
        </div>

      </body>
    </html>
  );
}
