from enum import Enum
class TipoDocumento(Enum):
  FACTURA = "01"
  LIQUIDACION_COMPRA =  "03"	
  NOTA_CREDITO = "04"
  NOTA_DEBITO = "05"
  GUIA_REMISION = "06"
  RETENCION = "07"  

class TipoImpuesto(Enum):    
  RENTA = 1
  IVA = 2
  ICE = 3
  IVA_PRENSUTIVO = 4
  IRBPNR = 5
  ISD = 6 
  def obtenerTipoImpuesto(codigo):
    for tipo in TipoImpuesto:
      if tipo.value == codigo:       
        return tipo
