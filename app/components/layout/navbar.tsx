'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Dumbbell, Calendar, LineChart, User, LogOut } from 'lucide-react';
import { useUser } from '../../contexts/user-context';

const navigation = [
  { name: 'Training Plans', href: '/training-plans', icon: Dumbbell },
  { name: 'Progress', href: '/progress', icon: LineChart },
];

export function Navbar() {
  const pathname = usePathname();
  const { user, logout } = useUser();

  // Don't show navbar on login/signup pages
  if (['/login', '/signup'].includes(pathname)) {
    return null;
  }

  return (
    <nav className="border-b bg-background">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between">
          <div className="flex">
            <div className="flex flex-shrink-0 items-center">
              <Link href="/" className="text-xl font-bold">
                Gym Bacteria
              </Link>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {navigation.map((item) => {
                const isActive = pathname.startsWith(item.href);
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                      isActive
                        ? 'border-b-2 border-primary text-foreground'
                        : 'text-muted-foreground hover:text-foreground'
                    }`}
                  >
                    <item.icon className="mr-2 h-4 w-4" />
                    {item.name}
                  </Link>
                );
              })}
            </div>
          </div>

          {user && (
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-sm">
                <User className="mr-2 h-4 w-4 text-muted-foreground" />
                <span>{user.nickname}</span>
              </div>
              <button
                onClick={logout}
                className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground h-9 px-3"
              >
                <LogOut className="mr-2 h-4 w-4" />
                Sign out
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
} 