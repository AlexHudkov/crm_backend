from rest_framework.routers import DefaultRouter
from .views import GroupViewSet

router = DefaultRouter()
router.register(r'', GroupViewSet, basename='learning_groups')

urlpatterns = router.urls
