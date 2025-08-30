'use client';

import { useTranslationContext } from '@/lib/hooks';
import { useEffect, useState } from 'react';

interface Vehicle {
  id: string;
  matricula: string;
  marca: string;
  modelo: string;
  tipo: string;
  capacidad_carga: number;
  estado: string;
  fecha_matriculacion: string;
  kilometraje: number;
}

// Mock data for development
const mockVehicles: Vehicle[] = [
  {
    id: '1',
    matricula: '1234-ABC',
    marca: 'Mercedes',
    modelo: 'Actros',
    tipo: 'truck',
    capacidad_carga: 25000,
    estado: 'available',
    fecha_matriculacion: '2020-01-15',
    kilometraje: 150000,
  },
  {
    id: '2',
    matricula: '5678-DEF',
    marca: 'Volvo',
    modelo: 'FH16',
    tipo: 'truck',
    capacidad_carga: 30000,
    estado: 'inUse',
    fecha_matriculacion: '2019-06-20',
    kilometraje: 200000,
  },
  {
    id: '3',
    matricula: '9012-GHI',
    marca: 'Scania',
    modelo: 'R450',
    tipo: 'truck',
    capacidad_carga: 28000,
    estado: 'maintenance',
    fecha_matriculacion: '2021-03-10',
    kilometraje: 80000,
  },
  {
    id: '4',
    matricula: '3456-JKL',
    marca: 'MAN',
    modelo: 'TGX',
    tipo: 'truck',
    capacidad_carga: 26000,
    estado: 'available',
    fecha_matriculacion: '2022-08-05',
    kilometraje: 45000,
  },
  {
    id: '5',
    matricula: '7890-MNO',
    marca: 'Iveco',
    modelo: 'Stralis',
    tipo: 'truck',
    capacidad_carga: 24000,
    estado: 'outOfService',
    fecha_matriculacion: '2018-11-30',
    kilometraje: 300000,
  },
];

