from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth_users.admin_views import CreateManagerView, AdminStatsView, ActivateManagerLinkView, \
    RecoveryManagerLinkView, BanManagerView, UnbanManagerView, DeleteManagerView
from apps.auth_users.auth_views import ActivateUserView, RecoveryPasswordRequestView, RecoverPasswordView, SocketView, \
    CurrentUserView, LoginView
from apps.auth_users.manager_views import ManagerViewSet

router = DefaultRouter()
router.register(r'admin/managers', ManagerViewSet, basename='admin-managers')

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # AUTH
    path('activate/<str:token>/', ActivateUserView.as_view(), name='activate_user'),
    path('recovery/', RecoveryPasswordRequestView.as_view(), name='recovery_request'),
    path('recovery/<str:token>/', RecoverPasswordView.as_view(), name='recovery_password'),
    path('token/', SocketView.as_view(), name='socket_token'),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),

    # ADMIN
    path('admin/create-manager/', CreateManagerView.as_view(), name='admin-create-manager'),
    path('admin/stats/', AdminStatsView.as_view(), name='admin-stats'),
    path('admin/activate-manager/', ActivateManagerLinkView.as_view(), name='activate-manager'),
    path('admin/recovery-manager/', RecoveryManagerLinkView.as_view(), name='admin-recovery-manager'),
    path('admin/ban-manager/', BanManagerView.as_view(), name='admin-ban-manager'),
    path('admin/unban-manager/', UnbanManagerView.as_view(), name='admin-unban-manager'),
    path('admin/delete-manager/', DeleteManagerView.as_view(), name='delete-manager'),
]

urlpatterns += router.urls
