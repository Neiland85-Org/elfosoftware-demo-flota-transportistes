'use client';

import Layout from '@/components/Layout';
import { TranslationProvider } from '@/lib/hooks/TranslationProvider';

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <TranslationProvider>
      <Layout>{children}</Layout>
    </TranslationProvider>
  );
}
