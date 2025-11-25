#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar la conexión con Supabase
"""

import os
from dotenv import load_dotenv

print("\n" + "="*70)
print("  DIAGNÓSTICO DE CONEXIÓN - ICFES.IA")
print("="*70 + "\n")

# 1. Verificar variables de entorno
print("1️⃣  Verificando variables de entorno...")
load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if supabase_url:
    print(f"   ✅ SUPABASE_URL: {supabase_url[:30]}...")
else:
    print("   ❌ SUPABASE_URL: NO CONFIGURADA")

if supabase_key:
    print(f"   ✅ SUPABASE_KEY: {supabase_key[:20]}...")
else:
    print("   ❌ SUPABASE_KEY: NO CONFIGURADA")

if google_api_key:
    print(f"   ✅ GOOGLE_API_KEY: {google_api_key[:20]}...")
else:
    print("   ❌ GOOGLE_API_KEY: NO CONFIGURADA")

print()

# 2. Verificar conexión con Supabase
print("2️⃣  Probando conexión con Supabase...")
try:
    from supabase_client import get_supabase_client
    supabase = get_supabase_client()
    print("   ✅ Cliente de Supabase creado correctamente")
    
    # Intentar una consulta simple
    result = supabase.table('administradores').select('id').limit(1).execute()
    print("   ✅ Conexión con base de datos exitosa")
    print(f"   ✅ Tabla 'administradores' accesible")
    
except Exception as e:
    print(f"   ❌ Error de conexión: {str(e)}")
    print()
    print("   💡 Posibles causas:")
    print("      - SUPABASE_URL o SUPABASE_KEY incorrectas")
    print("      - Sin conexión a internet")
    print("      - Tabla 'administradores' no existe")

print()

# 3. Verificar administradores registrados
print("3️⃣  Verificando administradores registrados...")
try:
    result = supabase.table('administradores').select('*').execute()
    
    if result.data:
        print(f"   ✅ {len(result.data)} administrador(es) encontrado(s)")
        for i, admin in enumerate(result.data, 1):
            print(f"\n   Administrador #{i}:")
            print(f"      Nombre:     {admin.get('nombre', 'N/A')}")
            print(f"      Cédula:     {admin.get('cedula', 'N/A')}")
            print(f"      Contraseña: {admin.get('password', 'N/A')}")
            print(f"      Email:      {admin.get('email', 'N/A')}")
    else:
        print("   ⚠️  No hay administradores registrados")
        print("   💡 Ejecuta: python create_admin.py")
        
except Exception as e:
    print(f"   ❌ Error al obtener administradores: {str(e)}")

print()

# 4. Verificar servidor Flask
print("4️⃣  Verificando servidor Flask...")
try:
    import requests
    response = requests.get('http://127.0.0.1:5000/', timeout=2)
    if response.status_code == 200:
        print("   ✅ Servidor Flask corriendo en http://127.0.0.1:5000")
    else:
        print(f"   ⚠️  Servidor responde con código: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ❌ Servidor Flask NO está corriendo")
    print("   💡 Ejecuta: python app.py")
except Exception as e:
    print(f"   ⚠️  No se pudo verificar: {str(e)}")
    print("   💡 Instala requests: pip install requests")

print()
print("="*70)
print("\n✅ DIAGNÓSTICO COMPLETADO\n")

# Resumen de credenciales
if result.data and len(result.data) > 0:
    admin = result.data[0]
    print("🔑 CREDENCIALES PARA LOGIN:")
    print(f"   URL:        http://127.0.0.1:5000/admin/login")
    print(f"   Cédula:     {admin.get('cedula', 'N/A')}")
    print(f"   Contraseña: {admin.get('password', 'N/A')}")
    print()
