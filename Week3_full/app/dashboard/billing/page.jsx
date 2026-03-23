import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";

export default function BillingPage() {
  return (
    <div>

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
          <Button variant="primary" >
            Upgrade Plan
          </Button>
        </div>
      </Card>

    </div>
  );
}
