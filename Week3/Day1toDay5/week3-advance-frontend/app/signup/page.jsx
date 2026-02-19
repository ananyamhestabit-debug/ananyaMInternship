"use client";
import Link from "next/link";

export default function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100">

      <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-xl p-10 w-full max-w-md">

        <h1 className="text-3xl font-semibold text-gray-900 mb-8 text-center">
          Create Your Account
        </h1>

        <div className="space-y-5">

          <input
            type="text"
            placeholder="Full Name"
            className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-300"
          />

          <input
            type="email"
            placeholder="Email"
            className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-300"
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-300"
          />

        </div>

        <Link
          href="/login"
          className="block mt-8 text-center bg-yellow-400 text-gray-900 py-3 rounded-xl hover:bg-yellow-500 transition font-medium"
        >
          Sign Up
        </Link>

        <p className="text-sm text-gray-600 mt-6 text-center">
          Already have an account?{" "}
          <Link href="/login" className="text-blue-600 hover:underline">
            Login
          </Link>
        </p>

      </div>
    </div>
  );
}
