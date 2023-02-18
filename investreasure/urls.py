from django.urls import path, include

urlpatterns = [
    path('base/', include('base.urls')),
    path('history/', include('history.urls')),
]

# API versioning
urlpatterns = [
    path('v0/', include(urlpatterns))
]
