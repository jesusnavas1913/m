#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilidades de validación para el sistema ICFES.IA
"""

import re
from typing import Tuple, Optional

def validate_cedula(cedula: str) -> Tuple[bool, Optional[str]]:
    """
    Valida el formato de una cédula colombiana
    
    Args:
        cedula: String con la cédula a validar
    
    Returns:
        Tupla (es_valida, mensaje_error)
    """
    if not cedula:
        return False, "La cédula es requerida"
    
    if not cedula.isdigit():
        return False, "La cédula debe contener solo números"
    
    if len(cedula) < 6 or len(cedula) > 10:
        return False, "La cédula debe tener entre 6 y 10 dígitos"
    
    return True, None

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Valida el formato de un email
    
    Args:
        email: String con el email a validar
    
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not email:
        return False, "El email es requerido"
    
    # Patrón robusto para emails
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "El formato del email es inválido"
    
    if len(email) > 254:  # RFC 5321
        return False, "El email es demasiado largo"
    
    return True, None

def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Valida que una contraseña cumpla con los requisitos de seguridad
    
    Args:
        password: String con la contraseña a validar
    
    Returns:
        Tupla (es_valida, mensaje_error)
    """
    if not password:
        return False, "La contraseña es requerida"
    
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if len(password) > 128:
        return False, "La contraseña es demasiado larga (máximo 128 caracteres)"
    
    if not any(c.isupper() for c in password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    if not any(c.islower() for c in password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    if not any(c.isdigit() for c in password):
        return False, "La contraseña debe contener al menos un número"
    
    # Opcional: verificar caracteres especiales
    # if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
    #     return False, "La contraseña debe contener al menos un carácter especial"
    
    return True, None

def validate_nombre(nombre: str) -> Tuple[bool, Optional[str]]:
    """
    Valida el formato de un nombre
    
    Args:
        nombre: String con el nombre a validar
    
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not nombre:
        return False, "El nombre es requerido"
    
    nombre_limpio = nombre.strip()
    
    if len(nombre_limpio) < 3:
        return False, "El nombre debe tener al menos 3 caracteres"
    
    if len(nombre_limpio) > 100:
        return False, "El nombre es demasiado largo (máximo 100 caracteres)"
    
    # Verificar que contenga al menos algunas letras
    if not any(c.isalpha() for c in nombre_limpio):
        return False, "El nombre debe contener letras"
    
    return True, None

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Limpia y sanitiza un input de texto
    
    Args:
        text: Texto a sanitizar
        max_length: Longitud máxima permitida
    
    Returns:
        Texto sanitizado
    """
    if not text:
        return ""
    
    # Eliminar espacios al inicio y final
    sanitized = text.strip()
    
    # Limitar longitud
    sanitized = sanitized[:max_length]
    
    # Eliminar caracteres de control peligrosos (excepto saltos de línea y tabs)
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\n\t')
    
    return sanitized

def validate_user_registration(nombre: str, cedula: str, email: str, password: str) -> Tuple[bool, Optional[str]]:
    """
    Valida todos los campos de registro de usuario
    
    Args:
        nombre: Nombre del usuario
        cedula: Cédula del usuario
        email: Email del usuario
        password: Contraseña del usuario
    
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    # Validar nombre
    is_valid, error = validate_nombre(nombre)
    if not is_valid:
        return False, error
    
    # Validar cédula
    is_valid, error = validate_cedula(cedula)
    if not is_valid:
        return False, error
    
    # Validar email
    is_valid, error = validate_email(email)
    if not is_valid:
        return False, error
    
    # Validar contraseña
    is_valid, error = validate_password(password)
    if not is_valid:
        return False, error
    
    return True, None
