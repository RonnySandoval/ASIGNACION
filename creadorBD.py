from sqlalchemy import (create_engine, Column, String, Integer, ForeignKey, Index)
from sqlalchemy.orm import declarative_base, relationship
import re
import os
import ventanas_emergentes

Base = declarative_base()  # Base de Declaración

# Tablas en representación de clases

class INFORMACION(Base):
    __tablename__    = 'INFORMACION'
    NOMBRE_PLANTA    = Column(String, primary_key=True)
    DESCRIPCION      = Column(String)

class PROCESOS(Base):
    __tablename__   = 'PROCESOS'
    ID_PROCESO      = Column(String, primary_key=True)
    NOMBRE          = Column(String)
    DESCRIPCION     = Column(String)
    SECUENCIA       = Column(Integer)

class TECNICOS(Base):
    __tablename__   = 'TECNICOS'
    ID_TECNICO      = Column(String, primary_key=True)
    NOMBRE          = Column(String)
    APELLIDO        = Column(String)
    DOCUMENTO       = Column(String)
    ESPECIALIDAD    = Column(String)

class TECNICOSPROCESOS(Base):
    __tablename__   = 'TECNICOS_PROCESOS'
    TEC_PROC        = Column(String, primary_key=True)
    ID_TECNICO      = Column(String)
    ID_PROCESO      = Column(String)

class MODELOS(Base):
    __tablename__   = 'MODELOS'
    ID_MODELO       = Column(String, primary_key=True)
    MARCA           = Column(String)
    MODELO          = Column(String)
    ESPECIFICACION  = Column(String, nullable=True)

class MODELOSREFERENCIAS(Base):
    __tablename__   = 'MODELOS_REFERENCIAS'
    REFERENCIA      = Column(String, primary_key=True)
    ID_MODELO       = Column(String)

class TIEMPOSMODELOS(Base):
    __tablename__   = 'TIEMPOS_MODELOS'
    PROCESO_MODELO  = Column(String, primary_key=True)
    ID_PROCESO      = Column(String)
    ID_MODELO       = Column(String)
    TIEMPO          = Column(Integer)

class PEDIDOS(Base):
    __tablename__   = 'PEDIDOS'
    ID_PEDIDO       = Column(String, primary_key=True)
    CLIENTE         = Column(String)
    FECHA_RECEPCION = Column(Integer)
    ENTREGA_ESTIMADA = Column(Integer)
    FECHA_ENTREGA   = Column(Integer)
    CONSECUTIVO     = Column(Integer)

class VEHICULOS(Base):
    __tablename__   = 'VEHICULOS'
    CHASIS          = Column(String, primary_key=True)
    ID_MODELO       = Column(String)
    COLOR           = Column(String)
    REFERENCIA      = Column(String)
    FECHA_INGRESO   = Column(Integer)
    NOVEDADES       = Column(String)
    SUBCONTRATAR    = Column(String)
    ID_PEDIDO       = Column(String)

class TIEMPOSVEHICULOS(Base):
    __tablename__   = 'TIEMPOS_VEHICULOS'
    PROCESO_CHASIS  = Column(String, primary_key=True)
    ID_PROCESO      = Column(String)
    CHASIS          = Column(String)
    TIEMPO          = Column(Integer)

class HISTORICOS(Base):
    __tablename__       = 'HISTORICOS'
    CODIGO_ASIGNACION   = Column(String, primary_key=True)
    ID_TECNICO          = Column(String)
    CHASIS              = Column(String)
    ID_PROCESO          = Column(String)
    OBSERVACIONES       = Column(String)
    INICIO              = Column(Integer)
    FIN                 = Column(Integer)
    DURACION            = Column(Integer)
    ESTADO              = Column(String)

class PROGRAMAS(Base):
    __tablename__   = 'PROGRAMAS'
    ID_PROGRAMA     = Column(String, primary_key=True)
    DESCRIPCION     = Column(String)

class ORDENES(Base):
    __tablename__   = 'ORDENES'
    CODIGO_ORDEN    = Column(String, primary_key=True)
    ID_PROGRAMA     = Column(String)
    CHASIS          = Column(String)
    ID_TECNICO      = Column(String)
    ID_PROCESO      = Column(String)
    OBSERVACIONES   = Column(String)
    INICIO          = Column(Integer)
    FIN             = Column(Integer)
    DURACION        = Column(Integer)

