from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import FileListCreateView, FileDetailView, FileDownloadView, FilePublicDownloadView, RegenerateLinkView

urlpatterns = [
    path('', FileListCreateView.as_view(), name='file-list-create'),
    path('<int:pk>/', FileDetailView.as_view(), name='file-detail'),
    path('<int:pk>/download/', FileDownloadView.as_view(), name='file-download'),
    path('public/<uuid:link_uuid>/', FilePublicDownloadView.as_view(), name='file-public-download'),
    path('<int:pk>/regenerate-link/', RegenerateLinkView.as_view(), name='regenerate-link'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
