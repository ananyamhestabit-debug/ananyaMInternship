"use client";

export default function Sidebar() {
  return (
    <div className="w-64 h-screen bg-slate-800 text-white p-6">
      <h2 className="text-2xl font-bold mb-8">Purity UI</h2>

      <ul className="space-y-3">
        <li className="bg-white text-slate-800 px-3 py-2 rounded">
          Dashboard
        </li>
        <li className="hover:bg-slate-700 px-3 py-2 rounded cursor-pointer">
          Tables
        </li>
        <li className="hover:bg-slate-700 px-3 py-2 rounded cursor-pointer">
          Billing
        </li>
        <li className="hover:bg-slate-700 px-3 py-2 rounded cursor-pointer">
          Profile
        </li>
      </ul>
    </div>
  );
}