export default function VehiclesPage() {
  const { t } = useTranslationContext();
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const itemsPerPage = 10;

  useEffect(() => {
    fetchVehicles();
  }, []);

  const fetchVehicles = async () => {
    try {
      setLoading(true);
      // Try to fetch from API first
      const response = await fetch('/api/vehicles');

      if (response.ok) {
        const data = await response.json();
        setVehicles(data);
      } else {
        // Fallback to mock data
        setVehicles(mockVehicles);
      }
    } catch (error) {
      // Fallback to mock data
      setVehicles(mockVehicles);
    } finally {
      setLoading(false);
    }
  };

  // Filter vehicles based on search and status
  const filteredVehicles = vehicles.filter(vehicle => {
    const matchesSearch =
      searchTerm === '' ||
      vehicle.matricula.toLowerCase().includes(searchTerm.toLowerCase()) ||
      vehicle.marca.toLowerCase().includes(searchTerm.toLowerCase()) ||
      vehicle.modelo.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus =
      statusFilter === '' || vehicle.estado === statusFilter;

    return matchesSearch && matchesStatus;
  });

  // Pagination
  const totalPages = Math.ceil(filteredVehicles.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedVehicles = filteredVehicles.slice(
    startIndex,
    startIndex + itemsPerPage
  );

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available':
        return 'bg-green-100 text-green-800';
      case 'inUse':
        return 'bg-blue-100 text-blue-800';
      case 'maintenance':
        return 'bg-yellow-100 text-yellow-800';
      case 'outOfService':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className='flex justify-center items-center h-64'>
        <div className='text-lg text-gray-600'>{t('common.loading')}</div>
      </div>
    );
  }

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='flex justify-between items-center'>
        <div>
          <h1 className='text-3xl font-bold text-gray-900'>
            {t('vehicles.title')}
          </h1>
          <p className='text-gray-600 mt-2'>{t('vehicles.subtitle')}</p>
        </div>
        <button className='bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors'>
          {t('vehicles.createVehicle')}
        </button>
      </div>

      {/* Filters */}
      <div className='bg-white p-4 rounded-lg shadow-sm border'>
        <div className='flex flex-col sm:flex-row gap-4'>
          <div className='flex-1'>
            <input
              type='text'
              placeholder={t('common.search')}
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className='w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            />
          </div>
          <div className='sm:w-48'>
            <select
              value={statusFilter}
              onChange={e => setStatusFilter(e.target.value)}
              className='w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            >
              <option value=''>
                {t('common.filter')} {t('vehicles.status')}
              </option>
              <option value='available'>
                {t('vehicleStatuses.available')}
              </option>
              <option value='inUse'>{t('vehicleStatuses.inUse')}</option>
              <option value='maintenance'>
                {t('vehicleStatuses.maintenance')}
              </option>
              <option value='outOfService'>
                {t('vehicleStatuses.outOfService')}
              </option>
            </select>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className='bg-white rounded-lg shadow-sm border overflow-hidden'>
        <div className='overflow-x-auto'>
          <table className='min-w-full divide-y divide-gray-200'>
            <thead className='bg-gray-50'>
              <tr>
                <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                  {t('vehicles.licensePlate')}
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                  {t('vehicles.brand')}
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                  {t('vehicles.model')}
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                  {t('vehicles.type')}
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                  {t('vehicles.capacity')}
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                  {t('vehicles.status')}
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                  {t('vehicles.mileage')}
                </th>
                <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                  {t('vehicles.actions')}
                </th>
              </tr>
            </thead>
            <tbody className='bg-white divide-y divide-gray-200'>
              {paginatedVehicles.map(vehicle => (
                <tr key={vehicle.id} className='hover:bg-gray-50'>
                  <td className='px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900'>
                    {vehicle.matricula}
                  </td>
                  <td className='px-6 py-4 whitespace-nowrap text-sm text-gray-900'>
                    {vehicle.marca}
                  </td>
                  <td className='px-6 py-4 whitespace-nowrap text-sm text-gray-900'>
                    {vehicle.modelo}
                  </td>
                  <td className='px-6 py-4 whitespace-nowrap text-sm text-gray-900'>
                    {t(`vehicleTypes.${vehicle.tipo}`)}
                  </td>
                  <td className='px-6 py-4 whitespace-nowrap text-sm text-gray-900'>
                    {vehicle.capacidad_carga.toLocaleString()} kg
                  </td>
                  <td className='px-6 py-4 whitespace-nowrap'>
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(vehicle.estado)}`}
                    >
                      {t(`vehicleStatuses.${vehicle.estado}`)}
                    </span>
                  </td>
                  <td className='px-6 py-4 whitespace-nowrap text-sm text-gray-900'>
                    {vehicle.kilometraje.toLocaleString()} km
                  </td>
                  <td className='px-6 py-4 whitespace-nowrap text-sm font-medium'>
                    <button className='text-blue-600 hover:text-blue-900 mr-4'>
                      {t('common.edit')}
                    </button>
                    <button className='text-red-600 hover:text-red-900'>
                      {t('common.delete')}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className='bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6'>
            <div className='flex-1 flex justify-between sm:hidden'>
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className='relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed'
              >
                {t('common.previous')}
              </button>
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className='ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed'
              >
                {t('common.next')}
              </button>
            </div>
            <div className='hidden sm:flex-1 sm:flex sm:items-center sm:justify-between'>
              <div>
                <p className='text-sm text-gray-700'>
                  {t('common.page')}{' '}
                  <span className='font-medium'>{currentPage}</span>{' '}
                  {t('common.of')}{' '}
                  <span className='font-medium'>{totalPages}</span>
                </p>
              </div>
              <div>
                <nav className='relative z-0 inline-flex rounded-md shadow-sm -space-x-px'>
                  <button
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                    className='relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed'
                  >
                    {t('common.previous')}
                  </button>
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    const pageNum =
                      Math.max(1, Math.min(totalPages - 4, currentPage - 2)) +
                      i;
                    return (
                      <button
                        key={pageNum}
                        onClick={() => handlePageChange(pageNum)}
                        className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                          pageNum === currentPage
                            ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                            : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                  <button
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className='relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed'
                  >
                    {t('common.next')}
                  </button>
                </nav>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* No data message */}
      {filteredVehicles.length === 0 && (
        <div className='text-center py-12'>
          <p className='text-gray-500 text-lg'>{t('common.noData')}</p>
        </div>
      )}
    </div>
  );
}
