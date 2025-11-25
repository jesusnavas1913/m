#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para crear administradores con contraseñas hasheadas usando bcrypt
Uso: python create_admin.py
"""

import bcrypt
from supabase_client import get_supabase_client
import os
from dotenv import load_dotenv

load_dotenv()

def create_admin():
    """Crea un nuevo administrador con contraseña hasheada"""
    print("=== CREAR NUEVO ADMINISTRADOR ===\n")
    
    nombre = input("Nombre del administrador: ").strip()
    cedula = input("Cédula (6-10 dígitos): ").strip()
    password = input("Contraseña (mínimo 8 caracteres, 1 mayúscula, 1 número): ").strip()
    
    # Validaciones
    if len(nombre) < 3:
        print("❌ El nombre debe tener al menos 3 caracteres")
        return
    
    if not cedula.isdigit() or len(cedula) < 6 or len(cedula) > 10:
        print("❌ La cédula debe tener entre 6 y 10 dígitos")
        return
    
    if len(password) < 8:
        print("❌ La contraseña debe tener al menos 8 caracteres")
        return
    
    if not any(c.isupper() for c in password):
        print("❌ La contraseña debe contener al menos una mayúscula")
        return
    
    if not any(c.isdigit() for c in password):
        print("❌ La contraseña debe contener al menos un número")
        return
    
    try:
        supabase = get_supabase_client()
        
        # Verificar si la cédula ya existe
        existing = supabase.table('administradores').select('cedula').eq('cedula', cedula).execute()
        if existing.data:
            print(f"❌ Ya existe un administrador con la cédula {cedula}")
            return
        
        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insertar en la base de datos
        new_admin = {
            'nombre': nombre,
            'cedula': cedula,
            'password': hashed_password
        }
        
        result = supabase.table('administradores').insert(new_admin).execute()
        
        if result.data:
            print(f"\n✅ Administrador creado exitosamente!")
            print(f"   Nombre: {nombre}")
            print(f"   Cédula: {cedula}")
            print(f"   Contraseña hasheada con bcrypt ✓")
        else:
            print("❌ Error al crear el administrador")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def update_admin_password():
    """Actualiza la contraseña de un administrador existente"""
    print("=== ACTUALIZAR CONTRASEÑA DE ADMINISTRADOR ===\n")
    
    cedula = input("Cédula del administrador: ").strip()
    new_password = input("Nueva contraseña (mínimo 8 caracteres, 1 mayúscula, 1 número): ").strip()
    
    # Validaciones
    if not cedula.isdigit() or len(cedula) < 6 or len(cedula) > 10:
        print("❌ La cédula debe tener entre 6 y 10 dígitos")
        return
    
    if len(new_password) < 8:
        print("❌ La contraseña debe tener al menos 8 caracteres")
        return
    
    if not any(c.isupper() for c in new_password):
        print("❌ La contraseña debe contener al menos una mayúscula")
        return
    
    if not any(c.isdigit() for c in new_password):
        print("❌ La contraseña debe contener al menos un número")
        return
    
    try:
        supabase = get_supabase_client()
        
        # Verificar si existe el administrador
        existing = supabase.table('administradores').select('*').eq('cedula', cedula).execute()
        if not existing.data:
            print(f"❌ No existe un administrador con la cédula {cedula}")
            return
        
        # Hashear la nueva contraseña
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Actualizar en la base de datos
        result = supabase.table('administradores').update({'password': hashed_password}).eq('cedula', cedula).execute()
        
        if result.data:
            print(f"\n✅ Contraseña actualizada exitosamente!")
            print(f"   Cédula: {cedula}")
            print(f"   Nueva contraseña hasheada con bcrypt ✓")
        else:
            print("❌ Error al actualizar la contraseña")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    print("\n╔════════════════════════════════════════╗")
    print("║  GESTIÓN DE ADMINISTRADORES - ICFES.IA ║")
    print("╚════════════════════════════════════════╝\n")
    
    print("Opciones:")
    print("1. Crear nuevo administrador")
    print("2. Actualizar contraseña de administrador")
    print("3. Salir\n")
    
    opcion = input("Selecciona una opción (1-3): ").strip()
    
    if opcion == '1':
        create_admin()
    elif opcion == '2':
        update_admin_password()
    elif opcion == '3':
        print("¡Hasta luego!")
    else:
        print("❌ Opción inválida")
