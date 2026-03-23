import Sidebar from "../../components/Sidebar";

export default function DashboardLayout({ children }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 min-w-0 p-4 sm:p-6 bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100">
        {children}
      </main>

    </div>
  );
}