export default function Badge({ children }) {
  return (
    <span className="px-2 py-1 text-xs bg-sky-100 text-sky-700 rounded-full">
      {children}
    </span>
  );
}
