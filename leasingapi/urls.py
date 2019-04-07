from leasingapi import views
from rest_framework import routers
app_name = 'leasingapi'
router = routers.DefaultRouter()

router.register(r"login", views.LoginViewSet, base_name="login")
router.register(r"logout", views.LogoutViewSet, base_name="logout")
router.register(r"signup", views.SignUpViewSet, base_name="signup")
router.register(r"leasing-user-info", views.LeasingUserInfoViewSet, base_name="leasing_user_info")
router.register(r"client-setting", views.ClientSettingModelViewSet, base_name="client_setting")
router.register(r'document-upload', views.DocumentUploadModelViewSet, base_name="document_upload")
router.register(r'invite-token', views.LeasingClientInviteTokenModelViewSet, base_name="leasing_client_invite_token")
router.register(r'legal-positions', views.LegalPositionModelViewSet, base_name="legal_positions")
router.register(r'reason', views.LegalTableReasonViewSet, base_name="reason")
router.register(r'text-search', views.TextSearchViewSet, base_name="text-search")
router.register(r'forgot-login', views.ForgotLoginViewSet, base_name="forgot-login")

urlpatterns = []
urlpatterns += router.urls
