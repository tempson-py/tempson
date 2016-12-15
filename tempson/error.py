import sys

class TemplateTypeError(BaseException):
    
    def __init__(self, typeName):
        sys.stderr.write('[Tempson] Excepted string instead of ' + str(typeName))
        
