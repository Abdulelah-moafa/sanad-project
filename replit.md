# Nabd | نبض Medical AI Application

## Overview

Nabd (نبض - meaning "pulse" in Arabic) is an Arabic-first medical AI platform built with **React 19** and Express. The application provides four core AI-powered healthcare features: mental health analysis (Farah), an intelligent medical chatbot, facial emotion detection with **TRUE LIVE STREAMING** (Mirror), and a Drug Interaction Checker. The platform features a modern glassmorphism design with full RTL (Right-to-Left) Arabic support.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Technology Stack

**Frontend:**
- React 19 with TypeScript
- Vite for development and bundling
- TailwindCSS for styling
- Shadcn/ui component library
- face-api.js for browser-based emotion detection
- wouter for client-side routing

**Backend:**
- Express.js server
- HuggingFace API for AI features (sentiment analysis, chatbot)
- TypeScript

**Design System:**
- Glassmorphism aesthetic with translucent backgrounds and backdrop blur effects
- Arabic-first UX with RTL (right-to-left) layout enforcement via CSS
- Purple gradient theme (#4e54c8 to #8f94fb)
- Responsive design with mobile considerations

### Application Structure

**Frontend:** `client/src/` - React 19 application
- `pages/Home.tsx` - Dashboard with service overview cards
- `pages/Farah.tsx` - Mental health chat with persona selection
- `pages/Doctor.tsx` - AI-powered medical chatbot
- `pages/Mirror.tsx` - TRUE LIVE camera streaming with face-api.js emotion detection
- `pages/Drugs.tsx` - Drug interaction checker

**Backend:** `server/` - Express.js API
- `routes.ts` - API endpoints for AI features
- `vite.ts` - Vite development server integration

### State Management

- React hooks (useState, useRef, useCallback)
- TanStack Query for API data fetching
- Browser MediaDevices API for camera access

## External Dependencies

### AI/ML Services

**Hugging Face Inference API:**
- Model: `Qwen/Qwen2.5-72B-Instruct` for Arabic medical chatbot
- Model: `CAMeL-Lab/bert-base-arabic-camelbert-msa-sentiment` for sentiment analysis
- Authentication via `HUGGINGFACE_API_TOKEN` secret

**face-api.js:**
- Browser-based facial emotion detection (no server required)
- Uses TensorFlow.js models loaded from CDN
- Real-time emotion overlay on live video stream

### Key Dependencies

- `react@19` - Latest React version
- `face-api.js` - Browser-based emotion detection
- `wouter` - Lightweight client-side routing
- `@tanstack/react-query` - Data fetching
- `tailwindcss` - Utility-first CSS
- `shadcn/ui` - Component library

## Configuration

### Environment Variables

- `HUGGINGFACE_API_TOKEN` - Required for AI chatbot functionality

## Running the Application

The application runs via Vite development server:

```bash
npm run dev
```

This starts Express.js server with Vite middleware serving the React frontend on port 5000.

## Features Detail

### Farah (فرح) - Mental Health

- Text input for emotional expression
- Simulated depression/anxiety analysis (demo mode)
- Color-coded severity levels (green/yellow/red)
- Wellness tips and recommendations

### Smart Doctor (طبيبك الذكي)

- Conversational AI chat interface
- Arabic language responses
- Medical advice with disclaimer
- Chat history within session

### Emotion Mirror (مرآة المشاعر)

- **TRUE LIVE STREAMING** using browser's MediaDevices API and face-api.js
- Real-time emotion overlay drawn on canvas over video feed
- Uses requestAnimationFrame for smooth 30fps detection
- Throttled processing (every 5th frame) for performance
- Confidence scores for all detected emotions
- Personalized advice based on detected emotion
- FPS counter showing detection performance

## Design Decisions

1. **React 19 Architecture:** Modern React with hooks, TypeScript, and Vite
2. **RTL Support:** CSS-based RTL enforcement for Arabic text
3. **Browser-Based ML:** face-api.js for client-side emotion detection (no server round-trips)
4. **Glassmorphism Design:** Translucent cards with backdrop blur, purple gradients
5. **wouter Routing:** Lightweight client-side navigation
6. **TanStack Query:** Efficient data fetching with caching
7. **Farah Personas:** Three character assistants (Batman, Barbie, Panda) for mental health support
8. **Drug Interaction Checker:** AI-powered drug interaction analysis via HuggingFace

## Recent Changes

- **December 2024:** Migrated from Streamlit to React 19 with Express backend
- **December 2024:** Implemented TRUE LIVE camera streaming with face-api.js
- **December 2024:** Real-time emotion overlay on video with canvas
- **December 2024:** All AI features working via HuggingFace API
- **December 2024:** Bright glassmorphism design with RTL Arabic support
