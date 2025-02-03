from fastapi import FastAPI, BackgroundTasks, HTTPException
import smtplib
from pydantic import BaseModel, Query, EmailStr
import time

app = FastAPI()


class Userdata(BaseModel):
    sender: EmailStr = Query(..., description='Enter the email of the sender', example='sender@gmail.com')
    password: str = Query(..., description='Enter the password of the email of the sender')
    receiver: EmailStr = Query(..., description='Enter the email of the receiver', example='reciever@gmail.com')
    message: str = Query(..., description='Enter the message for the email')


def send_email(userdata: Userdata):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(userdata.sender, userdata.password)
        server.sendmail(userdata.sender, userdata.receiver, userdata.message)

        raise HTTPException(status_code=200, detail="The message was succesfully sended")

    except Exception as _ex:
        raise HTTPException(status_code=400, detail=f'There were some errors, more details: {str(_ex)}')


@app.post('/send_email')
def send_email(background_tasks: BackgroundTasks, userdata: Userdata):
    background_tasks.add_task(send_email, userdata)
    time.sleep(5)
    return {'message': 'done'}
