import Card from "../../../components/ui/Card";

export const metadata = {
  title: "About – SaaS Hub",
  description: "Learn more about SaaS Hub admin dashboard platform.",
};

export default function AboutPage() {
  return (
    <div>

      <section className="max-w-5xl mx-auto px-6 py-20">

        <h1 className="text-4xl font-bold text-gray-900 text-center">
          About SaaS Hub
        </h1>

        <p className="mt-8 text-gray-600 text-lg leading-relaxed text-center max-w-3xl mx-auto">
          SaaS Hub is a modern admin dashboard platform designed for managing
          users, analytics, billing, and system configurations in a clean,
          scalable and professional interface.
        </p>

        <div className="mt-16 grid md:grid-cols-3 gap-8">

          <Card>
            <h3 className="text-xl font-semibold text-blue-600">
              Scalable Architecture
            </h3>
            <p className="mt-4 text-gray-600">
              Built using Next.js App Router and reusable component system.
            </p>
          </Card>

          <Card>
            <h3 className="text-xl font-semibold text-blue-600">
              Modern UI System
            </h3>
            <p className="mt-4 text-gray-600">
              TailwindCSS utility-first styling with responsive layout.
            </p>
          </Card>

          <Card>
            <h3 className="text-xl font-semibold text-blue-600">
              Enterprise Ready
            </h3>
            <p className="mt-4 text-gray-600">
              Designed to reflect real-world SaaS dashboard structure.
            </p>
          </Card>

        </div>

      </section>
      
      <section id="contact" className="py-20 border-t border-white/30">

        <div className="max-w-4xl mx-auto px-6 text-center">

          <h2 className="text-3xl font-semibold text-gray-900">
            Contact Us
          </h2>

          <p className="mt-6 text-gray-600">
            Have questions or feedback? We'd love to hear from you.
          </p>

          <div className="mt-10 grid md:grid-cols-2 gap-6">

            <Card>
              <h4 className="font-semibold text-gray-900">
                Email
              </h4>
              <p className="text-gray-600 mt-2">
                support@saashub.com
              </p>
            </Card>

            <Card>
              <h4 className="font-semibold text-gray-900">
                Office
              </h4>
              <p className="text-gray-600 mt-2">
                123 Tech Street, Startup City
              </p>
            </Card>

          </div>

        </div>

      </section>

    </div>
  );
}