# Crear el motor de la base de datos y las tablas
def crea_BBDD(nombre):
    nombre_modificado = re.sub(r'\s+', '_', nombre).lower()  # Reemplaza múltiples espacios consecutivos por un solo '_' y pasa a minusculas
    nombreBD =f"planta_{nombre_modificado}.db"

    # Verificar si el archivo de la base de datos ya existe
    if os.path.exists(nombreBD):
        print(f"La base de datos '{nombreBD}' ya existe.")
        ventanas_emergentes.messagebox.showinfo("Base de Datos existente", f"La base de datos '{nombreBD}' ya existe.")
        return "existe"

    motor = f"sqlite:///{nombreBD}"
    engine = create_engine(motor) 
    Base.metadata.create_all(engine)
    mensaje= f"""
    Base de datos creada con éxito.
    Motor: {motor}
    Nombre: {nombreBD}"""
    
    print(mensaje)
    ventanas_emergentes.messagebox.showinfo("Base de Datos creada", mensaje)
    return nombreBD
















##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


# Base de Declaración
BaseFK = declarative_base()

# Tablas en representación de clases
class ModelosFK(BaseFK):
    __tablename__   = 'modelos'
    id_modelo       = Column(String, primary_key=True)
    marca           = Column(String)
    modelo          = Column(String)
    especificacion  = Column(String, nullable=True)

class ProcesosFK(BaseFK):
    __tablename__   = 'procesos'
    id_proceso      = Column(String, primary_key=True)
    nombre          = Column(String)
    descripcion     = Column(String)
    secuencia       = Column(Integer)

class TecnicosFK(BaseFK):
    __tablename__   = 'tecnicos'
    id_tecnico      = Column(String, primary_key=True)
    nombre          = Column(String)
    apellido        = Column(String)
    especialidad    = Column(String)

class PedidosFK(BaseFK):
    __tablename__   = 'pedidos'
    id_pedido       = Column(String, primary_key=True)
    cliente         = Column(String)
    fecha_recepcion = Column(Integer)
    entrega_estimada = Column(Integer)
    fecha_entrega   = Column(Integer)
    consecutivo     = Column(Integer)

class VehiculosFK(BaseFK):
    __tablename__   = 'vehiculos'
    chasis          = Column(String, primary_key=True)
    id_modelo       = Column(String, ForeignKey('modelos.id_modelo'))
    color           = Column(String)
    referencia      = Column(String)
    fecha_ingreso   = Column(Integer)
    novedades       = Column(String)
    subcontratar    = Column(String)
    id_pedido       = Column(String, ForeignKey('pedidos.id_pedido'))

class ModelosReferenciasFK(BaseFK):
    __tablename__   = 'modelos_referencias'
    referencia      = Column(String, primary_key=True)
    id_modelo       = Column(String, ForeignKey('modelos.id_modelo'))

class TiemposModelosFK(BaseFK):
    __tablename__   = 'tiempos_modelos'
    proceso_modelo  = Column(String, primary_key=True)
    id_proceso      = Column(String, ForeignKey('procesos.id_proceso'))
    id_modelo       = Column(String, ForeignKey('modelos.id_modelo'))
    tiempo          = Column(Integer)

class TiemposVehiculosFK(BaseFK):
    __tablename__   = 'tiempos_vehiculos'
    proceso_chasis  = Column(String, primary_key=True)
    id_proceso      = Column(String, ForeignKey('procesos.id_proceso'))
    chasis          = Column(String, ForeignKey('vehiculos.chasis'))
    tiempo          = Column(Integer)

class HistoricosFK(BaseFK):
    __tablename__       = 'historicos'
    codigo_asignacion   = Column(String, primary_key=True)
    id_tecnico          = Column(String, ForeignKey('tecnicos.id_tecnico'))
    chasis              = Column(String, ForeignKey('vehiculos.chasis'))
    id_proceso          = Column(String, ForeignKey('procesos.id_proceso'))
    observaciones       = Column(String)
    inicio              = Column(Integer)
    fin                 = Column(Integer)
    duracion            = Column(Integer)
    estado              = Column(String)

