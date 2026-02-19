import Card from "@/components/ui/Card"
import Input from "@/components/ui/Input"
import Button from "@/components/ui/Button"

export default function ProfilePage() {
  return (
    <Card>
      <h2 className="text-xl font-semibold mb-4">
        Admin Profile
      </h2>

      <div className="space-y-4">
        <Input placeholder="Full Name" />
        <Input placeholder="Email Address" />
        <Button>Save Changes</Button>
      </div>
    </Card>
  )
}
