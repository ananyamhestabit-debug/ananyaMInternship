"use client";
import { useState } from "react";
import Button from "./Button";

export default function Modal({ triggerText, children }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setOpen(true)}>{triggerText}</Button>

      {open && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
          <div className="bg-white p-6 rounded-xl w-96">
            <div className="mb-4">{children}</div>
            <Button className="bg-yellow-400 text-gray-900 hover:bg-yellow-500 px-5 py-2 w-full" onClick={() => setOpen(false)}>
              Close
            </Button>
          </div>
        </div>
      )}
    </>
  );
}
