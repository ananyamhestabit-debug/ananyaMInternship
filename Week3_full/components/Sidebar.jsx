"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Button from "./ui/Button";
import {useState} from "react";

export default function Sidebar() {
  const pathname = usePathname();
  

  const linkClass = (path) =>
    `block px-4 py-2 rounded-lg transition ${
      pathname === path
        ? "bg-sky-500 text-white"
        : "text-gray-800 hover:bg-sky-100"
      
    }`;

  return (
    <aside className="sticky top-0 h-screen w-56 md:w-64 bg-sky-50 border-r border-sky-200 p-4 sm:p-6 hidden sm:block">

      <div>
        <div className="mb-8 text-blue-600 text-lg font-semibold">
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
      </div>

      <div className="mt-10">
        <Link href="/login" className="block w-full">
          <Button className="bg-yellow-400 text-gray-900 hover:bg-yellow-500 px-6 py-3 w-full"
          onClick={()=>
          
          }>
  Logout
</Button>
        </Link>
      </div>

    </aside>
  );
}