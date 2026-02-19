import Link from "next/link";
import Image from "next/image";

export const metadata = {
  title: "SaaS Hub – Admin Dashboard",
  description:
    "SaaS Hub is a modern and responsive admin dashboard built with Next.js and Tailwind CSS.",
};

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-yellow-50 to-yellow-100 p-6">

      {/* Hero Section */}
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

  <span className="text-sky-600">
    SaaS Hub
  </span>

  <span>Dashboard</span>

</h1>


        <p className="mt-6 text-gray-600 max-w-2xl mx-auto text-base sm:text-lg">
          SaaS Hub is a modern admin dashboard designed to manage users,
          analytics, subscriptions, and application settings with a clean,
          scalable and responsive interface.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row justify-center gap-4">
          <Link
            href="/dashboard"
            className="bg-sky-600 text-white px-6 py-3 rounded-xl shadow hover:bg-sky-700 transition"
          >
            Go to Dashboard
          </Link>

          <Link
            href="/login"
            className="border border-sky-600 text-sky-600 px-6 py-3 rounded-xl hover:bg-sky-50 transition"
          >
            Login
          </Link>
        </div>

      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center text-gray-900">
          Powerful Features
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">

          <div className="bg-white p-6 rounded-2xl shadow hover:shadow-xl hover:-translate-y-1 transition duration-300">
            <h3 className="text-xl font-semibold text-gray-800">
              User Management
            </h3>
            <p className="text-gray-600 mt-3">
              Manage users, roles, and permissions efficiently from a central dashboard interface.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow hover:shadow-xl hover:-translate-y-1 transition duration-300">
            <h3 className="text-xl font-semibold text-gray-800">
              Analytics & Insights
            </h3>
            <p className="text-gray-600 mt-3">
              Monitor system activity, user growth, and revenue metrics with structured UI components.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow hover:shadow-xl hover:-translate-y-1 transition duration-300">
            <h3 className="text-xl font-semibold text-gray-800">
              Secure Settings
            </h3>
            <p className="text-gray-600 mt-3">
              Configure application settings, preferences, and system controls securely and efficiently.
            </p>
          </div>

        </div>
      </section>

<section id="contact" className="py-20 border-t">
  <div className="max-w-4xl mx-auto px-6 text-center">
    <h2 className="text-3xl font-semibold text-gray-900">What Our Users Say</h2>
    <div className="mt-12 grid md:grid-cols-3 gap-8">
      <div className="p-6 rounded-2xl shadow bg-white hover:shadow-xl hover:-translate-y-1 transition duration-300">
        <p className="text-gray-600">
          “SaaS Hub helped us streamline our user management process.”
        </p>
        <h4 className="mt-4 font-semibold text-gray-800">– Product Manager</h4>
      </div>
      <div className="p-6 rounded-2xl shadow bg-white hover:shadow-xl hover:-translate-y-1 transition duration-300">
        <p className="text-gray-600">
          “The dashboard UI is clean and easy to use.”
        </p>
        <h4 className="mt-4 font-semibold text-gray-800">– Startup Founder</h4>
      </div>
      <div className="p-6 rounded-2xl shadow bg-white hover:shadow-xl hover:-translate-y-1 transition duration-300">
        <p className="text-gray-600">
          “Analytics section gives clear visibility into system activity.”
        </p>
        <h4 className="mt-4 font-semibold text-gray-800">– Operations Lead</h4>
      </div>
    </div>
  </div>
</section>

      <footer className="bg-white border-t text-center py-6 text-gray-500 text-sm">
        © 2026 SaaS Hub. All rights reserved.
      </footer>

    </div>
  );
}
