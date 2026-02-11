from rest_framework.routers import DefaultRouter

from src.quotes.api.views import QuoteViewSet

router = DefaultRouter()

router.register(r"quotes", QuoteViewSet, basename="quotes")

urlpatterns = router.urls
