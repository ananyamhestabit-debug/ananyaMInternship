export default function Card({ title, children, className = "" }) {
  return (
    <div
      className={`w-full min-w-0 bg-white/80 backdrop-blur-md border border-blue-100 shadow-lg rounded-xl p-4 sm:p-6 transition hover:shadow-xl hover:-translate-y-1 duration-300 overflow-hidden ${className}`}
    >
      {title && (
        <h2 className="text-base sm:text-lg font-semibold text-blue-600 mb-3 break-words">
          {title}
        </h2>
      )}

      <div className="break-words text-sm sm:text-base">
        {children}
      </div>
    </div>
  );
}