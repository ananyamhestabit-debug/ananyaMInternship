"use client";

import Button from "../../../components/ui/Button";
import Avatar from "../../../components/ui/Avatar";

export default function ProfilePage() {
  return (
    <div className="min-h-screen p-4 sm:p-6">

      <div className="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-6 sm:p-8 max-w-4xl mx-auto">

        <div className="flex flex-col sm:flex-row items-center gap-6">

          <Avatar size={100} className="border-4 border-blue-200" />

          <div className="text-center sm:text-left">
            <h1 className="text-xl sm:text-2xl font-semibold text-gray-900">
              Ananya Mishra
            </h1>
            <p className="text-gray-600">Administrator</p>
          </div>

        </div>


        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-8 text-sm">

          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-500">Full Name</p>
            <p className="font-medium text-gray-900">
              Ananya Mishra
            </p>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-500">Role</p>
            <p className="font-medium text-gray-900">
              Admin
            </p>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-500">Email</p>

            <p className="font-medium text-gray-900 break-all text-sm sm:text-base">
              admin@saasapp.com
            </p>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-500">Account Status</p>
            <span className="inline-block px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-semibold">
              Active
            </span>
          </div>

        </div>

        <div className="mt-8 flex flex-col sm:flex-row gap-4">

          <Button variant="primary" className="w-full sm:w-auto">
            Edit Profile
          </Button>

          <Button variant="secondary" className="w-full sm:w-auto">
            Change Password
          </Button>

        </div>

      </div>

    </div>
  );
}