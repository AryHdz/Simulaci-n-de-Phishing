"""
Nexora SOC Lab - Backend Flask
Simulación educativa de ciberseguridad (Blue Team)
"""

from flask import Flask, request, jsonify, session, send_from_directory, redirect
import json
import os
import hashlib
import webbrowser
from datetime import datetime, timedelta
from functools import wraps
from threading import Timer

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'nexora-soc-lab-2026-secret'  # En producción: usar variable de entorno
app.permanent_session_lifetime = timedelta(hours=2)

# ─────────────────────────────────────────────
# BASE DE DATOS SIMULADA (JSON en memoria)
# ─────────────────────────────────────────────
# Contraseñas hasheadas con SHA-256
# Para generar: hashlib.sha256("password".encode()).hexdigest()
USERS_DB = {
    "ana.garcia": {
        "password_hash": hashlib.sha256("Nexora2026!".encode()).hexdigest(),
        "nombre": "Ana García",
        "rol": "Analista SOC",
        "departamento": "Seguridad",
        "avatar": "AG"
    },
    "carlos.ruiz": {
        "password_hash": hashlib.sha256("SecurePass#1".encode()).hexdigest(),
        "nombre": "Carlos Ruiz",
        "rol": "Ingeniero Blue Team",
        "departamento": "Ciberseguridad",
        "avatar": "CR"
    },
    "admin": {
        "password_hash": hashlib.sha256("Admin123!".encode()).hexdigest(),
        "nombre": "Administrador",
        "rol": "SOC Manager",
        "departamento": "Dirección",
        "avatar": "AD"
    }
}

# Mensaje de phishing del escenario (el de la imagen)
INBOX = [
    {
        "id": "msg-001",
        "de_nombre": "Soporte Bancario Nexora",
        "de_email": "soporte@nexora-seguro.net",
        "para": "finanzas@nexora.com",
        "asunto": "⚠️ ALERTA DE SEGURIDAD: Cuenta bloqueada por actividades sospechosas",
        "fecha": "2026-05-02 05:58",
        "cuerpo": (
            "Estimado equipo de finanzas,\n\n"
            "Hemos detectado 3 intentos de acceso no autorizados a su cuenta bancaria corporativa. "
            "Por seguridad, la cuenta ha sido SUSPENDIDA temporalmente.\n\n"
            "PARA REACTIVAR SU CUENTA EN LAS PRÓXIMAS 2 HORAS:\n"
            "1. Haga clic en el siguiente enlace: http://nexora-verificacion.xyz/secure/login\n"
            "2. Confirme sus credenciales de acceso\n"
            "3. Valide su token de seguridad\n\n"
            "Si no completa este proceso en 2 horas, su cuenta quedará permanentemente bloqueada "
            "y se reportará a la unidad de fraudes financieros.\n\n"
            "Atentamente,\nSoporte Bancario Nexora\n+34 987 654 321\nwww.nexora.com"
        ),
        "url_sospechosa": "http://nexora-verificacion.xyz/secure/login",
        "es_phishing": True,
        "indicadores": [
            "Dominio del remitente no coincide: soporte@nexora-seguro.net (dominio falso, el real es nexora.com)",
            "URL sospechosa con dominio diferente: nexora-verificacion.xyz ≠ nexora.com",
            "Urgencia artificial: 'en las próximas 2 HORAS'",
            "Amenaza de consecuencias graves: 'bloqueada permanentemente'",
            "Solicita credenciales a través de un enlace externo",
            "Typosquatting: 'nexora-seguro.net' en lugar de 'nexora.com'",
            "Número de teléfono español (+34) incongruente con empresa mexicana"
        ]
    }
]

# Registro de análisis enviados
ANALYSIS_LOG = []

# ─────────────────────────────────────────────
# DECORADOR DE AUTENTICACIÓN
# ─────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'No autenticado', 'redirect': '/'}), 401
        return f(*args, **kwargs)
    return decorated

# ─────────────────────────────────────────────
# RUTAS ESTÁTICAS
# ─────────────────────────────────────────────
@app.route('/')
def index():
    session.clear()
    return send_from_directory('templates', 'login.html')

@app.route('/panel')
def panel():
    if 'user' not in session:
        return redirect('/')
    return send_from_directory('templates', 'panel.html')

# ─────────────────────────────────────────────
# API: AUTENTICACIÓN
# ─────────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def api_login():
    session.clear()
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'mensaje': 'Usuario y contraseña son requeridos'}), 400

    user = USERS_DB.get(username)
    if not user:
        return jsonify({'success': False, 'mensaje': 'Credenciales incorrectas'}), 401

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user['password_hash'] != password_hash:
        return jsonify({'success': False, 'mensaje': 'Credenciales incorrectas'}), 401

    # Crear sesión
    session.permanent = True
    session['user'] = {
        'username': username,
        'nombre': user['nombre'],
        'rol': user['rol'],
        'departamento': user['departamento'],
        'avatar': user['avatar'],
        'login_time': datetime.now().isoformat()
    }

    return jsonify({
        'success': True,
        'mensaje': f'Bienvenido, {user["nombre"]}',
        'usuario': {
            'nombre': user['nombre'],
            'rol': user['rol'],
            'departamento': user['departamento'],
            'avatar': user['avatar']
        }
    })

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/session', methods=['GET'])
def api_session():
    if 'user' in session:
        return jsonify({'autenticado': True, 'usuario': session['user']})
    return jsonify({'autenticado': False})

