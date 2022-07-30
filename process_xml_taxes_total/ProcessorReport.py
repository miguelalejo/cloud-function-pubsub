import base64
import xml.etree.ElementTree as ET
import pandas as pd
from EnumsReport import *
from EntitiesReport import *
import tempfile
import os
tmpdir = tempfile.gettempdir()

class ProcessadorXML():
  def __init__(self,xml) -> None:
      self._xml = xml
  
  def extract_inner(self):
    root = ET.fromstring(self._xml)
    vs_data = root.find('.//comprobante')
    inner_xml = vs_data.text.strip()
    return ET.fromstring(inner_xml)

  def procesar(self):
    root = self.extract_inner()
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

class GenerarReporte():
  def crearListaDevIva(self,comprobantes:ComprobanteTO):
    listaComprobantes = []
    for comprobante in comprobantes:

      if comprobante.gravaImpuesto and TipoDocumento.FACTURA.value == comprobante.codDoc :
        print("Grava")
        print(comprobante.dia)
        tuplaComprobante = {'RUC PROVEEDOR':comprobante.ruc,'NRO_FACTURA':comprobante.nroFactura,'DIA':comprobante.dia,'MES':comprobante.mes,'ANIO':comprobante.anio,'IVA':comprobante.totalIva,'ICE':comprobante.totalIce}      
        listaComprobantes.append(tuplaComprobante)
    return listaComprobantes,comprobante.ruc

  def crearReporteDevIva(self,comprobantes:ComprobanteTO):
    listaComprobantes,ruc = self.crearListaDevIva(comprobantes)
    dfReporteDevIva = pd.DataFrame(listaComprobantes,
                    columns=['RUC PROVEEDOR','NRO_FACTURA','DIA','MES','ANIO','IVA','ICE' 
    ]).sort_values(by='IVA', ascending=False)
    return dfReporteDevIva,ruc
  
  def exportarReporte(self,reporte,groupId):
    ruta = os.path.join(tmpdir,"{fId}.xlsx".format(fId=groupId))
    reporte.to_excel(ruta,index=False)
    return ruta
