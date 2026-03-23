import Card from "../../../components/ui/Card";
import Badge from "../../../components/ui/Badge";
import Modal from "../../../components/ui/Modal";
import Button from "../../../components/ui/Button";

const users = [
  { name: "Ananya Mishra", role: "Admin", status: "Online" },
  { name: "Rahul Sharma", role: "Developer", status: "Offline" },
  { name: "Priya Verma", role: "Manager", status: "Online" },
];

export default function Users() {
  return (
    <div className="min-h-screen p-4 sm:p-6">

      <Card title="Users Management">

        <div className="overflow-x-auto">

          <table className="min-w-[600px] w-full text-left text-sm">

            <thead className="border-b">
              <tr className="text-gray-600 uppercase text-xs tracking-wide">
                <th className="py-3 px-2">Name</th>
                <th className="px-2">Role</th>
                <th className="px-2">Status</th>
                <th className="px-2 text-center">Action</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user, index) => (
                <tr
                  key={index}
                  className="border-b hover:bg-blue-50 transition"
                >

                  <td className="py-3 px-2 font-medium text-gray-900 break-words">
                    {user.name}
                  </td>

                  <td className="px-2 text-gray-700 break-words">
                    {user.role}
                  </td>

                  <td className="px-2 whitespace-nowrap">
                    <Badge>{user.status}</Badge>
                  </td>

                  <td className="px-2 py-3">

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-2 sm:gap-3">

                      <Modal triggerText="View">
                        <p>User: {user.name}</p>
                        <p>Role: {user.role}</p>
                        <p>Status: {user.status}</p>
                      </Modal>

                      <Button variant="danger" className="w-full sm:w-auto">
                        Delete
                      </Button>

                    </div>

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