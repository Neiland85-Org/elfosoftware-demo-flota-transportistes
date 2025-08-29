#!/bin/bash
echo "🚀 Iniciando servidor Next.js en background..."
cd apps/web
npm run dev > /dev/null 2>&1 &
echo "✅ Servidor iniciado. Verifica en http://localhost:3000"
echo "📊 PID del proceso: $!"
