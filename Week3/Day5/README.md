# Week 3 – Advanced Frontend  
Next.js + TailwindCSS- SaaS Hub Dashboard

## Overview

This project was built during Week 3 of Advanced Frontend training.  
The goal was to create a multi-page, responsive UI using Next.js (App Router) and TailwindCSS with a reusable component system and clean routing structure.

---

## Tech Stack

- Next.js (App Router)
- React
- TailwindCSS
- next/image
- JavaScript

---

## Work Summary (Day Wise)

### Day 1
- TailwindCSS setup
- Global layout creation
- Navbar and Sidebar components
- Dashboard layout skeleton

### Day 2
- Built reusable UI components:
  - Button
  - Input
  - Card
  - Badge
  - Modal
- Followed atomic design approach

### Day 3
- Implemented file-based routing
- Created nested dashboard layout
- Pages: `/`, `/about`, `/dashboard`, `/dashboard/profile`

### Day 4
- Built responsive landing page
- Implemented image optimization
- Added SEO metadata
- Improved typography and layout responsiveness

### Day 5 (Capstone)
- Built full multi-page UI (no backend):
  - `/login`
  - `/dashboard`
  - `/dashboard/users`
  - `/dashboard/profile`
- Reused components from `/components/ui`
- Ensured clean structure and mobile responsiveness

---

## Screenshots

Landing Page  
<img width="1813" height="862" alt="landingpage" src="https://github.com/user-attachments/assets/1817fdbc-f393-4b0f-bafd-88566fba5c82" />

Dashboard  
<img width="1813" height="920" alt="dashboard" src="![alt text](<Screenshot from 2026-04-25 12-33-40.png>)">

Users Page  
<img width="1813" height="920" alt="userpage" src="https://github.com/user-attachments/assets/f8d71d86-0880-4d65-bbf7-1e772757f7da" />

Profile Page  
<img width="1813" height="920" alt="profile" src="https://github.com/user-attachments/assets/18898494-b96b-4bf5-bfb0-d8d69ac067f5" />

Login Page  
<img width="1813" height="920" alt="login" src="https://github.com/user-attachments/assets/f4f399d1-6282-4e43-9a36-df5a1b4caf40" />

---

## Tech Stack

- Next.js (App Router)
- React
- TailwindCSS
- JavaScript

---

## Folder Structure

app/
 ├── layout.jsx
 ├── page.jsx
 ├── globals.css
 ├── favicon.ico
 │
 ├── login/
 ├── signup/
 ├── ping/
 │
 └── dashboard/
      ├── layout.jsx
      ├── page.jsx
      ├── about/
      ├── analytics/
      ├── billing/
      ├── products/
      ├── profile/
      ├── settings/
      └── users/

components/
 └── ui/
      ├── Badge.jsx
      ├── Button.jsx
      ├── Card.jsx
      ├── Input.jsx
      ├── Modal.jsx
      ├── Navbar.jsx
      └── Sidebar.jsx

---

## How to Run

git clone <repository-link>  
cd project-folder  
npm install  
npm run dev  

Open http://localhost:3000

---

## Learning Outcomes

- Understanding Next.js App Router
- Nested layouts implementation
- Reusable component architecture
- Managing large folder structure
- Building scalable dashboard UI

---