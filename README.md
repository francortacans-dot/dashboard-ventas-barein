# 📊 Dashboard de Análisis de Ventas - Barein GP

**Análisis automático de KPIs, segmentación y anomalías con IA integrada**

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Status](https://img.shields.io/badge/Status-Active-green)

---

## 🎯 Descripción

Dashboard interactivo desarrollado en **Python + Streamlit** que automatiza el análisis de datos de ventas de Barein GP. Integra **monitoreo en tiempo real**, **análisis con IA** (Claude) y **sincronización automática** con OneDrive.

### Características Principales

- ✅ **KPIs Automáticos**: Venta total, tickets promedio, segmentación por vendedor/marca
- ✅ **Detección de Anomalías**: Identifica ventas inusuales (>30 unidades)
- ✅ **Análisis con IA**: Claude analiza patrones y genera insights automáticos
- ✅ **Monitoreo en Tiempo Real**: Script que sincroniza cambios a OneDrive
- ✅ **Visualizaciones Interactivas**: Gráficos dinámicos con Plotly
- ✅ **Botón de Recarga**: Actualiza datos con un click

---

## 🏗️ Arquitectura

```
┌─────────────────────┐
│  Venta_consolidado  │ (Datos locales)
│    Archivo Excel    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│  monitor_sincronizacion.py  │ (Watchdog)
│   Monitorea cambios         │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│      OneDrive (Nube)        │
│  Sincronización automática   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   analisis.py               │
│  Clase AnalisadorVentas     │
│  - KPIs                     │
│  - Segmentación             │
│  - Anomalías                │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   app.py (Streamlit)        │
│  - Dashboard Interactivo    │
│  - Visualizaciones          │
│  - Integración Claude IA    │
└─────────────────────────────┘
```

---

## 🚀 Instalación

### Requisitos

- Python 3.11+
- Windows/Linux/Mac
- Git

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/francortacans-dot/dashboard-ventas-barein.git
cd dashboard-ventas-barein
```

2. **Instalar dependencias**
```bash
pip install pandas openpyxl streamlit plotly scikit-learn anthropic python-dotenv watchdog
```

3. **Configurar API Key**

Crea un archivo `.env` en la carpeta raíz:
```
ANTHROPIC_API_KEY=tu_api_key_aqui
```

4. **Ejecutar el monitor (opcional pero recomendado)**
```bash
python monitor_sincronizacion.py
```

O usa el archivo batch:
```bash
iniciar_monitor.bat
```

5. **Ejecutar el dashboard**
```bash
streamlit run app.py
```

El dashboard se abrirá en `http://localhost:8501`

---

## 📂 Estructura del Proyecto

```
dashboard-ventas-barein/
├── app.py                          # Dashboard Streamlit principal
├── analisis.py                     # Clase de análisis de datos
├── monitor_sincronizacion.py       # Script de monitoreo y sincronización
├── iniciar_monitor.bat             # Ejecutable para iniciar monitor
├── .env                            # Variables de entorno (no subir a GitHub)
├── .gitignore                      # Archivos a ignorar
├── requirements.txt                # Dependencias
├── Venta_consolidado.xlsx          # Datos de ejemplo
└── README.md                       # Este archivo
```

---

## 📊 Funcionalidades

### 1. **KPIs Dashboard**
Métricas principales:
- Venta total
- Cantidad total de unidades
- Número de transacciones
- Ticket promedio
- Vendedores activos
- Clientes únicos

### 2. **Segmentación**
Análisis por:
- Vendedor (ranking de ventas)
- Marca (productos más vendidos)
- Cliente (top 10 clientes)
- Actividad (mostrador, empresa, reventa)

### 3. **Detección de Anomalías**
Identifica operaciones inusuales:
- Ventas > 30 unidades por vendedor
- Patrones atípicos de compra
- Clientes con comportamiento anómalo

### 4. **Análisis con IA**
Claude genera:
- Insights sobre tendencias
- Recomendaciones estratégicas
- Análisis de anomalías detectadas
- Resumen ejecutivo automático

### 5. **Visualizaciones**
- Gráficos de barras (top vendedores/marcas)
- Series temporales (evolución de ventas)
- Gráficos de pastel (distribución por actividad)
- Tablas interactivas

---

## 🔧 Uso

### Interfaz Principal

```
1. Barra Lateral (Configuración)
   - Botón "🔄 Recargar Datos"
   - Hora de última actualización
   - Ruta del archivo

2. Pestañas Principales
   - 📈 KPIs: Indicadores clave
   - 👥 Segmentación: Análisis por categoría
   - ⚠️ Anomalías: Detección automática
   - 🤖 IA: Análisis con Claude
   - 📊 Visualizaciones: Gráficos interactivos
```

### Flujo de Trabajo

1. **Descarga datos** desde tu sistema
2. **Guardalos** en `C:\Nuevo\Venta_consolidado.xlsx`
3. **El monitor detecta cambios** automáticamente
4. **Clickea "Recargar"** en el dashboard
5. **Ve los insights** actualizados

---

## 🤖 Integración con IA

El dashboard utiliza **Claude 3.5 Sonnet** para:

- Análisis automático de datos
- Generación de insights
- Detección de patrones
- Recomendaciones basadas en datos

**Requiere API Key de Anthropic** (gratuita con créditos iniciales)

---

## 🔄 Automatización

### Monitor de Sincronización

Script que:
- ✅ Monitorea cambios en `Venta_consolidado.xlsx`
- ✅ Copia automáticamente a OneDrive
- ✅ Detecta nuevos archivos
- ✅ Sincroniza cada 2 segundos

**Ejecutar:**
```bash
python monitor_sincronizacion.py
```

O usar el batch automático:
```bash
iniciar_monitor.bat
```

---

## 📈 Ejemplos de Salida

### KPIs
```
💰 Venta Total: $2,500,000
📦 Cantidad Total: 45,433 unidades
📊 Transacciones: 2,891
🎯 Ticket Promedio: $864.82
👨‍💼 Vendedores Activos: 12
🏢 Clientes Únicos: 156
```

### Anomalías Detectadas
```
⚠️ Se detectaron 23 anomalías
- Venta de 45 unidades (Fernando, Mostrador)
- Venta de 38 unidades (Juan, Empresa)
```

### Insights de IA
```
Claude genera análisis como:
- "Las ventas en mostrador representan el 65% del total"
- "El vendedor Fernando tiene un 23% más de actividad que el promedio"
- "Detectamos 3 anomalías significativas en el período"
```

---

## 🛠️ Tech Stack

| Componente | Tecnología | Propósito |
|-----------|-----------|----------|
| **Backend** | Python 3.11+ | Lógica de análisis |
| **Frontend** | Streamlit | Dashboard interactivo |
| **Datos** | Pandas, Openpyxl | Procesamiento de Excel |
| **Visualización** | Plotly | Gráficos interactivos |
| **Monitoreo** | Watchdog | Detección de cambios |
| **IA** | Anthropic Claude | Análisis inteligente |
| **Almacenamiento** | OneDrive | Sincronización nube |

---

## 📚 Dependencias

```
pandas>=2.0.0
openpyxl>=3.10.0
streamlit>=1.28.0
plotly>=5.17.0
scikit-learn>=1.3.0
anthropic>=0.7.0
python-dotenv>=1.0.0
watchdog>=3.0.0
```

---

## 🔐 Seguridad

⚠️ **Importante:**
- Nunca subas tu `.env` a GitHub (está en `.gitignore`)
- Tu API Key de Claude se mantiene local
- Los datos de ventas no se comparten públicamente
- El proyecto es privado por defecto

---

## 📝 Logs y Debugging

El monitor genera logs automáticos:

```
2026-03-27 12:24:01 - INFO - ✅ Cambio detectado: Venta_consolidado.xlsx
2026-03-27 12:24:02 - INFO - 🔄 Sincronizado a OneDrive
```

---

## 🚀 Próximas Mejoras

- [ ] Exportar reportes a PDF
- [ ] Predicción de ventas con ML
- [ ] Alertas en tiempo real
- [ ] API REST para integración
- [ ] Dashboard en tiempo real con WebSockets
- [ ] Soporte multi-usuario

---

## 📞 Contacto

**Autor:** Francisco Pablo Cortacans  
**Email:** francortacans@gmail.com  

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Siéntete libre de usarlo y modificarlo.

---

## 🙏 Agradecimientos

- **Streamlit** por el framework de dashboards
- **Anthropic** por la API de Claude
- **Barein GP** por los datos

---

**Última actualización:** 27 de Marzo, 2026  
**Status:** ✅ Activo y en desarrollo
