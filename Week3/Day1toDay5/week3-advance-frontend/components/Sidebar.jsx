"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const linkClass = (path) =>
    `block px-4 py-2 rounded-lg transition ${
      pathname === path
        ? "bg-sky-500 text-white"
        : "text-gray-800 hover:bg-sky-100"
    }`;

  return (
    <aside className="w-full md:w-64 bg-sky-50 border-r border-sky-100 p-6">
      
      <div className="mb-8 bold text-blue-600 text-lg">
        SaaS Hub Dashboard
      </div>

      <nav className="space-y-3">

        <Link href="/dashboard" className={linkClass("/dashboard")}>
          Dashboard
        </Link>

        <Link href="/dashboard/analytics" className={linkClass("/dashboard/analytics")}>
          Analytics
        </Link>

        <Link href="/dashboard/products" className={linkClass("/dashboard/products")}>
          Products
        </Link>

        <Link href="/dashboard/billing" className={linkClass("/dashboard/billing")}>
          Billing
        </Link>

        <Link href="/dashboard/users" className={linkClass("/dashboard/users")}>
          Users
        </Link>

        <Link href="/dashboard/profile" className={linkClass("/dashboard/profile")}>
          Profile
        </Link>


      </nav>

      <div className="mt-10">
        <Link href="/login">
          <button className="w-full bg-yellow-500 text-white py-2 rounded-lg hover:bg-yellow-600 transition">
            Logout
          </button>
        </Link>
      </div>

    </aside>
  );
}
