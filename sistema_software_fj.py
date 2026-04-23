import logging
from abc import ABC, abstractmethod

# 1. CONFIGURACIÓN DE LOGS (Requisito: Registro de eventos y errores)
logging.basicConfig(
    filename='registro_eventos.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. EXCEPCIONES PERSONALIZADAS (Requisito: Manejo avanzado de errores)
class SoftwareFJError(Exception):
    """Clase base para errores del sistema."""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Error cuando los datos de reserva son incorrectos."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Error cuando el servicio solicitado no puede procesarse."""
    pass

# 3. CLASE ABSTRACTA GENERAL (Requisito: Entidades generales)
class EntidadSistema(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass

# 4. CLASE CLIENTE (Requisito: Encapsulación y validaciones)
class Cliente(EntidadSistema):
    def __init__(self, id_cliente, nombre, email):
        self.__id = id_cliente  # Atributo privado
        self.__nombre = self._validar_nombre(nombre)
        self.email = email

    def _validar_nombre(self, nombre):
        if not nombre or len(nombre) < 3:
            error_msg = f"Nombre inválido: {nombre}"
            logging.error(error_msg)
            raise ValueError(error_msg)
        return nombre

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} (ID: {self.__id})"

# 5. CLASE ABSTRACTA SERVICIO (Requisito: Herencia y Polimorfismo)
class Servicio(EntidadSistema, ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Método para polimorfismo."""
        pass

# 6. SERVICIOS ESPECIALIZADOS (Un ejemplo para que tus compañeros sigan)
class AlquilerEquipos(Servicio):
    def calcular_costo(self, horas, descuento=0):
        """Uso de parámetros opcionales (Sobrecarga lógica)."""
        try:
            if horas <= 0:
                raise ReservaInvalidaError("Las horas deben ser mayores a cero.")
            total = (self.precio_base * horas) - descuento
            return max(total, 0)
        except Exception as e:
            logging.error(f"Error calculando costo en Alquiler: {e}")
            raise

    def mostrar_info(self):
        return f"Servicio: {self.nombre} | Tarifa: {self.precio_base}/hora"

# 7. CLASE RESERVA (Requisito: Integración y manejo de excepciones)
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def procesar_reserva(self):
        print(f"--- Procesando reserva para {self.cliente.mostrar_info()} ---")
        try:
            # Simulación de validación
            if self.duracion > 24:
                raise ReservaInvalidaError("No se permiten reservas mayores a 24 horas.")
            
            costo = self.servicio.calcular_costo(self.duracion)
            self.estado = "Confirmada"
            logging.info(f"Reserva exitosa: {self.cliente.mostrar_info()} - Costo: {costo}")
            print(f"Resultado: {self.estado}. Total a pagar: ${costo}")

        except ReservaInvalidaError as e:
            self.estado = "Fallida"
            logging.warning(f"Reserva fallida (Datos inválidos): {e}")
            print(f"Error controlado: {e}")
        
        except Exception as e:
            self.estado = "Error de Sistema"
            logging.error(f"Error inesperado: {e}", exc_info=True)
            print("Ocurrió un error grave, pero el sistema sigue funcionando.")
        
        finally:
            print(f"Finalizando proceso de reserva. Estado final: {self.estado}\n")

# --- SIMULACIÓN INICIAL (Para probar que todo funciona) ---
if __name__ == "__main__":
    try:
        # Caso 1: Todo correcto
        cliente1 = Cliente("001", "Paula Vanegas", "paula@ejemplo.com")
        laptop = AlquilerEquipos("Laptop Gamer", 50000)
        reserva1 = Reserva(cliente1, laptop, 3)
        reserva1.procesar_reserva()

        # Caso 2: Error provocado (Horas excesivas)
        reserva2 = Reserva(cliente1, laptop, 100)
        reserva2.procesar_reserva()

    except Exception as e:
        print(f"Error fuera del flujo: {e}")
        