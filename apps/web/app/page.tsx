import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Inicio | Flota Transportistes',
  description: 'Panel principal del sistema de gestión de flota',
};

export default function HomePage() {
  return (
    <div className='container mx-auto px-4 py-8'>
      <div className='max-w-4xl mx-auto'>
        {/* Header */}
        <div className='text-center mb-12'>
          <h1 className='text-4xl font-bold text-gray-900 mb-4'>
            🚛 Elfosoftware
          </h1>
          <h2 className='text-2xl font-semibold text-gray-700 mb-2'>
            Sistema de Gestión de Flota
          </h2>
          <p className='text-lg text-gray-600'>
            Arquitectura DELFOS - Domain-driven Enterprise Layered Framework for
            Optimal Solutions
          </p>
        </div>

        {/* Cards de funcionalidades */}
        <div className='grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12'>
          <div className='bg-white rounded-lg shadow-md p-6'>
            <div className='text-3xl mb-4'>🏭</div>
            <h3 className='text-xl font-semibold mb-2'>Dominio Flota</h3>
            <p className='text-gray-600'>
              Gestión completa de vehículos, conductores y recursos de
              transporte.
            </p>
          </div>

          <div className='bg-white rounded-lg shadow-md p-6'>
            <div className='text-3xl mb-4'>📍</div>
            <h3 className='text-xl font-semibold mb-2'>Tracking GPS</h3>
            <p className='text-gray-600'>
              Seguimiento en tiempo real de la flota y optimización de rutas.
            </p>
          </div>

          <div className='bg-white rounded-lg shadow-md p-6'>
            <div className='text-3xl mb-4'>📊</div>
            <h3 className='text-xl font-semibold mb-2'>Analytics</h3>
            <p className='text-gray-600'>
              Reportes y análisis de rendimiento de la flota de transportistas.
            </p>
          </div>
        </div>

        {/* Estado del proyecto */}
        <div className='bg-white rounded-lg shadow-md p-6'>
          <h3 className='text-xl font-semibold mb-4'>📋 Estado del Proyecto</h3>
          <div className='grid md:grid-cols-2 gap-4'>
            <div className='flex items-center'>
              <span className='text-green-500 mr-2'>✅</span>
              <span>Configuración organizacional completa</span>
            </div>
            <div className='flex items-center'>
              <span className='text-green-500 mr-2'>✅</span>
              <span>Arquitectura DELFOS definida</span>
            </div>
            <div className='flex items-center'>
              <span className='text-yellow-500 mr-2'>🚧</span>
              <span>Implementación del dominio Flota</span>
            </div>
            <div className='flex items-center'>
              <span className='text-yellow-500 mr-2'>🚧</span>
              <span>APIs REST con FastAPI</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
