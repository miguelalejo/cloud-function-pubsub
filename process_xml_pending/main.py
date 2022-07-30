import base64
from MongoService import *
import requests
from bson import ObjectId

def updateOne(mgConector,id):
    try:
        newvalues = { "$set": { "status": "DONE" } }
        mgConector.update_one(bd_name="edocuments",collecion="pending_groups",query={"_id":id}, value=newvalues) 
    except DuplicateKeyError as e:
        print(e)
        print("Errro insert")

def hello_pubsub(event, context):
     """Triggered from a message on a Cloud Pub/Sub topic.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """
     print("Data",event['data'])
     pubsub_message = base64.b64decode(event['data']).decode('utf-8')
     uri = "cluster0.2gzpcvj.mongodb.net/?retryWrites=true&w=majority"
     user = "m001-student"
     password = "m001-mongodb-basics"    
     mgConectorServ = MongoServiceConector(uri, user, password)
     documents = mgConectorServ.find(bd_name="edocuments",collecion="pending_groups",query= {'status':'PENDING'},projection={ "group_id": 1,"nFiles": 1})     
     nFileSaved = documents.count()
     print("Tamanio lista Pending",nFileSaved)
     for doc in documents:
          if "group_id" in doc.keys():           
               groupId = doc["group_id"]
               nFiles = doc["nFiles"]
               print("Generar Pending",groupId)
               r = requests.put("https://fnservicefunctionfra-pcqrvbtxdq-uc.a.run.app/", data={'idTransaction': groupId, 'nFiles': nFiles})
               print(r.status_code, r.reason)
               updateOne(mgConectorServ,groupId)
     
    
