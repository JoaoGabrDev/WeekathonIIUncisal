import qrcode
from io import BytesIO
import base64

def gerar_qrcode(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