class ProgramasFK(BaseFK):
    __tablename__   = 'programas'
    id_programa     = Column(String, primary_key=True)
    descripcion     = Column(String)

class OrdenesFK(BaseFK):
    __tablename__   = 'ordenes'
    codigo_orden    = Column(String, primary_key=True)
    id_programa     = Column(String, ForeignKey('programas.id_programa'))
    chasis          = Column(String, ForeignKey('vehiculos.chasis'))
    id_tecnico      = Column(String, ForeignKey('tecnicos.id_tecnico'))
    id_proceso      = Column(String, ForeignKey('procesos.id_proceso'))
    observaciones   = Column(String)
    inicio          = Column(Integer)
    fin             = Column(Integer)
    duracion        = Column(Integer)

class TecnicosProcesosFK(BaseFK):
    __tablename__   = 'tecnicos_procesos'
    tec_proc        = Column(String, primary_key=True)
    id_tecnico      = Column(String, ForeignKey('tecnicos.id_tecnico'))
    id_proceso      = Column(String, ForeignKey('procesos.id_proceso'))

class InformacionFK(BaseFK):
    __tablename__   = 'informacion'
    planta        = Column(String, primary_key=True)
    descripcion      = Column(String)


# Crear el motor de la base de datos y las tablas
def crea_BBDD_FK(nombre):
    nombre = re.sub(r'\s+', '_', nombre)  # Reemplaza múltiples espacios consecutivos por un solo '_'
    motor = f"sqlite:///planta_{nombre}.db"

    engine = create_engine(motor) 
    BaseFK.metadata.create_all(engine)
    print(f"Base de datos creada con motor: {motor}")
    return motor



