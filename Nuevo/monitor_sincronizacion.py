import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CONFIGURACIÓN
CARPETA_LOCAL = r"C:\Nuevo"
CARPETA_ONEDRIVE = r"C:\Users\Neumaticos Barein GP\OneDrive\Documentos\Nuevo"
ARCHIVO_MONITOREO = "Venta_consolidado.xlsx"

class MonitorCambios(FileSystemEventHandler):
    """Monitorea cambios en archivos y sincroniza a OneDrive"""
    
    def on_modified(self, event):
        """Se ejecuta cuando un archivo es modificado"""
        if event.is_directory:
            return
        
        # Solo monitoreamos el archivo que nos interesa
        if ARCHIVO_MONITOREO in event.src_path:
            logger.info(f"✅ Cambio detectado: {event.src_path}")
            self.sincronizar_a_onedrive()
    
    def on_created(self, event):
        """Se ejecuta cuando se crea un archivo nuevo"""
        if event.is_directory:
            return
        
        if ARCHIVO_MONITOREO in event.src_path:
            logger.info(f"📄 Archivo nuevo detectado: {event.src_path}")
            time.sleep(2)  # Espera a que se termine de escribir
            self.sincronizar_a_onedrive()
    
    def sincronizar_a_onedrive(self):
        """Copia el archivo a OneDrive"""
        try:
            ruta_origen = os.path.join(CARPETA_LOCAL, ARCHIVO_MONITOREO)
            ruta_destino = os.path.join(CARPETA_ONEDRIVE, ARCHIVO_MONITOREO)
            
            # Verificar que origen existe
            if not os.path.exists(ruta_origen):
                logger.error(f"❌ Archivo origen no encontrado: {ruta_origen}")
                return
            
            # Crear carpeta OneDrive si no existe
            if not os.path.exists(CARPETA_ONEDRIVE):
                os.makedirs(CARPETA_ONEDRIVE)
                logger.info(f"📁 Carpeta creada: {CARPETA_ONEDRIVE}")
            
            # Copiar archivo
            shutil.copy2(ruta_origen, ruta_destino)
            logger.info(f"🔄 ✅ Sincronizado a OneDrive: {ruta_destino}")
            
        except PermissionError:
            logger.error("❌ Error de permisos. Intenta de nuevo en unos segundos.")
        except Exception as e:
            logger.error(f"❌ Error al sincronizar: {str(e)}")

def iniciar_monitor():
    """Inicia el monitor de cambios"""
    logger.info("=" * 60)
    logger.info("🚀 MONITOR DE SINCRONIZACIÓN INICIADO")
    logger.info("=" * 60)
    logger.info(f"📂 Monitoreando carpeta: {CARPETA_LOCAL}")
    logger.info(f"📂 Sincronizando a: {CARPETA_ONEDRIVE}")
    logger.info(f"📄 Archivo: {ARCHIVO_MONITOREO}")
    logger.info("=" * 60)
    logger.info("Esperando cambios... (Ctrl+C para detener)")
    logger.info("=" * 60)
    
    # Crear observador
    event_handler = MonitorCambios()
    observer = Observer()
    observer.schedule(event_handler, CARPETA_LOCAL, recursive=False)
    
    try:
        observer.start()
        # Mantener el script corriendo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n❌ Monitor detenido por el usuario")
        observer.stop()
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    # Verificar que existen las carpetas
    if not os.path.exists(CARPETA_LOCAL):
        logger.error(f"❌ Carpeta local no existe: {CARPETA_LOCAL}")
        exit(1)
    
    iniciar_monitor()
