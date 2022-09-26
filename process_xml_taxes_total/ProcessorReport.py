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
    identificacionComprador = root.find('infoFactura/identificacionComprador').text
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
    return ComprobanteTO(codDoc,ruc,estab,ptoEmi,secuencial,fechaEmision,identificacionComprador,impuestos)

class GenerarReporte():
  def crearListaDevIva(self,comprobantes:ComprobanteTO):
    listaComprobantes = []
    for comprobante in comprobantes:

      if comprobante.gravaImpuesto and TipoDocumento.FACTURA.value == comprobante.codDoc :
        print("Grava")
        print(comprobante.dia)
        tuplaComprobante = {'ID COMPRADOR':comprobante.identificacionComprador, 'RUC PROVEEDOR':comprobante.ruc,'NRO_FACTURA':comprobante.nroFactura,'DIA':comprobante.dia,'MES':comprobante.mes,'ANIO':comprobante.anio,'IVA':comprobante.totalIva,'ICE':comprobante.totalIce}      
        listaComprobantes.append(tuplaComprobante)
    return listaComprobantes,comprobante.identificacionComprador

  def crearReporteDevIva(self,comprobantes:ComprobanteTO):
    listaComprobantes,identificacionComprador = self.crearListaDevIva(comprobantes)
    custom_dict = {'01': 1, '02': 2, '03': 3,'04': 4,'05': 5,'06': 6,'07': 7,'08': 8,'09': 9,'10': 10,'11': 11,'12': 12} 

    dfReporteDevIva = pd.DataFrame(listaComprobantes,
                    columns=['ID COMPRADOR','RUC PROVEEDOR','NRO_FACTURA','DIA','MES','ANIO','IVA','ICE' 
    ])
    
    dfReporteDevIva['mes_rank'] = dfReporteDevIva.sort_values(by=['MES'], key=lambda x: x.map(custom_dict),ascending=[True]).groupby('MES')['IVA'].rank(ascending=True)
   
    
    #df['mes_rank'] = df.sort_values(by=['MES'], key=lambda x: x.map(custom_dict),ascending=[True]).groupby('MES')['Name'].rank(ascending=True)
    #dfReporteDevIva = df.sort_values(['MES', 'yearly_rank'])
    dfReporteDevIva = dfReporteDevIva.sort_values(by=['MES','mes_rank'])
    dfReporteDevIva.drop(columns=['mes_rank'],inplace=True)
    return dfReporteDevIva,identificacionComprador
  
  def exportarReporte(self,reporte,groupId):
    ruta = os.path.join(tmpdir,"{fId}.xlsx".format(fId=groupId))
    reporte.to_excel(ruta,index=False)
    return ruta
