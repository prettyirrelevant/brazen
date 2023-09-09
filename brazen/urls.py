"""
URL configuration for the brazen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from rest_framework import status
from rest_framework.permissions import AllowAny


class HttpAndHttpsOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):  # noqa: FBT002
        schema = super().get_schema(request, public)
        schema.schemes = ['http', 'https']
        return schema


docs_schema_view = get_schema_view(
    openapi.Info(
        title='BridgeBloc API',
        default_version='v1',
        description='BridgeBloc API',
        license=openapi.License(name='MIT License'),
    ),
    generator_class=HttpAndHttpsOpenAPISchemaGenerator,
    public=True,
    permission_classes=[AllowAny],
)


def handler_400(request, exception, *args, **kwargs):  # noqa: ARG001
    return JsonResponse(data={'message': 'Bad request', 'errors': None}, status=status.HTTP_400_BAD_REQUEST)


def handler_404(request, exception):  # noqa: ARG001
    return JsonResponse(data={'message': 'Not found', 'errors': None}, status=status.HTTP_404_NOT_FOUND)


def handler_500(request):  # noqa: ARG001
    return JsonResponse(
        data={
            'message': "We're sorry, but something went wrong on our end",
            'errors': None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


handler400 = handler_400
handler404 = handler_404
handler500 = handler_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.accounts.urls')),
    path('api/docs', docs_schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
]
