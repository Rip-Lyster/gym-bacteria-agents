import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Navbar } from './components/layout/navbar'
import { UserProvider } from './contexts/user-context'

// Initialize Inter font with Latin subset
const inter = Inter({ subsets: ['latin'] })

/**
 * Application metadata configuration
 * Defines core SEO properties for the application
 */
export const metadata: Metadata = {
  title: 'Gym Bacteria - Training Management System',
  description: 'Advanced training plan and workout management system',
}

/**
 * Root layout component that wraps all pages
 * Provides common structure and styling across the application
 * @param {Object} props - Component properties
 * @param {React.ReactNode} props.children - Child components to be rendered within the layout
 * @returns {JSX.Element} The rendered layout structure
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-background antialiased`}>
        <UserProvider>
          <div className="relative flex min-h-screen flex-col">
            <Navbar />
            <div className="flex-1">{children}</div>
          </div>
        </UserProvider>
      </body>
    </html>
  )
}
