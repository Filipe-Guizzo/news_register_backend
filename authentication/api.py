from ninja import Router, Schema
from typing import Optional
import bcrypt
from person.models import Person
import smtplib
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import EMAIL_SUPORT, EMAIL_PASSWORD
import bcrypt
from ninja.security import HttpBearer

router = Router()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            Person.objects.get(token=token)
            return token
        except:
            return False

class LoginSchema(Schema):
    content: str = 'Successfully logged in'
    token: str
    person: int

class LoginSchemaIn(Schema):
    email: str
    password: str

class MessageSchema(Schema):
    content: str
    status:int
    error: Optional[str]

class SendCodeSchema(Schema):
    email: str
    code: str
    person: int

class SendCodeSchemaIn(Schema):
    email: str

class ResendCodeSchema(Schema):
    email: str
    code: str
    person: int

class ResendCodeSchemaIn(Schema):
    email: str
    code: str

class PasswordRecoverySchema(Schema):
    content: str
    status: int

class PasswordRecoverySchemaIn(Schema):
    password: str
    person: int


@router.post('/login/', response={200: LoginSchema, 401: MessageSchema})
def login(request, payload:LoginSchemaIn):
    try:
        json_data = payload.dict()
        email = json_data['email']
        password = json_data['password']
        
        person = Person.objects.get(email=email)
        
        if bcrypt.checkpw(password.encode('ascii'), person.password.encode('ascii')):
            return 200, {
                'token': person.token,
                'person': person.id
            }
        else:
            return 401,{
                'content': 'Incorrect password',
                'status': 401,
            }
    except Exception as e:
        return 401,{
            'content': 'Incorrect email',
            'status': 401,
            'error': str(e)
        }

@router.post('/send-code/', response={200: SendCodeSchema, 400: MessageSchema})
def send_code(request, payload:SendCodeSchemaIn):
    try:
        json_data = payload.dict()
        email = json_data['email']
        person = Person.objects.get(email=email)
        code = f'C-{randint(10000, 99999)}'

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Code Recovery'
        msg['From'] = EMAIL_SUPORT
        msg['To'] = email
        html = MIMEText(f"""
            <img style="width: 100%; height: 300px; object-fit: cover;" src="https://wallpaperaccess.com/full/2228834.jpg" alt="wallpaper"/>
            <h1 style="color:#A9A9A9;">This is your recovery code:</h1>
            <h2><strong>{code}</strong></h2>
        """, 'html') 
        msg.attach(html)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SUPORT, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return 200, {
            'email': email,
            'code': code,
            'person': person.id
        }
    except Exception as e:
        return 400,{
            'content': 'Error to send code',
            'status': 400,
            'error': str(e)
        }

@router.post('/resend-code/', response={200: ResendCodeSchema, 400: MessageSchema})
def resend_code(request, payload:ResendCodeSchemaIn):
    try:
        json_data = payload.dict()
        email = json_data['email']
        code = json_data['code']
        person = Person.objects.get(email=email)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Code Recovery'
        msg['From'] = EMAIL_SUPORT
        msg['To'] = email
        html = MIMEText(f"""
            <img style="width: 100%; height: 300px; object-fit: cover;" src="https://wallpaperaccess.com/full/2228834.jpg" alt="wallpaper"/>
            <h1 style="color:#A9A9A9;">This is your recovery code:</h1>
            <h2><strong>{code}</strong></h2>
        """, 'html') 
        msg.attach(html)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SUPORT, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return 200, {
            'email': email,
            'code': code,
            'person': person.id
        }
    except Exception as e:
        return 400,{
            'content': 'Error to resend code',
            'status': 400,
            'error': str(e)
        }

@router.put('/password-recovery/', response={200: PasswordRecoverySchema, 400: MessageSchema})
def password_recovery(request, payload:PasswordRecoverySchemaIn):
    try:
        json_data = payload.dict()
        password = json_data['password']
        id_person = json_data['person']
        #password cryptography
        password = json_data['password']
        password_hashed = bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt(14)).decode('utf-8')
        password = password_hashed
        
        person = Person.objects.get(id=id_person)
        person.password = password
        person.save()

        return 200, {
            'content': 'Successfully recovered password',
            'status': 200
        }
    except Exception as e:
        return 400,{
            'content': 'Error recovering password',
            'status': 400,
            'error': str(e)
        }