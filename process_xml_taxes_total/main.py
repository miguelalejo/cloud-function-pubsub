import base64
from MongoService import *
from ProcessorReport import *
import datetime
import json

def createObject(mgConector,groupId,blobExcel,ruc):
    try:
        mgConector.insert_one(bd_name="edocuments",collecion="excel_dev_reports", value={'group_id': groupId, 'blob_excel': blobExcel,  'ruc':ruc,'date':datetime.datetime.utcnow()}) 
    except DuplicateKeyError as e:
        print(e)
        print("Errro insert")

def createBatchProcess(mgConector,groupId,nFiles):
    try:
        mgConector.insert_one(bd_name="edocuments",collecion="pending_groups", value={'group_id': groupId, 'nFiles': nFiles,  'status':'PENDING'}) 
    except DuplicateKeyError as e:
        print(e)
        print("Errro insert")

def readfile(filePath):
     in_file = open(filePath, "rb") # opening for [r]eading as [b]inary
     data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
     in_file.close()
     return data

def hello_pubsub(event, context):
     """Triggered from a message on a Cloud Pub/Sub topic.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """
     print("Data",event['data'])
     pubsub_message = base64.b64decode(event['data']).decode('utf-8')
     json_object = json.loads(pubsub_message)
     uri = "cluster0.2gzpcvj.mongodb.net/?retryWrites=true&w=majority"
     user = "m001-student"
     password = "m001-mongodb-basics"    
     mgConectorServ = MongoServiceConector(uri, user, password)
     groupId = int(json_object['idTransaction'])
     nFiles = int(json_object['nFiles'])
     documents = mgConectorServ.find(bd_name="edocuments",collecion="bills",query= {'group_id': groupId },projection={ "group_id": 1, "_id": 1 ,"file_name":1,"blob_xml":1})     
     nFileSaved = documents.count()
     print("Tamanio lista",nFileSaved)
     print("Tamanio lista esperado",nFiles)
     if nFileSaved == nFiles:
          listComprobantes = []
          for doc in documents:
               if "blob_xml" in doc.keys():
                    print(doc)
                    print("Generar Blob")
                    fileBlob = doc["blob_xml"]
                    print(fileBlob)
                    procesarComprobante = ProcessadorXML(fileBlob) 
                    comprobanteTO = procesarComprobante.procesar()
                    listComprobantes.append(comprobanteTO)
          
          
          if len(listComprobantes):
               print("Generar Reporte")
               generarReporte = GenerarReporte()
               reporte,ruc = generarReporte.crearReporteDevIva(listComprobantes)
               filePath = generarReporte.exportarReporte(reporte,groupId)
               print("Generarado Reporte")
               blobExcel = readfile(filePath)
               createObject(mgConectorServ,groupId,blobExcel,ruc)
               print("Enviado Reporte")
          
          print(pubsub_message)
     else:
          print("Registerd pendien transation")
          createBatchProcess(mgConectorServ,groupId,nFiles)
     

