import Link from "next/link";
import Image from "next/image";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";

export const metadata = {
  title: "SaaS Hub – Admin Dashboard",
  description:
    "SaaS Hub is a modern and responsive admin dashboard built with Next.js and Tailwind CSS.",
};

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100 p-6">

     
      <section className="text-center py-16 sm:py-20 px-4 sm:px-6 max-w-6xl mx-auto">
        
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 leading-tight flex flex-wrap justify-center items-center gap-3">
          <span>Welcome to</span>

          <Image
            src="/logo3.png"
            alt="SaaS Hub Logo"
            width={60}
            height={60}
            className="object-contain"
            priority
          />

          <span className="text-sky-600">SaaS Hub</span>
          <span>Dashboard</span>
        </h1>

        <p className="mt-6 text-gray-600 max-w-2xl mx-auto text-base sm:text-lg">
          SaaS Hub is a modern admin dashboard designed to manage users,
          analytics, subscriptions, and application settings with a clean,
          scalable and responsive interface.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row justify-center gap-4">

          <Link href="/dashboard" className="block w-full sm:w-auto">
          <Button className="bg-yellow-400 text-gray-900 hover:bg-yellow-500 px-6 py-3 w-full">
          Go to Dashboard
          </Button>
          </Link>

          <Link href="/login" className="block w-full sm:w-auto">
          <Button className="bg-sky-200  text-gray-900 hover:bg-sky-300 px-6 py-3 w-full">
          Login
          </Button>
          </Link>

</div>

      </section>

     
      <section className="py-16 px-4 sm:px-6 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center text-gray-900">
          Powerful Features
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">

          <Card>
            <h3 className="text-xl font-semibold text-gray-800">
              User Management
            </h3>
            <p className="text-gray-600 mt-3">
              Manage users, roles, and permissions efficiently from a central dashboard interface.
            </p>
          </Card>

          <Card>
            <h3 className="text-xl font-semibold text-gray-800">
              Analytics & Insights
            </h3>
            <p className="text-gray-600 mt-3">
              Monitor system activity, user growth, and revenue metrics with structured UI components.
            </p>
          </Card>

          <Card>
            <h3 className="text-xl font-semibold text-gray-800">
              Secure Settings
            </h3>
            <p className="text-gray-600 mt-3">
              Configure application settings, preferences, and system controls securely and efficiently.
            </p>
          </Card>

        </div>
      </section>

  
      <section id="contact" className="py-20 border-t">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-semibold text-gray-900">
            What Our Users Say
          </h2>

          <div className="mt-12 grid md:grid-cols-3 gap-8">

            <Card>
              <p className="text-gray-600">
                “SaaS Hub helped us streamline our user management process.”
              </p>
              <h4 className="mt-4 font-semibold text-gray-800">
                – Product Manager
              </h4>
            </Card>

            <Card>
              <p className="text-gray-600">
                “The dashboard UI is clean and easy to use.”
              </p>
              <h4 className="mt-4 font-semibold text-gray-800">
                – Startup Founder
              </h4>
            </Card>

            <Card>
              <p className="text-gray-600">
                “Analytics section gives clear visibility into system activity.”
              </p>
              <h4 className="mt-4 font-semibold text-gray-800">
                – Operations Lead
              </h4>
            </Card>

          </div>
        </div>
      </section>

    
      <footer className="bg-gradient-to-br from--yellow-100 to-yellow-100 p-6 border-t text-center py-6 text-gray-500 text-sm">
        © 2026 SaaS Hub. All rights reserved.
      </footer>

    </div>
  );
}