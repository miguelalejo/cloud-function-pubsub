class XmlFileTO: 
    def __init__(self, name, blob):
        self._name = name
        self._blob = blob   
    
    @property
    def name(self):        
        return self._name
        
    @name.setter
    def name(self, name):        
        self._name = name

    @property
    def blob(self):        
        return self._blob
        
    @blob.setter
    def blob(self, blob):        
        self._blob = blob

