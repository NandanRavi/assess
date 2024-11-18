import jwt
from django.conf import settings
from .models import CustomUser
from datetime import datetime, timedelta

def encode_jwt(user):
    expiration_time = datetime.now() + timedelta(minutes=10)
    payload = {
        'user_id': user.id,
        'exp': expiration_time.timestamp()
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
        # user_id = payload.get('user_id')
        # user = CustomUser.objects.get(id=user_id)
        # return user
    except jwt.ExpiredSignatureError:
        return None
    except (jwt.InvalidTokenError, CustomUser.DoesNotExist) as e:
        return None