import base64, uuid
from django.core.files.base import ContentFile

def get_report_image(data):
    f , str_image = data.split(';base64')
    decoded_img = base64.b64decode(str_image)
    img_name = str(uuid.uuid64())[:10] + '.png'
    data = ContentFile(decoded_img, name=img_name)
    return data