# ─────────────────────────────────────────────
# API: BANDEJA DE ENTRADA
# ─────────────────────────────────────────────
@app.route('/api/inbox', methods=['GET'])
@login_required
def api_inbox():
    # Retornar mensajes sin revelar si son phishing (eso lo decide el analista)
    mensajes_seguros = []
    for msg in INBOX:
        mensajes_seguros.append({
            'id': msg['id'],
            'de_nombre': msg['de_nombre'],
            'de_email': msg['de_email'],
            'para': msg['para'],
            'asunto': msg['asunto'],
            'fecha': msg['fecha'],
            'cuerpo': msg['cuerpo'],
            'url_sospechosa': msg['url_sospechosa']
        })
    return jsonify({'mensajes': mensajes_seguros})

# ─────────────────────────────────────────────
# API: ENVIAR ANÁLISIS
# ─────────────────────────────────────────────
@app.route('/api/analizar', methods=['POST'])
@login_required
def api_analizar():
    data = request.get_json()
    msg_id = data.get('mensaje_id')
    es_phishing_usuario = data.get('es_phishing')
    indicadores_marcados = data.get('indicadores_marcados', [])
    justificacion = data.get('justificacion', '')

    # Buscar mensaje original
    mensaje = next((m for m in INBOX if m['id'] == msg_id), None)
    if not mensaje:
        return jsonify({'error': 'Mensaje no encontrado'}), 404

    # Evaluar respuesta
    correcto = (es_phishing_usuario == mensaje['es_phishing'])
    indicadores_correctos = [i for i in indicadores_marcados if i in mensaje['indicadores']]
    score = 0

    if correcto:
        score += 50
    score += len(indicadores_correctos) * 7  # Hasta 49 pts por indicadores
    score = min(score, 100)

    # Registrar análisis
    registro = {
        'analista': session['user']['nombre'],
        'mensaje_id': msg_id,
        'timestamp': datetime.now().isoformat(),
        'respuesta_usuario': es_phishing_usuario,
        'respuesta_correcta': mensaje['es_phishing'],
        'correcto': correcto,
        'indicadores_marcados': indicadores_marcados,
        'indicadores_correctos': indicadores_correctos,
        'justificacion': justificacion,
        'score': score
    }
    ANALYSIS_LOG.append(registro)

    return jsonify({
        'correcto': correcto,
        'score': score,
        'es_phishing_real': mensaje['es_phishing'],
        'indicadores_reales': mensaje['indicadores'],
        'indicadores_correctos': indicadores_correctos,
        'mensaje': '✅ ¡Análisis correcto!' if correcto else '❌ Clasificación incorrecta. Revisa los indicadores.',
        'explicacion': (
            'Este es un correo de PHISHING. El atacante suplanta a Nexora usando un dominio falso '
            '(nexora-seguro.net) y crea urgencia artificial para que la víctima haga clic en un '
            'enlace malicioso (nexora-verificacion.xyz) y entregue sus credenciales.'
            if mensaje['es_phishing'] else 'Este mensaje es legítimo.'
        )
    })

@app.route('/api/indicadores/<msg_id>', methods=['GET'])
@login_required
def api_indicadores(msg_id):
    """Devuelve la lista de posibles indicadores para el ejercicio (mezcla con falsos)"""
    mensaje = next((m for m in INBOX if m['id'] == msg_id), None)
    if not mensaje:
        return jsonify({'error': 'Mensaje no encontrado'}), 404

    # Indicadores reales + algunos falsos (para el ejercicio)
    todos = mensaje['indicadores'] + [
        "El mensaje tiene formato HTML",
        "El mensaje fue enviado en horario laboral",
        "El remitente usa un nombre corporativo"
    ]
    import random
    random.shuffle(todos)
    return jsonify({'indicadores': todos})

if __name__ == '__main__':
    print("\n🛡️  Nexora SOC Lab iniciando...")
    url = "http://127.0.0.1:5000"
    print(f"   URL local: {url}")
    print("\n   Usuarios disponibles:")
    print("   ├── ana.garcia    / Nexora2026!")
    print("   ├── carlos.ruiz   / SecurePass#1")
    print("   └── admin         / Admin123!")
    print("\n   Presiona Ctrl+C para detener\n")
    Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(host='127.0.0.1', debug=False, port=5000)
