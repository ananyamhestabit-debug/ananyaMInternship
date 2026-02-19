export default function DashboardLayout({ children }) {
  return (
    <div className="flex flex-col md:flex-row min-h-screen bg-gray-100">

      <aside className="w-full md:w-64 bg-white shadow-md p-6">
        <h2 className="text-xl font-bold mb-6 text-gray-900">
          Admin Panel
        </h2>

        <ul className="space-y-4">
          <li>
            <a href="/dashboard" className="text-gray-700 hover:text-sky-500">
              Dashboard
            </a>
          </li>

          <li>
            <a href="/dashboard/users" className="text-gray-700 hover:text-sky-500">
              Users
            </a>
          </li>

          <li>
            <a href="/dashboard/profile" className="text-gray-700 hover:text-sky-500">
              Profile
            </a>
          </li>

          <li>
            <a href="/" className="text-yellow-500 hover:text-red-600">
              Logout
            </a>
          </li>
        </ul>
      </aside>

      <main className="flex-1 p-4 sm:p-8">
        {children}
      </main>

    </div>
  );
}
