"use client";
import Image from "next/image";

export default function ProfilePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100 p-6">

      <div className="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 max-w-4xl">

        <div className="flex items-center gap-6">
          <Image
            src="/user.png"
            alt="Admin Profile"
            width={100}
            height={100}
            className="rounded-full border-4 border-blue-200"
          />

          <div>
            <h1 className="text-2xl font-semibold text-gray-900">
              Ananya Mishra
            </h1>
            <p className="text-gray-600">Administrator</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-8 text-sm">

          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-500">Full Name</p>
            <p className="font-medium text-gray-900">Ananya Mishra</p>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-500">Role</p>
            <p className="font-medium text-gray-900">Admin</p>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-500">Email</p>
            <p className="font-medium text-gray-900">admin@saasapp.com</p>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-500">Account Status</p>
            <span className="inline-block px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-semibold">
              Active
            </span>
          </div>

        </div>

        <div className="mt-8 flex gap-4">
          <button className="px-6 py-2 rounded-xl bg-yellow-400 text-gray-900 hover:bg-yellow-500 transition">
            Edit Profile
          </button>

          <button className="px-6 py-2 rounded-xl border border-gray-300 text-gray-700 hover:bg-gray-100 transition">
            Change Password
          </button>
        </div>

      </div>

    </div>
  );
}
