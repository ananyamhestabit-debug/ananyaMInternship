"use client";

import Link from "next/link";
import Image from "next/image";

export default function Navbar() {
  return (
    <header className="w-full bg-white border-b px-6 py-3 flex items-center justify-between">
      
      <Link href="/dashboard" className="flex items-center">
        <Image
          src="/logo.png"  
          alt="SaaS Hub Logo"
          width={140}            
          height={40}
          className="object-contain"
          priority
        />
      </Link>

      <div className="flex items-center gap-4">

                <Link
          href="/dashboard/about"
          className="text-gray-700 hover:text-sky-600"
        >
          About Us
        </Link> &nbsp;
        
        <Link
          href="/dashboard/settings"
          className="text-gray-700 hover:text-sky-600"
        >
          Settings
        </Link> &nbsp;


        <Link href="/dashboard/profile" className="flex items-center gap-2">
          <Image
            src="/user.png"
            alt="Admin"
            width={36}
            height={36}
            className="rounded-full border"
          />
          <span className="text-sm font-medium text-gray-800">Admin</span>
        </Link>
      </div>
    </header>
  );
}
