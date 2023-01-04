from rest_framework.routers import DefaultRouter

from api.v1.theater.views import PerformanceViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'performances', PerformanceViewSet, basename='performance')
router.register(r'categories', CategoryViewSet, basename='category')

app_name = 'theater'
urlpatterns = router.urls