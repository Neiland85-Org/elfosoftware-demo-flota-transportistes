'use client';

import { useTranslationContext } from '@/lib/hooks/TranslationProvider';
import Link from 'next/link';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const { t, currentLang, changeLanguage } = useTranslationContext();

  const handleLanguageChange = (lang: 'en' | 'ca') => {
    changeLanguage(lang);
  };

  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <header className='bg-white shadow-sm border-b'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex justify-between items-center h-16'>
            {/* Logo */}
            <div className='flex items-center'>
              <Link href='/' className='text-xl font-bold text-gray-900'>
                🚛 Elfosoftware
              </Link>
            </div>

            {/* Navigation */}
            <nav className='hidden md:flex space-x-8'>
              <Link
                href='/'
                className='text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium'
              >
                {t('navigation.home')}
              </Link>
              <Link
                href='/vehicles'
                className='text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium'
              >
                {t('navigation.vehicles')}
              </Link>
              <Link
                href='/dashboard'
                className='text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium'
              >
                {t('navigation.dashboard')}
              </Link>
            </nav>

            {/* Language Selector */}
            <div className='flex items-center space-x-4'>
              <select
                value={currentLang}
                onChange={e =>
                  handleLanguageChange(e.target.value as 'en' | 'ca')
                }
                className='bg-white border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
              >
                <option value='en'>English</option>
                <option value='ca'>Català</option>
              </select>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        {children}
      </main>

      {/* Footer */}
      <footer className='bg-white border-t mt-16'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
          <div className='text-center text-gray-500 text-sm'>
            <p>&copy; 2024 Elfosoftware - Flota Transportistes</p>
            <p className='mt-2'>
              Arquitectura DELFOS - Domain-driven Enterprise Layered Framework
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
