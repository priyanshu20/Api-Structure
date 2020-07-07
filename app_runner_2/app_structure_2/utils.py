import redis,nexmo,random
from .models import User,db

r=redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
client=nexmo.Client(key='5c7afd9f',secret='sLn6Vnzk3glV9fQ2')



def generate_otp(username,num):
    otp=random.randrange(1000000)
    r.set(username,otp)
    r.expire(username,300)
    num='+91'+num
    responseData=client.send_message({
        "from":"Flask Appplication",
        "to":num,
        "text":f"The OTP to verify your account is {otp} -Flask Application"
    })
    if responseData["messages"][0]["status"]=='0':
        return {"message":"Otp has been sent to your mobile number"}
    else:
        return {"error":f"Message failed with error: {responseData['messages'][0]['error-text']}"}
