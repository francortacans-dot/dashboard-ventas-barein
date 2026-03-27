import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class AnalisadorVentas:
    def __init__(self, ruta_archivo):
        """Carga los datos de ventas"""
        self.df = pd.read_excel(ruta_archivo)
        self.df['Fecha'] = pd.to_datetime(self.df['MES/AÑO'], format='%m/%Y', errors='coerce')
        self.df['Cant'] = pd.to_numeric(self.df['Cant'], errors='coerce')
        self.df['Importe ML'] = pd.to_numeric(self.df['Importe ML'], errors='coerce')
        
    def calcular_kpis(self):
        """Calcula KPIs principales"""
        kpis = {
            'total_ventas': self.df['Importe ML'].sum(),
            'cantidad_total': self.df['Cant'].sum(),
            'numero_transacciones': len(self.df),
            'ticket_promedio': self.df['Importe ML'].sum() / len(self.df) if len(self.df) > 0 else 0,
            'cantidad_promedio': self.df['Cant'].mean(),
            'numero_vendedores': self.df['Vendedor'].nunique(),
            'numero_clientes': self.df['Cliente'].nunique(),
            'numero_productos': self.df['Codigo Producto'].nunique(),
        }
        return kpis
    
    def segmentacion_vendedores(self):
        """Segmenta ventas por vendedor"""
        seg_vendedores = self.df.groupby('Vendedor').agg({
            'Importe ML': 'sum',
            'Cant': 'sum',
            'Cliente': 'nunique'
        }).round(2).sort_values('Importe ML', ascending=False)
        seg_vendedores.columns = ['Venta Total', 'Cantidad Total', 'Clientes']
        return seg_vendedores
    
    def segmentacion_marcas(self):
        """Segmenta ventas por marca"""
        seg_marcas = self.df.groupby('Marca').agg({
            'Importe ML': 'sum',
            'Cant': 'sum'
        }).round(2).sort_values('Importe ML', ascending=False)
        seg_marcas.columns = ['Venta Total', 'Cantidad Total']
        return seg_marcas
    
    def segmentacion_clientes_top(self, top_n=10):
        """Top clientes por venta"""
        seg_clientes = self.df.groupby('Razón Social').agg({
            'Importe ML': 'sum',
            'Cant': 'sum'
        }).round(2).sort_values('Importe ML', ascending=False).head(top_n)
        seg_clientes.columns = ['Venta Total', 'Cantidad Total']
        return seg_clientes
    
    def detectar_anomalias(self, umbral_cantidad=30):
        """Detecta anomalías: ventas > umbral por vendedor"""
        anomalias = self.df[self.df['Cant'] > umbral_cantidad].copy()
        anomalias = anomalias[['Vendedor', 'Cliente', 'Marca', 'Descripción', 'Cant', 'Importe ML', 'MES/AÑO']].sort_values('Cant', ascending=False)
        return anomalias
    
    def tendencia_temporal(self):
        """Analiza tendencia de ventas en el tiempo"""
        tendencia = self.df.groupby('MES/AÑO').agg({
            'Importe ML': 'sum',
            'Cant': 'sum'
        }).round(2)
        tendencia.columns = ['Venta Total', 'Cantidad Total']
        return tendencia
    
    def analisis_actividad(self):
        """Segmenta por tipo de actividad"""
        seg_actividad = self.df.groupby('Actividad').agg({
            'Importe ML': 'sum',
            'Cant': 'sum',
            'Vendedor': 'nunique'
        }).round(2).sort_values('Importe ML', ascending=False)
        seg_actividad.columns = ['Venta Total', 'Cantidad Total', 'Vendedores']
        return seg_actividad
    
    def vendedor_mas_activo(self):
        """Identifica vendedor con más actividad"""
        vendedor_activo = self.df.groupby('Vendedor')['Importe ML'].sum().sort_values(ascending=False)
        return vendedor_activo
    
    def producto_mas_vendido(self):
        """Identifica producto más vendido"""
        producto_top = self.df.groupby('Descripción').agg({
            'Cant': 'sum',
            'Importe ML': 'sum'
        }).sort_values('Cant', ascending=False).head(10)
        producto_top.columns = ['Cantidad Vendida', 'Importe Total']
        return producto_top
    
    def generar_resumen_ejecutivo(self):
        """Genera un resumen textual para IA"""
        kpis = self.calcular_kpis()
        vendedores = self.segmentacion_vendedores()
        marcas = self.segmentacion_marcas()
        anomalias = self.detectar_anomalias()
        
        resumen = f"""
RESUMEN EJECUTIVO - ANÁLISIS DE VENTAS BAREIN GP

INDICADORES CLAVE:
- Venta Total: ${kpis['total_ventas']:,.2f}
- Cantidad Total: {kpis['cantidad_total']:.0f} unidades
- Transacciones: {kpis['numero_transacciones']}
- Ticket Promedio: ${kpis['ticket_promedio']:,.2f}
- Vendedores Activos: {kpis['numero_vendedores']}
- Clientes Únicos: {kpis['numero_clientes']}

TOP 5 VENDEDORES:
{vendedores.head(5).to_string()}

TOP 5 MARCAS:
{marcas.head(5).to_string()}

ANOMALÍAS DETECTADAS (Ventas > 30 unidades):
{anomalias.to_string() if len(anomalias) > 0 else 'Ninguna anomalía detectada'}

Análisis generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return resumen
