import base64
from MongoService import *
from ProcessorReport import *

def hello_pubsub(event, context):
     """Triggered from a message on a Cloud Pub/Sub topic.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """
     pubsub_message = base64.b64decode(event['data']).decode('utf-8')
     uri = "cluster0.2gzpcvj.mongodb.net/?retryWrites=true&w=majority"
     user = "m001-student"
     password = "m001-mongodb-basics"    
     mgConectorServ = MongoServiceConector(uri, user, password)
     group_id = int(pubsub_message)
     documents = mgConectorServ.find(bd_name="edocuments",collecion="bills",query= {'group_id': group_id },projection={ "group_id": 1, "_id": 1 ,"file_name":1,"blob_xml":1})
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
          reporte = procesarComprobante.crearReporteDevIva(listComprobantes)
          reporte.to_excel("{fId}.xlsx".format(fId=group_id))
     print(pubsub_message)
