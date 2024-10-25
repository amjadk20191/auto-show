
import convert_numbers

from rest_framework.exceptions import APIException
import re
from datetime import datetime
import uuid



def CheckPhoneNumber(phone):
        try:
            pattern = r'^\d{3,15}$'

            if not re.match(pattern, phone):
                raise APIException(detail={"detail":"phone number is unvalid"})
        except:
            raise APIException(detail={"detail":"phone number is unvalid"})
        return str(convert_numbers.hindi_to_english(phone))
    
    
    

def UploadPath(Instance, Filname, Folder):
    Now = datetime.now()
    DateTime = Now.strftime("%m%d%Y%H%M%S")
    return Folder+'/'+''.join([ str(uuid.uuid4()) + str(DateTime) + Filname])
