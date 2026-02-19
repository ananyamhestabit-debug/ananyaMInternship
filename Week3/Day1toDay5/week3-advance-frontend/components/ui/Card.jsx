// components/ui/Card.jsx
export default function Card({ title, children }) {
  return (
    <div className="bg-white/80 backdrop-blur-md border border-blue-100 shadow-lg rounded-xl p-6 transition hover:shadow-xl hover:-translate-y-1 duration-300">
      {title && (
        <h2 className="text-xl font-semibold text-blue-600 mb-4 tracking-tight">
          {title}
        </h2>
      )}
      {children}
    </div>
  );
}
