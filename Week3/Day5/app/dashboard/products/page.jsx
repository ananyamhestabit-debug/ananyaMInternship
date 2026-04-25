import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";

export default function ProductsPage() {

  const plans = [
    { name: "Starter Plan", active: false },
    { name: "Pro Plan", active: true },
    { name: "Enterprise Plan", active: false },
  ];

  return (
    <div className="min-h-screen p-4 sm:p-6">

      <h2 className="text-xl sm:text-3xl font-semibold text-gray-900 mb-8 tracking-tight">
        Products & Plans
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

        {plans.map((plan) => (
          <Card key={plan.name}>

            <h3 className="text-lg sm:text-xl font-semibold text-blue-600 break-words">
              {plan.name}
            </h3>

            <p className="text-sm text-gray-600 mt-2">
              Subscription product for SaaS customers.
            </p>

            <div className="mt-4 flex items-center justify-between">

              {plan.active ? (
                <Badge>Active</Badge>
              ) : (
                <span className="text-gray-400 text-sm">
                  Inactive
                </span>
              )}

            </div>

          </Card>
        ))}

      </div>

    </div>
  );
}