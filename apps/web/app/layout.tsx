import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Flota Transportistes',
  description: 'Sistema de gestión de flota de transportistas',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang='es'>
      <body>{children}</body>
    </html>
  );
}