"""CREATE TABLE "HISTORICOS" (
	"CODIGO_ASIGNACION"	TEXT NOT NULL UNIQUE,
	"CHASIS"	TEXT NOT NULL,
	"ID_TECNICO"	TEXT NOT NULL,
	"ID_PROCESO"	TEXT NOT NULL,
	"OBSERVACIONES"	TEXT,
	"INICIO"	INTEGER NOT NULL,
	"FIN"	INTEGER,
	"DURACION"	INTEGER,
	"ESTADO"	TEXT NOT NULL,
	PRIMARY KEY("CODIGO_ASIGNACION"),
	--FOREIGN KEY("CHASIS") REFERENCES "VEHICULOS"("CHASIS"),
	--FOREIGN KEY("ID_PROCESO") REFERENCES "PROCESOS"("ID_PROCESO"),
	--FOREIGN KEY("ID_TECNICO") REFERENCES "TECNICOS"("ID_TECNICO")
)

CREATE TABLE "MODELOS" (
	"ID_MODELO"	TEXT NOT NULL UNIQUE,
	"MARCA"	TEXT NOT NULL,
	"MODELO"	TEXT NOT NULL,
	"ESPECIFICACION"	TEXT,
	PRIMARY KEY("ID_MODELO")
)

CREATE TABLE "MODELOS_REFERENCIAS" (
	"REFERENCIA"	TEXT UNIQUE,
	"ID_MODELO"	TEXT,
	PRIMARY KEY("REFERENCIA"),
	--FOREIGN KEY("ID_MODELO") REFERENCES "MODELOS"("ID_MODELO")
)

CREATE TABLE "ORDENES" (
	"CODIGO_ORDEN"	TEXT NOT NULL,
	"CHASIS"	TEXT NOT NULL,
	"ID_TECNICO"	TEXT NOT NULL,
	"ID_PROCESO"	TEXT NOT NULL,
	"OBSERVACIONES"	TEXT,
	"INICIO"	INTEGER NOT NULL,
	"FIN"	INTEGER NOT NULL,
	"DURACION"	INTEGER NOT NULL,
	"ID_ORDENES" TEXT,
	PRIMARY KEY("CODIGO_ORDEN"),
	--FOREIGN KEY("CHASIS") REFERENCES "VEHICULOS"("CHASIS"),
	--FOREIGN KEY("ID_PROCESO") REFERENCES "PROCESOS"("ID_PROCESO"),
	--FOREIGN KEY("ID_TECNICO") REFERENCES "TECNICOS"("ID_TECNICO"),
	--FOREIGN KEY("ID_PROGRAMA") REFERENCES "PROGRAMAS("ID_PROGRAMAS")
)


CREATE TABLE "PEDIDOS" (
	"ID_PEDIDO"	TEXT NOT NULL UNIQUE,
	"CLIENTE"	TEXT,
	"FECHA_RECEPCION"	INTEGER NOT NULL,
	"ENTREGA_ESTIMADA"	INTEGER,
	"FECHA_ENTREGA"	INTEGER, CONSECUTIVO INTEGER,
	PRIMARY KEY("ID_PEDIDO")
)

CREATE TABLE "PROCESOS" (
	"ID_PROCESO"	TEXT NOT NULL UNIQUE,
	"NOMBRE"	TEXT NOT NULL UNIQUE,
	"DESCRIPCION"	TEXT, SECUENCIA INTEGER,
	PRIMARY KEY("ID_PROCESO")
)

CREATE TABLE "REFERENCIAS" (
"REFERENCIA" TEXT,
  "ID_MODELO" TEXT,
	PRIMARY KEY("REFERENCIA"),
	--FOREIGN KEY("ID_MODELO") REFERENCES "MODELOS"("ID_MODELO")
)

CREATE TABLE "TECNICOS" (
	"ID_TECNICO"	TEXT NOT NULL UNIQUE,
	"NOMBRE"	TEXT NOT NULL,
	"APELLIDO"	TEXT NOT NULL,
	"DOCUMENTO"	INTEGER UNIQUE,
	"ESPECIALIDAD"	TEXT NOT NULL,
	PRIMARY KEY("ID_TECNICO")
)

CREATE TABLE "TECNICO_PROCESO" (
	"PROCESO_TECNICO"	TEXT NOT NULL UNIQUE,
	"ID_PROCESO"	TEXT NOT NULL,
	"ID_TECNICO"	TEXT NOT NULL,
	PRIMARY KEY("ESPECIALIDAD_TECNICO"),
	--FOREIGN KEY("ID_PROCESO") REFERENCES "PROCESOS"("ID_PROCESO"),
	--FOREIGN KEY("ID_TECNICO") REFERENCES "TECNICOS"("ID_TECNICO")
)

CREATE TABLE "TIEMPOS_MODELOS" (
	"PROCESO_MODELO"	TEXT NOT NULL UNIQUE,
	"ID_PROCESO"	TEXT NOT NULL,
	"ID_MODELO"	TEXT NOT NULL,
	"TIEMPO"	INTEGER NOT NULL,
	PRIMARY KEY("PROCESO_MODELO"),
	--FOREIGN KEY("ID_MODELO") REFERENCES "MODELOS"("ID_MODELO"),
	--FOREIGN KEY("ID_PROCESO") REFERENCES "PROCESOS"("ID_PROCESO")
)

CREATE TABLE "TIEMPOS_VEHICULOS" (
"PROCESO_CHASIS" TEXT,
  "ID_PROCESO" TEXT,
  "CHASIS" TEXT,
  "TIEMPO" REAL,
  PRIMARY KEY ("PROCESO_CHASIS"),
  --FOREIGN KEY("ID_PROCESO") REFERENCES "PROCESOS"("ID_PROCESO"),
  --FOREIGN KEY("CHASIS") REFERENCES "VEHICULOS"("CHASIS")
)

CREATE TABLE "VEHICULOS" (
"CHASIS" TEXT,
  "ID_MODELO" TEXT,
  "COLOR" TEXT,
  "REFERENCIA" TEXT,
  "FECHA_INGRESO" TEXT,
  "NOVEDADES" TEXT,
  "SUBCONTRATAR" TEXT,
  "ID_PEDIDO" TEXT,
  PRIMARY KEY ("PROCESO_CHASIS"),
  --FOREIGN KEY("ID_PEDIDO") REFERENCES "PEDIDOS"("ID_PEDIDO")
)

CREATE TABLE "PROGRAMAS" (
"ID_PROGRAMA" TEXT,
"DESCRIPCION" TEXT,
  PRIMARY KEY ("ID_PROGRAMA")
  )
"""
