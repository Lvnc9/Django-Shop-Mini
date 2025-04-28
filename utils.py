### you right the functions which global and not related to
# any app should be put here ###
from django.contrib.auth.mixins import UserPassesTestMixin
from kavenegar import *

def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI("6554616D71674B3454365968735055394C46437344585048774B353071575842504D3777764144665038303D")
        params = {
            "sender" : "2000660110",  #1000689696 
            "receptor" : phone_number,
            "message" : f"رمز عبور شما برای ورود به جنگو-اپ: {code}"
        }
        response = api.sms_send(params)
        response = b"{response}".decode("utf-8")
        print(params)
    except APIException as e:
        print(phone_number)
        #d = e.decode("utf-8")
        print(e)
    except HTTPException as e:
        #d = e.decode("utf-8")
        print(e)    


class IsAdminUserMixin(UserPassesTestMixin):
    """ 
    We override the UserPassesTestMixin to avoid repeating codes
    test_func is the code which checks the condition beofre accessing to the view  
    """
    
    def test_func(self):
        print("="*90)
        print(self.request.user)
        print("="*90)

        return self.request.user.is_authenticated and self.request.user.is_admin