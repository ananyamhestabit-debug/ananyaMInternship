import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100 p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Dashboard Overview
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500 text-sm">Total Users</p>
          <h3 className="text-2xl font-bold text-sky-600">1,245</h3>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500 text-sm">Active Sessions</p>
          <h3 className="text-2xl font-bold text-green-600">89</h3>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500 text-sm">Revenue</p>
          <h3 className="text-2xl font-bold text-purple-600">₹42,500</h3>
        </div>


        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500 text-sm">System Status</p>
          <h3 className="text-xl font-bold text-green-600 mt-1">
            All Systems Operational
          </h3>
          <span className="inline-block mt-2 px-3 py-1 text-xs rounded-full bg-green-100 text-green-700">
            Online
          </span>
        </div>
      </div>

      <div className="mt-10 bg-white p-6 rounded-xl shadow">
        <h3 className="text-lg font-bold mb-4 text-black">
  Recent Activity
</h3>


        <ul className="space-y-3 text-gray-600 text-sm">
          <li>✅ New user registered</li>
          <li>🔁 Profile updated</li>
          <li>💳 Payment received</li>
        </ul>
      </div>
    </div>
  );
}
