import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";

export default function ProductsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100 p-6">

      <h2 className="text-3xl font-semibold text-gray-900 mb-8 tracking-tight">
        Products & Plans
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {["Starter Plan", "Pro Plan", "Enterprise Plan"].map((plan) => (
          <Card key={plan}>
            <h3 className="text-xl font-semibold text-blue-600">
              {plan}
            </h3>

            <p className="text-sm text-gray-600 mt-2">
              Subscription product for SaaS customers.
            </p>

            <div className="mt-4">
              <Badge>Active</Badge>
            </div>
          </Card>
        ))}

      </div>
    </div>
  );
}
