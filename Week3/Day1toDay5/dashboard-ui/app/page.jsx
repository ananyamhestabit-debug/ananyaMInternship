import Sidebar from "@/components/layout/Sidebar";
import Navbar from "@/components/layout/Navbar";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";

export default function Dashboard() {
  return (
    <div className="flex">
      <Sidebar />

      <div className="flex-1">
        <Navbar />

        <main className="p-6 bg-gray-100 min-h-screen">
          <h1 className="text-2xl font-bold mb-6">
            Dashboard Overview
          </h1>

          {/* Stats Cards */}
          <div className="grid grid-cols-3 gap-6 mb-8">
            <Card title="Users" value="1,200" />
            <Card title="Sales" value="$24,000" />
            <Card title="Orders" value="320" />
          </div>

          {/* Component Showcase */}
          <div className="bg-white p-6 rounded-xl shadow space-y-4">
            <h2 className="text-lg font-semibold">
              Component Library Preview
            </h2>

            <Input placeholder="Enter email..." />

            <Button>Primary Button</Button>

            <div className="flex gap-3">
              <Badge color="green">Active</Badge>
              <Badge color="red">Inactive</Badge>
              <Badge color="blue">New</Badge>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
