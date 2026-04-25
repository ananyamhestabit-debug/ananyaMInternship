"use client";

import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { name: "Jan", users: 200 },
  { name: "Feb", users: 400 },
  { name: "Mar", users: 350 },
  { name: "Apr", users: 500 },
  { name: "May", users: 700 },
  { name: "Jun", users: 650 },
];

export default function DashboardPage() {
  return (
    <div className="min-h-screen p-4 sm:p-6">

      <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mb-6">
        Dashboard Overview
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">

        <Card>
          <p className="text-gray-500 text-sm">Total Users</p>
          <h3 className="text-lg sm:text-xl font-bold text-sky-600">
            1,245
          </h3>
        </Card>

        <Card>
          <p className="text-gray-500 text-sm">Active Sessions</p>
          <h3 className="text-lg sm:text-xl font-bold text-green-600">
            89
          </h3>
        </Card>

        <Card>
          <p className="text-gray-500 text-sm">Revenue</p>
          <h3 className="text-lg sm:text-xl font-bold text-purple-600">
            ₹42,500
          </h3>
        </Card>

        <Card>
          <p className="text-gray-500 text-sm">System Status</p>
          <h3 className="text-sm sm:text-base font-bold text-green-600 break-words">
            All Systems Operational
          </h3>
          <Badge>Online</Badge>
        </Card>

      </div>

  
      <div className="mt-10">

        <Card title="User Growth">

          <div className="w-full h-[250px] sm:h-[300px]">

            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>

                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />

                <Line dataKey="users" stroke="#0ea5e9" strokeWidth={3} type="monotone"/>

              </LineChart>
            </ResponsiveContainer>

          </div>

        </Card>

      </div>

      <div className="mt-10">

        <Card title="Recent Activity">
          <ul className="space-y-3 text-gray-600 text-sm">
            <li>New user registered</li>
            <li>Profile updated</li>
            <li>Payment received</li>
          </ul>
        </Card>

      </div>

    </div>
  );
}