from django.urls import include, path
from rest_framework import routers
from election_results.api import views

router = routers.DefaultRouter()
router.register("parties", views.PartyViewSet)
router.register("partyvotecounts", views.PartyVoteCountViewSet)
router.register("constituencies", views.ConstituencyViewSet)
router.register("total-results", views.TotalResultsViewSet)

urlpatterns = router.urls + [
    path("upload/<str:filename>/", views.FileUploadView.as_view(), name="upload"),
]
