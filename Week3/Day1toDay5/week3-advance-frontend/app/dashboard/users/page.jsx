import Card from "@/components/ui/Card";

const users = [
  { name: "Ananya Mishra", role: "Admin", status: "Online" },
  { name: "Rahul Sharma", role: "Developer", status: "Offline" },
  { name: "Priya Verma", role: "Manager", status: "Online" },
];

export default function Users() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100 p-6">

      <Card title="Users Management" >

        <div className="overflow-x-auto">

          <table className="min-w-full text-left">

            <thead className="border-b">
              <tr className="text-gray-600 uppercase text-xs tracking-wide">
                <th className="py-3">Name</th>
                <th>Role</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user, index) => (
                <tr key={index} className="border-b hover:bg-blue-50 transition">

                  <td className="py-4 text-gray-900 font-medium">
                    {user.name}
                  </td>

                  <td className="text-gray-700">
                    {user.role}
                  </td>

                  <td>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${
                        user.status === "Online"
                          ? "bg-green-100 text-green-700"
                          : "bg-gray-200 text-gray-600"
                      }`}
                    >
                      {user.status}
                    </span>
                  </td>

                </tr>
              ))}
            </tbody>

          </table>

        </div>

      </Card>

    </div>
  );
}
