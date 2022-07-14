import base64
import xml.etree.ElementTree as ET
import pandas as pd
from EnumsReport import *
from EntitiesReport import *

class ProcessadorXML():
  def __init__(self,xml) -> None:
      self._xml = xml

  def procesar(self):
    root = ET.fromstring(self._xml)
    listXmlData = []
    print("All atributes ")    
    codDoc = root.find('infoTributaria/codDoc').text
    ruc = root.find('infoTributaria/ruc').text
    estab = root.find('infoTributaria/estab').text
    ptoEmi = root.find('infoTributaria/ptoEmi').text
    secuencial = root.find('infoTributaria/secuencial').text
    fechaEmision = root.find('infoFactura/fechaEmision').text
    impuestos = []
    for totalImpuesto in root.findall('infoFactura/totalConImpuestos/totalImpuesto'):
        codigo = int(totalImpuesto.find('codigo').text)
        codigoPorcentaje = totalImpuesto.find('codigoPorcentaje').text
        baseImponible = totalImpuesto.find('baseImponible').text
        nodoTarifa = totalImpuesto.find('tarifa')
        if nodoTarifa is None:
          tarifa = None
        else:
          tarifa = float(totalImpuesto.find('tarifa').text)
        valor = float(totalImpuesto.find('valor').text)
        print(valor)
        impuestoTO = ImpuestoTO(codigo,codigoPorcentaje,baseImponible,tarifa,valor)
        impuestos.append(impuestoTO)
    return ComprobanteTO(codDoc,ruc,estab,ptoEmi,secuencial,fechaEmision,impuestos)

  def crearListaDevIva(self,comprobantes:ComprobanteTO):
    listaComprobantes = []
    for comprobante in comprobantes:

      if comprobante.gravaImpuesto and TipoDocumento.FACTURA.value == comprobante.codDoc :
        print("Grava")      
        print(comprobante.dia)
        tuplaComprobante = {'RUC PROVEEDOR':comprobante.ruc,'NRO_FACTURA':comprobante.nroFactura,'DIA':comprobante.dia,'MES':comprobante.mes,'ANIO':comprobante.anio,'IVA':comprobante.totalIva,'ICE':comprobante.totalIce}      
        listaComprobantes.append(tuplaComprobante)
    return listaComprobantes

  def crearReporteDevIva(self,comprobantes:ComprobanteTO):
    listaComprobantes = self.crearListaDevIva(comprobantes)
    dfReporteDevIva = pd.DataFrame(listaComprobantes,
                    columns=['RUC PROVEEDOR','NRO_FACTURA','DIA','MES','ANIO','IVA','ICE' 
    ])
    return dfReporteDevIva
