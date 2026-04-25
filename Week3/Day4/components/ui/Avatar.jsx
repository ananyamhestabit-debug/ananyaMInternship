import Image from "next/image";

export default function Avatar({
  src = "/user.png",
  alt = "User",
  size = 40,
  className = "",
}) {
  return (
    <Image
      src={src}
      alt={alt}
      width={size}
      height={size}
      className={`rounded-full border object-cover ${className}`}
    />
  );
}