import Card from "@/components/ui/Card";

export default function AnalyticsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100 p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Analytics
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <p className="text-gray-500 text-sm">Monthly Growth</p>
          <h3 className="text-2xl font-bold text-green-600">+24%</h3>
        </Card>

        <Card>
          <p className="text-gray-500 text-sm">New Signups</p>
          <h3 className="text-2xl font-bold text-sky-600">312</h3>
        </Card>

        <Card>
          <p className="text-gray-500 text-sm">Churn Rate</p>
          <h3 className="text-2xl font-bold text-red-500">3.1%</h3>
        </Card>
      </div>
    </div>
  );
}
