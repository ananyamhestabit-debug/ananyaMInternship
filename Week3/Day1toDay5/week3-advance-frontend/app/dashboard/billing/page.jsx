import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";

export default function BillingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100 p-6">

      <h2 className="text-3xl font-semibold text-gray-900 mb-8 tracking-tight">
        Billing & Subscription
      </h2>

      <Card>
        <p className="text-gray-700 text-lg">
          Current Plan: <strong className="text-blue-600">Pro</strong>
        </p>

        <p className="text-sm text-gray-500 mt-2">
          Next Billing Date: 12 March 2026
        </p>

        <div className="mt-6">
          <Button>
            Upgrade Plan
          </Button>
        </div>
      </Card>

    </div>
  );
}
