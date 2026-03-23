"use client";

export default function Button(props) {

  const {
    children,
    variant = "primary",
    size = "md",
    onClick,
    disabled = false,
    className = "",
  } = props;

  const baseStyles =
    "font-medium transition-all duration-200 rounded-lg";

  const sizeStyles = {
    sm: "px-3 py-1 text-sm",
    md: "px-5 py-2",
    lg: "px-6 py-3",
  };

  const colorMap = {
    primary:
      "bg-yellow-400 text-gray-900 hover:bg-yellow-500",

    secondary:
      "bg-blue-100 text-blue-700 hover:bg-blue-200",

    danger:
      "bg-red-500 text-white hover:bg-red-600",
  };

  const appliedColor =
    colorMap[variant] || colorMap.primary;

  const appliedSize =
    sizeStyles[size] || sizeStyles.md;

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`
        ${baseStyles}
        ${appliedSize}
        ${appliedColor}
        ${disabled ? "opacity-50 cursor-not-allowed" : ""}
        ${className}
      `}
    >
      {children}
    </button>
  );
}