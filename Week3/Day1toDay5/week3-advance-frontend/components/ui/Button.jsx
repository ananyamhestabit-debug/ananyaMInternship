// components/ui/Button.jsx
"use client";

export default function Button({ children, variant = "primary", onClick }) {
  const base =
    "px-5 py-2 rounded-xl font-medium transition duration-300 shadow-sm";

  const styles = {
    primary:
      "bg-yellow-400 text-gray-900 hover:bg-yellow-500",  // Golden color for primary buttons
    secondary:
      "bg-gray-200 text-gray-800 hover:bg-gray-300",
    danger:
      "bg-yellow-500 text-white hover:bg-yellow-600",  // Golden color for danger (e.g., Logout)
  };

  return (
    <button onClick={onClick} className={`${base} ${styles[variant]}`}>
      {children}
    </button>
  );
}
