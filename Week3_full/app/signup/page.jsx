"use client";

import Link from "next/link";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

export default function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100 px-4">

      <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-xl p-6 sm:p-10 w-full max-w-md">

        <h1 className="text-2xl sm:text-3xl font-semibold text-gray-900 mb-8 text-center">
          Create Your Account
        </h1>

     
        <div className="space-y-5">

          <Input
            type="text"
            placeholder="Full Name"
            className="py-3"
          />

          <Input
            type="email"
            placeholder="Email"
            className="py-3"
          />

          <Input
            type="password"
            placeholder="Password"
            className="py-3"
          />

        </div>

       
        <div className="mt-8">
          <Link href="/login" className="block w-full">
            <Button className="bg-yellow-400 text-gray-900 hover:bg-yellow-500 px-6 py-3 w-full">
              Sign Up
            </Button>
          </Link>
        </div>

      
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