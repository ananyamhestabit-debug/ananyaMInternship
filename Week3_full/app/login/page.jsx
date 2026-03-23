"use client";

import Link from "next/link";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100">

      <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-xl p-10 w-full max-w-md">

        <h1 className="text-3xl font-semibold text-gray-900 mb-8 text-center">
          Welcome Back
        </h1>

        <div className="space-y-5">

          <Input
            type="text"
            placeholder="Username"
            className="py-3"
          />

          <Input
            type="password"
            placeholder="Password"
            className="py-3"
          />

        </div>

      
        <Link href="/dashboard" className="block mt-8 w-full">
  <Button className="w-full py-3">
    Login
  </Button>
</Link>

        <p className="text-sm text-gray-600 mt-6 text-center">
          Don’t have an account?{" "}
          <Link href="/signup" className="text-blue-600 hover:underline">
            Sign up
          </Link>
        </p>

      </div>

    </div>
  );
}