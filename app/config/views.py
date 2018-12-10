from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


def index(request):
    return render(request, 'index.html')


@authentication_classes((TokenAuthentication, SessionAuthentication))
class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = {
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    }

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)
