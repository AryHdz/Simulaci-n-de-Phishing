# 🔐 Simulación de Análisis de Phishing – SOC Nivel 2

[![Status](https://img.shields.io/badge/status-completado-brightgreen)]()
[![SOC](https://img.shields.io/badge/SOC-Nivel%202-blue)]()
[![License](https://img.shields.io/badge/license-educativo-lightgrey)]()

## 📌 Descripción General

Este proyecto consiste en una **simulación práctica de análisis de phishing**, desarrollada a través de una página web de una empresa ficticia llamada **Nexora**.

El enfoque principal está basado en la ejecución simulada de un **analista SOC de segundo nivel**, donde se recrea el proceso completo de validación y análisis de un correo sospechoso utilizando una herramienta de análisis simulada.

> ⚠️ **Nota importante:** Este proyecto es **completamente educativo** y se ejecuta en entorno local. No se almacena ni procesa información real.

---

## 🎯 Objetivo del Proyecto

Recrear un escenario realista donde un **analista SOC Nivel 2**:

| Fase | Acción |
|------|--------|
| 1️⃣ | Recibe un posible incidente (correo sospechoso) |
| 2️⃣ | Realiza un análisis más profundo del mensaje |
| 3️⃣ | Determina si el correo corresponde a un intento de phishing |
| 4️⃣ | Genera una respuesta basada en el análisis técnico |

---

## 🧠 Contexto SOC Nivel 2

A diferencia del **Nivel 1** (monitoreo y triage básico), este proyecto simula tareas de **Nivel 2** como:

| Área | Descripción |
|------|-------------|
| 🔍 **Investigación** | Análisis profundo de eventos sospechosos |
| 📊 **Análisis de indicadores** | Identificación de IoC (Indicadores de Compromiso) |
| 🛠 **Uso de herramientas** | Empleo de sistemas de análisis (simulado) |
| ✅ **Validación** | Confirmación o descarte de incidentes de seguridad |

---

## 🖥️ Vistas del Proyecto

### 1. 🔐 Login del Analista SOC

![Login del Analista SOC](./images/login.png)

*Pantalla de acceso al laboratorio SOC. El analista debe ingresar sus credenciales para iniciar la sesión de trabajo.*

**Usuarios de prueba disponibles:**
- `ana.garcia`
- `carlos.ruiz`
- `admin`

---

### 2. 📧 Correo Sospechoso – Bandeja de Entrada

![Correo de Phishing](./images/correo-phishing.png)

*El analista recibe un correo que simula una alerta de seguridad bancaria. A simple vista ya se observan indicadores iniciales de posible phishing.*

**Detalles del correo:**
| Campo | Valor |
|-------|-------|
| **De** | Soporte Bancario Nexora <soporte@nexora-seguro.net> |
| **Para** | finanzas@nexora.com |
| **Asunto** | ALERTA DE SEGURIDAD: Cuenta bloqueada |
| **Enlace sospechoso** | http://nexora-verificacion.xyz/secure/login |

---

### 3. ✅ Resultado del Análisis

![Resultado del Análisis](./images/resultado-analisis.png)

*Tras ejecutar la herramienta de análisis, se obtiene una puntuación de riesgo de **99/100** y se confirma que se trata de un intento de phishing.*

---

## 🔍 Indicadores de Phishing Identificados

| # | Indicador | Descripción |
|---|-----------|-------------|
| 1 | **Dominio falso** | `soporte@nexora-seguro.net` vs el real `nexora.com` |
| 2 | **URL maliciosa** | `nexora-verificacion.xyz` ≠ `nexora.com` |
| 3 | **Urgencia artificial** | "en las próximas 2 HORAS" |
| 4 | **Amenaza** | "bloqueada permanentemente" |
| 5 | **Solicitud de credenciales** | Pide contraseñas por enlace externo |
| 6 | **Typosquatting** | `nexora-seguro.net` imita a `nexora.com` |
| 7 | **Incongruencia geográfica** | Teléfono español (+34) para empresa mexicana |

---

## 🛠 Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| HTML5 / CSS3 | Interfaz web del simulador |
| JavaScript | Lógica de análisis simulada |
| Git & GitHub | Control de versiones y despliegue |

---

## 📁 Estructura del Proyecto
