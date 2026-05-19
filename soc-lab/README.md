# 🛡️ Nexora SOC Lab — Laboratorio de Ciberseguridad

Simulación educativa de un **SOC (Security Operations Center)** de Blue Team.  
El empleado analiza correos en busca de phishing usando técnicas reales.

---

## 📁 Estructura del proyecto

```
soc-lab/
├── app.py                  # Backend Flask (API + rutas)
├── requirements.txt        # Dependencias Python
├── templates/
│   ├── login.html          # Página de login
│   └── panel.html          # Panel del analista SOC
└── README.md
```

---

## 🗃️ Base de datos simulada

La "base de datos" es un diccionario Python en `app.py` (líneas ~20-50).  
No necesita ningún motor externo para el laboratorio.

### Usuarios disponibles

| Usuario       | Contraseña     | Rol              |
|---------------|----------------|------------------|
| ana.garcia    | Nexora2026!    | Analista SOC     |
| carlos.ruiz   | SecurePass#1   | Ingeniero Blue Team |
| admin         | Admin123!      | SOC Manager      |

### ¿Cómo se valida el login?

```
Contraseña ingresada → SHA-256 hash → Comparar con hash en USERS_DB
```

Las contraseñas **nunca se almacenan en texto plano**.

### ¿Cómo agregar un usuario?

En `app.py`, en `USERS_DB`, añade:

```python
import hashlib

"nuevo.usuario": {
    "password_hash": hashlib.sha256("MiPassword123".encode()).hexdigest(),
    "nombre": "Nombre Completo",
    "rol": "Analista Jr",
    "departamento": "SOC",
    "avatar": "NC"
}
```

---

## 🚀 Cómo ejecutar en local

### Requisitos previos

- Python 3.8 o superior
- pip

### Pasos

```bash
# 1. Entrar al directorio del proyecto
cd soc-lab

# 2. (Opcional) Crear entorno virtual
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el servidor
python app.py
```
### Inicio rapido en Windows

Tambien puedes iniciar la simulacion con doble clic en:

```bash
iniciar-simulacion.bat
```

La aplicacion se ejecuta solo en tu computadora, en `127.0.0.1`. No publica nada en internet.

---

## 🔌 Conexión con base de datos real (opcional)

Para conectar con SQLite (sin instalar nada extra):

```python
import sqlite3

def init_db():
    conn = sqlite3.connect('soc_lab.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT,
            nombre TEXT,
            rol TEXT
        )
    ''')
    conn.commit()
    conn.close()
```

Para conectar con PostgreSQL:
```bash
pip install psycopg2-binary
```

```python
import psycopg2
conn = psycopg2.connect(
    host="localhost", database="soc_lab",
    user="postgres", password="tu_password"
)
```

---

## 🎯 Objetivo educativo

Este laboratorio enseña a identificar:

1. **Typosquatting**: dominios falsos que imitan al original
2. **Urgencia artificial**: "2 horas o tu cuenta será bloqueada"
3. **URLs maliciosas**: dominio diferente al corporativo
4. **Suplantación de identidad**: nombre real, email falso
5. **Ingeniería social**: amenazas para presionar a la víctima

---

## ⚖️ Uso

Este proyecto es exclusivamente para **fines educativos** en entornos de laboratorio controlados.
