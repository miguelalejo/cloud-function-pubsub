import base64
from MongoService import *

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
    mgConectorServ.find(bd_name="edocuments",collecion="bills",query= {'group_id': group_id },projection={ "group_id": 1, "_id": 1 ,"file_name":1,"blob_xml":1})
    print(pubsub_message)
