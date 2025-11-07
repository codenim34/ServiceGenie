# ServiceGenie Frontend

Frontend application for ServiceGenie - AI-powered commerce platform.

## Tech Stack

- **Next.js 14** (App Router) with TypeScript
- **Firebase Authentication**
- **Tailwind CSS**
- **Axios** for API calls

## Setup

1. Install dependencies:
```bash
npm install
```

2. Copy `.env.local.example` to `.env.local` and fill in your Firebase credentials:
```bash
cp .env.local.example .env.local
```

3. Update `.env.local` with your Firebase configuration and backend URL.

## Running the Application

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

## Features

- User authentication (login/register)
- Product management (create, read, update, delete)
- Order management
- AI chat assistant
- Owner dashboard with analytics

## Project Structure

```
frontend/
├── app/              # Next.js app router pages
├── components/       # React components
├── lib/             # Utilities and API client
└── styles/          # Global styles
```
