from datetime import datetime
from EnumsReport import *

class ImpuestoTO:
  def __init__(self,codigo,codigoPorcentaje,baseImponible,tarifa,valor) -> None:
      self._codigo = codigo
      self._tipoImpuesto = TipoImpuesto.obtenerTipoImpuesto(codigo)
      print(self._tipoImpuesto)
      self._codigoPorcentaje = codigoPorcentaje
      self._baseImponible = baseImponible
      self._tarifa = tarifa
      self._valor = valor

  @property
  def tipoImpuesto(self):
      return self._tipoImpuesto  
  

class ComprobanteTO:
  def __init__(self,codDoc,ruc,estab,ptoEmi,secuencial,fechaEmision,impuestos) -> None:
      self._codDoc = codDoc
      self._ruc = ruc
      self._estab = estab
      self._ptoEmi = ptoEmi
      self._secuencial = secuencial
      self._fechaEmision = datetime.strptime(fechaEmision, '%d/%m/%Y')
      self._impuestos = impuestos
      self._totalIva = 0
      self._totalIce = 0
      self._gravaImpuesto = self._gravaImpuestoDevolucion()

  @property
  def ruc(self):        
      return self._ruc
  
  @property
  def nroFactura(self):        
      return "{festab}-{fptoEmi}-{fsec}".format(festab=self._estab,fptoEmi=self._ptoEmi,fsec=self._secuencial)
  
  @property
  def dia(self):        
      return self._fechaEmision.strftime("%d")
  
  @property
  def mes(self):        
      return self._fechaEmision.strftime("%m")
    
  @property
  def anio(self):        
      return self._fechaEmision.strftime("%Y")

  @property
  def impuestos(self):        
      return self._impuestos

  @property
  def totalIva(self):
    return self._totalIva

  @property
  def totalIce(self):
    return self._totalIce

  @property
  def codDoc(self):
    return self._codDoc
    
  @property
  def gravaImpuesto(self):
    return self._gravaImpuesto 

  def _gravaImpuestoDevolucion(self):
    tieneImpuestoGravado = False
    for impuesto in self._impuestos:      
      if TipoImpuesto.IVA == impuesto._tipoImpuesto:
        print("Grave deb iva")
        self._totalIva = self._totalIva+impuesto._valor
        print(self._totalIva)
        tieneImpuestoGravado = True
      elif TipoImpuesto.ICE == impuesto._tipoImpuesto:
        self._totalIce = self._totalIce+impuesto._valor
        tieneImpuestoGravado = True
    return tieneImpuestoGravado
  
