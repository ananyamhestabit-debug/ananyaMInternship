import Card from "../../../components/ui/Card";
import Button from "../../../components/ui/Button";

export default function SettingsPage() {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Settings
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <Card>
          <h3 className="text-lg font-semibold mb-4 text-gray-800">
            App Settings
          </h3>

          <div className="space-y-3 text-sm text-gray-700">
            <div className="flex items-center justify-between">
              <span>Notifications</span>
              <span className="text-green-600 font-medium">Enabled</span>
            </div>

            <div className="flex items-center justify-between">
              <span>Email Reports</span>
              <span className="text-green-600 font-medium">Enabled</span>
            </div>

            <div className="flex items-center justify-between">
              <span>Auto Backup</span>
              <span className="text-green-600 font-medium">Enabled</span>
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-semibold mb-4 text-gray-800">
            Theme & Preferences
          </h3>

          <div className="space-y-4 text-sm text-gray-700">
            <div className="flex items-center justify-between">
              <span>Dark Mode</span>
              <input type="checkbox" className="w-5 h-5" />
            </div>

            <div className="flex items-center justify-between">
              <span>Compact Layout</span>
              <input type="checkbox" className="w-5 h-5" />
            </div>

            <div className="flex items-center justify-between">
              <span>Show Email Alerts</span>
              <input type="checkbox" className="w-5 h-5" />
            </div>
          </div> 

          <Button variant="secondary" className="mt-6">
            Save Preferences
          </Button>

        </Card>
      </div>
    </div>
  );
}