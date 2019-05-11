from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q


class UserAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        # 这里有个问题，注册时需要保证用户名和邮箱名一定不同
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
