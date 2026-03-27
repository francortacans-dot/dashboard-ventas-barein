import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from analisis import AnalisadorVentas
from anthropic import Anthropic
import os
from dotenv import load_dotenv
import time
from io import BytesIO
import requests
 
# Cargar variables de entorno
load_dotenv()
 
# Configurar página
st.set_page_config(page_title="Dashboard Ventas Barein GP", layout="wide", initial_sidebar_state="expanded")
 
# Título y descripción
st.title("📊 Dashboard de Análisis de Ventas - Barein GP")
st.markdown("Análisis automático de KPIs, segmentación y anomalías con insights de IA")
 
# URL del archivo en GitHub (raw)
GITHUB_REPO = "francortacans-dot/dashboard-ventas-barein"
GITHUB_FILE = "Venta_consolidado.xlsx"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{GITHUB_FILE}"
 
# Sidebar
st.sidebar.title("⚙️ Configuración")
 
# Botón de recarga
col1, col2, col3 = st.sidebar.columns([2, 1, 1])
with col1:
    if st.button("🔄 Recargar Datos", use_container_width=True):
        st.rerun()
 
with col2:
    st.write("")
 
with col3:
    st.caption(f"⏰ {time.strftime('%H:%M')}")
 
# Mostrar información
st.sidebar.info(f"📁 Fuente: GitHub (Raw)")
 
# Cargar datos desde GitHub
@st.cache_data
def cargar_archivo_github():
    try:
        response = requests.get(GITHUB_RAW_URL)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            return None
    except Exception as e:
        st.error(f"Error al descargar: {str(e)}")
        return None
 
