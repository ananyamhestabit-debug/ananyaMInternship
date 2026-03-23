export default function Input({
  type = "text",
  placeholder,
  className = "",
}) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      className={`w-full border border-gray-300 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-400 ${className}`}
    />
  );
}