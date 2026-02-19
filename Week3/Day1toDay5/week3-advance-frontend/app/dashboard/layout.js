import Sidebar from "@/components/ui/Sidebar"

export default function DashboardLayout({ children }) {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-6 bg-gray-50 min-h-screen">
        {children}
      </div>
    </div>
  )
}