# Cargar análisis
try:
    # Descargar el archivo de GitHub
    st.info("📥 Cargando datos desde GitHub...")
    archivo_bytes = cargar_archivo_github()
    
    if archivo_bytes is None:
        st.error("No se pudo descargar el archivo de GitHub")
        st.stop()
    
    # Crear analizador con el archivo descargado
    analizador = AnalisadorVentas.__new__(AnalisadorVentas)
    analizador.df = pd.read_excel(archivo_bytes)
    analizador.df['Fecha'] = pd.to_datetime(analizador.df['MES/AÑO'], format='%m/%Y', errors='coerce')
    analizador.df['Cant'] = pd.to_numeric(analizador.df['Cant'], errors='coerce')
    analizador.df['Importe ML'] = pd.to_numeric(analizador.df['Importe ML'], errors='coerce')
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 KPIs", "👥 Segmentación", "⚠️ Anomalías", "🤖 Análisis IA", "📊 Visualizaciones"])
    
    # TAB 1: KPIs
    with tab1:
        st.subheader("Indicadores Clave de Desempeño")
        kpis = analizador.calcular_kpis()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Venta Total", f"${kpis['total_ventas']:,.0f}")
        col2.metric("📦 Cantidad Total", f"{kpis['cantidad_total']:,.0f} unidades")
        col3.metric("📊 Transacciones", f"{kpis['numero_transacciones']:,}")
        col4.metric("🎯 Ticket Promedio", f"${kpis['ticket_promedio']:,.0f}")
        
        st.divider()
        
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("👨‍💼 Vendedores Activos", f"{kpis['numero_vendedores']}")
        col6.metric("🏢 Clientes Únicos", f"{kpis['numero_clientes']}")
        col7.metric("📦 Productos", f"{kpis['numero_productos']}")
        col8.metric("📈 Promedio por Unidad", f"{kpis['cantidad_promedio']:.2f}")
    
    # TAB 2: Segmentación
    with tab2:
        st.subheader("Análisis de Segmentación")
        
        seg_tab1, seg_tab2, seg_tab3, seg_tab4 = st.tabs(["Vendedores", "Marcas", "Top Clientes", "Actividades"])
        
        with seg_tab1:
            st.write("**Venta por Vendedor**")
            seg_vendedores = analizador.segmentacion_vendedores()
            st.dataframe(seg_vendedores, use_container_width=True)
        
        with seg_tab2:
            st.write("**Venta por Marca**")
            seg_marcas = analizador.segmentacion_marcas()
            st.dataframe(seg_marcas, use_container_width=True)
        
        with seg_tab3:
            st.write("**Top 10 Clientes**")
            seg_clientes = analizador.segmentacion_clientes_top(10)
            st.dataframe(seg_clientes, use_container_width=True)
        
        with seg_tab4:
            st.write("**Venta por Actividad**")
            seg_actividad = analizador.analisis_actividad()
            st.dataframe(seg_actividad, use_container_width=True)
    
    # TAB 3: Anomalías
    with tab3:
        st.subheader("Detección de Anomalías")
        st.info("Se consideran anomalías ventas > 30 unidades por vendedor")
        
        anomalias = analizador.detectar_anomalias(umbral_cantidad=30)
        
        if len(anomalias) > 0:
            st.warning(f"⚠️ Se detectaron {len(anomalias)} anomalías")
            st.dataframe(anomalias, use_container_width=True)
        else:
            st.success("✅ No se detectaron anomalías")
    
    # TAB 4: Análisis con IA
    with tab4:
        st.subheader("🤖 Análisis Inteligente con Claude")
        
        # Verificar API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            st.error("❌ API key de Anthropic no configurada")
            st.info("Este dashboard necesita una API key de Claude para funcionar completamente")
        else:
            st.success("✅ Conectado a Claude")
            
            # Generar resumen para IA
            resumen_datos = analizador.generar_resumen_ejecutivo()
            
            # Inicializar cliente Anthropic
            client = Anthropic()
            
            # Caja de chat
            st.subheader("Chat de Análisis")
            
            # Mensaje predeterminado
            mensaje_default = f"Analiza los siguientes datos de ventas y proporciona insights clave, recomendaciones y análisis de anomalías:\n\n{resumen_datos}"
            
            if st.button("📋 Generar Análisis Automático"):
                with st.spinner("Claude está analizando..."):
                    try:
                        response = client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1500,
                            messages=[
                                {"role": "user", "content": mensaje_default}
                            ]
                        )
                        
                        insight = response.content[0].text
                        st.markdown("### 📊 Insights Generados por Claude:")
                        st.markdown(insight)
                        
                        # Permitir copiar
                        st.code(insight, language="markdown")
                    except Exception as e:
                        st.error(f"Error al conectar con Claude: {str(e)}")
    
    # TAB 5: Visualizaciones
    with tab5:
        st.subheader("📊 Gráficos y Visualizaciones")
        
        col1, col2 = st.columns(2)
        
        # Gráfico 1: Top Vendedores
        with col1:
            seg_vendedores = analizador.segmentacion_vendedores().head(10)
            fig_vendedores = go.Figure(data=[
                go.Bar(x=seg_vendedores.index, y=seg_vendedores['Venta Total'], name='Venta Total')
            ])
            fig_vendedores.update_layout(title="Top 10 Vendedores", xaxis_title="Vendedor", yaxis_title="Venta ($)")
            st.plotly_chart(fig_vendedores, use_container_width=True)
        
        # Gráfico 2: Top Marcas
        with col2:
            seg_marcas = analizador.segmentacion_marcas().head(10)
            fig_marcas = go.Figure(data=[
                go.Bar(x=seg_marcas.index, y=seg_marcas['Venta Total'], name='Venta Total', marker_color='lightblue')
            ])
            fig_marcas.update_layout(title="Top 10 Marcas", xaxis_title="Marca", yaxis_title="Venta ($)")
            st.plotly_chart(fig_marcas, use_container_width=True)
        
        # Gráfico 3: Tendencia Temporal
        st.subheader("Tendencia de Ventas en el Tiempo")
        tendencia = analizador.tendencia_temporal()
        fig_tendencia = go.Figure()
        fig_tendencia.add_trace(go.Scatter(x=tendencia.index, y=tendencia['Venta Total'], mode='lines+markers', name='Venta Total'))
        fig_tendencia.update_layout(title="Evolución de Ventas", xaxis_title="Período", yaxis_title="Venta ($)")
        st.plotly_chart(fig_tendencia, use_container_width=True)
        
        # Gráfico 4: Distribución por Actividad
        col3, col4 = st.columns(2)
        with col3:
            seg_actividad = analizador.analisis_actividad()
            fig_actividad = px.pie(
                values=seg_actividad['Venta Total'],
                names=seg_actividad.index,
                title="Distribución de Ventas por Actividad"
            )
            st.plotly_chart(fig_actividad, use_container_width=True)
        
        # Gráfico 5: Productos más vendidos
        with col4:
            productos_top = analizador.producto_mas_vendido()
            fig_productos = go.Figure(data=[
                go.Bar(x=productos_top['Cantidad Vendida'], y=productos_top.index, orientation='h', marker_color='orange')
            ])
            fig_productos.update_layout(title="Top 10 Productos (Cantidad)", xaxis_title="Cantidad Vendida")
            st.plotly_chart(fig_productos, use_container_width=True)
 
except Exception as e:
    st.error(f"Error al procesar el archivo: {str(e)}")
    st.info("Verifica que el archivo esté en GitHub y que tengas las librerías necesarias instaladas.")
 
