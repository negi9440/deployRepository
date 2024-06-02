# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend
# from django.db import OperationalError
# import logging

# logger = logging.getLogger(__name__)

# class CustomUserBackend(ModelBackend):
#     def authenticate(self, request, user_id_field=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         if user_id_field is None or password is None:
#             return None
#         try:
#             # UserModel.USERNAME_FIELD の代わりに 'user_id_field' を使用
#             user = UserModel.objects.get(user_id_field=user_id_field)
#             if user.check_password(password):
#                 return user
#         except UserModel.DoesNotExist:
#             return None
        
            
# ロガーの設定
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)  # ログレベルの設定

# class CustomUserBackend(ModelBackend):
#     def authenticate(self, request, user_id_field=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(user_id_field=user_id_field)
#             if user.check_password(password):
#                 return user
#         except UserModel.DoesNotExist:
#             logger.info("Authentication failed: User does not exist")
#         except OperationalError as e:
#             logger.error(f"Database error occurred during authentication: {e}")
#         except Exception as e:
#             logger.exception("An unexpected error occurred during authentication")
#             raise e  # 予期せぬエラーは再スローして明確にする
#         return None



# class CustomUserBackend(ModelBackend):
#      def authenticate(self, request, user_id_field=None, password=None, **kwargs):
#          UserModel = get_user_model()
#          try:
#              user = UserModel.objects.get(user_id_field=user_id_field)
#              if user.check_password(password):
#                   return user
#          except UserModel.DoesNotExist:
#              logger.info("Authentication failed: User does not exist")
#          except OperationalError as e:
#              logger.error(f"Database error occurred during authentication: {e}")
#             # ここで OperationalError を特定して対処することができます
#          except Exception as e:
#              logger.exception("An unexpected error occurred during authentication")
#              raise e  # 予期せぬエラーは再スローして明確にする
#          return None

