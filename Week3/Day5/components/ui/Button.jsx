"use client";

export default function Button({ children, onClick, className = "" }) {
  return (
    <button
      onClick={onClick}
      className={`px-5 py-2 rounded-lg transition ${className}`}
    >
      {children}
    </button>
  );
}