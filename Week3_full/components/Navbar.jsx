"use client";

import Link from "next/link";
import Image from "next/image";
import Avatar from "./ui/Avatar";

export default function Navbar() {
  return (
    <header className="w-full bg-gray-50 border-b border-sky-200 px-4 sm:px-6 py-3 flex items-center justify-between flex-wrap gap-4">

      <Link href="/" className="flex items-center">
        <Image
          src="/logo.png"
          alt="SaaS Hub Logo"
          width={120}
          height={40}
          className="object-contain"
          priority
        />
      </Link>

      <div className="flex items-center gap-4 sm:gap-6 flex-wrap">

        <Link href="/dashboard/about" className="text-gray-700 hover:text-sky-600">
          About
        </Link>

        <Link href="/dashboard/settings" className="text-gray-700 hover:text-sky-600">
          Settings
        </Link>

        <Link href="/dashboard/profile" className="flex items-center gap-2">
          <Avatar size={36} />
          <span className="text-sm font-medium text-gray-800">
            Admin
          </span>
        </Link>

      </div>
    </header>
  );
}