import { NextResponse } from 'next/server';

// Mock vehicle data
const mockVehicles = [
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

export async function GET() {
  try {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    return NextResponse.json(mockVehicles);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch vehicles' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();

    // Simulate creating a new vehicle
    const newVehicle = {
      id: Date.now().toString(),
      ...body,
      fecha_matriculacion: new Date().toISOString().split('T')[0],
    };

    // In a real app, this would be saved to a database
    mockVehicles.push(newVehicle);

    return NextResponse.json(newVehicle, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create vehicle' },
      { status: 500 }
    );
  }
}
