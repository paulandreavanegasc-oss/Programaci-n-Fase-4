import logging
from abc import ABC, abstractmethod

# 1. CONFIGURACIÓN DE LOGS (Archivo de registro)
logging.basicConfig(
    filename='errores.log', 
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. EXCEPCIONES PERSONALIZADAS
class ErrorSoftwareFJ(Exception):
    """Base para errores del sistema"""
    pass

class DatoInvalidoError(ErrorSoftwareFJ):
    """Para datos de entrada incorrectos"""
    pass

class ReservaError(ErrorSoftwareFJ):
    """Para fallos en la lógica de reserva"""
    pass

# 3. CLASE ABSTRACTA BASE
class EntidadBase(ABC):
    @abstractmethod
    def obtener_detalles(self):
        pass

# 4. CLASE CLIENTE (Encapsulación)
class Cliente(EntidadBase):
    def __init__(self, id_cliente, nombre, correo):
        # Validación estricta
        if not isinstance(id_cliente, str) or len(id_cliente) < 3:
            raise DatoInvalidoError("ID de cliente inválido (mínimo 3 caracteres).")
        
        self.__id_cliente = id_cliente  # Atributo Privado
        self.nombre = nombre
        self.correo = correo

    def obtener_detalles(self):
        return f"Cliente: {self.nombre} | ID: {self.__id_cliente}"

# 5. SERVICIOS (Herencia y Polimorfismo)
class Servicio(EntidadBase, ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, cantidad):
        pass

class ReservaSalas(Servicio):
    def calcular_costo(self, horas):
        if horas <= 0: raise DatoInvalidoError("Las horas deben ser positivas.")
        return self.precio_base * horas

    def obtener_detalles(self):
        return f"[SALA] {self.nombre}"

class AlquilerEquipos(Servicio):
    def calcular_costo(self, dias):
        if dias <= 0: raise DatoInvalidoError("Los días deben ser positivos.")
        return self.precio_base * dias * 1.15

    def obtener_detalles(self):
        return f"[EQUIPO] {self.nombre}"

class AsesoriaEspecializada(Servicio):
    # SOBRECARGA SIMULADA: Cálculo básico o con impuestos/descuentos
    def calcular_costo(self, horas, impuesto=0.19, descuento=0):
        if horas <= 0: raise DatoInvalidoError("Tiempo de asesoría inválido.")
        subtotal = self.precio_base * horas
        total = (subtotal * (1 + impuesto)) - descuento
        return total

    def obtener_detalles(self):
        return f"[ASESORÍA] {self.nombre}"

# 6. CLASE RESERVA (Manejo robusto de excepciones)
class Reserva:
    def __init__(self, cliente, servicio, cantidad):
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"

    def procesar(self):
        try:
            print(f"--- Procesando: {self.cliente.nombre} ---")
            
            # Validación de integridad
            if self.servicio is None:
                raise ValueError("El servicio no existe.")
            
            total = self.servicio.calcular_costo(self.cantidad)
            
        except ValueError as e:
            # ENCADENAMIENTO DE EXCEPCIONES (Requisito)
            raise ReservaError("No se pudo procesar la reserva por falta de objeto") from e
            
        except DatoInvalidoError as e:
            logging.error(f"Error de datos: {e}")
            self.estado = "Cancelada (Datos Inválidos)"
            print(f"AVISO: {e}")
            
        else:
            # BLOQUE ELSE (Se ejecuta si NO hubo excepción en el try)
            self.estado = "Confirmada"
            print(f"ÉXITO: {self.servicio.obtener_detalles()}. Total: ${total:.2f}")
            
        finally:
            # BLOQUE FINALLY (Se ejecuta siempre)
            print(f"Estado Final: {self.estado}\n")

# 7. EJECUCIÓN DE LAS 10 SIMULACIONES
def ejecutar_sistema():
    print("=== SOFTWARE FJ - SISTEMA ROBUSTO ===\n")
    
    # Datos de prueba
    try:
        paula = Cliente("UV123", "Paula Vanegas", "paula@unad.edu.co")
        sala = ReservaSalas("Sala Pro", 50000)
        equipo = AlquilerEquipos("Cámara 4K", 30000)
        asesoria = AsesoriaEspecializada("Consultoría Multimedia", 100000)
    except Exception as e:
        print(f"Error fatal al inicializar: {e}")
        return

    # 10 Operaciones (Mezcla de éxitos y errores provocados)
    operaciones = [
        (paula, sala, 3),            # 1. Éxito
        (paula, equipo, 2),          # 2. Éxito
        (paula, asesoria, 1),        # 3. Éxito
        (paula, sala, -1),           # 4. Error (Horas negativas)
        (paula, None, 5),            # 5. Error (Servicio nulo - Dispara encadenamiento)
        (paula, equipo, 0),          # 6. Error (Días cero)
        (paula, asesoria, 4),        # 7. Éxito
        (paula, sala, 10),           # 8. Éxito
        (paula, equipo, 1),          # 9. Éxito
        (paula, asesoria, 2)         # 10. Éxito
    ]

    for i, (c, s, cant) in enumerate(operaciones, 1):
        print(f"Operación #{i}:")
        try:
            reserva = Reserva(c, s, cant)
            reserva.procesar()
        except ReservaError as e:
            logging.error(f"Fallo crítico en op #{i}: {e}")
            print(f"ERROR CRÍTICO: {e} (Ver logs para detalles)\n")
        except Exception as e:
            logging.error(f"Error no esperado: {e}")
            print("El sistema recuperó estabilidad automáticamente.\n")

if __name__ == "__main__":
    ejecutar_sistema()