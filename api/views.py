from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import PredictInputSerializer, PredictOutputSerializer

@extend_schema(
    methods=['POST'],
    request=PredictInputSerializer,
    responses={200: PredictOutputSerializer},
    description="Inferencia de IA para análisis de riesgo y predicción de comportamiento de compra del cliente.",
    summary="Predicción de Riesgo de Cliente"
)
@extend_schema(
    methods=['GET'],
    responses={200: PredictOutputSerializer},
    description="Información y estado del endpoint de inferencia.",
    summary="Estado de Inferencia"
)
@api_view(['GET', 'POST'])
def predict_view(request):
    """
    Endpoint de Inferencia de IA:
    Predice el nivel de riesgo y comportamiento del cliente a partir de:
    - frecuencia_compra (int/float)
    - monto_promedio (float)
    - dias_ultima_compra (int/float)
    """
    if request.method == 'GET':
        return Response({
            "mensaje": "Endpoint de inferencia de IA activo. Envía una petición POST con los datos del cliente.",
            "ejemplo_payload": {
                "frecuencia_compra": 1,
                "monto_promedio": 12000.0,
                "dias_ultima_compra": 50
            }
        }, status=status.HTTP_200_OK)

    serializer = PredictInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            "status": "error",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    frecuencia = data['frecuencia_compra']
    monto = data['monto_promedio']
    dias = data['dias_ultima_compra']

    # Modelo heurístico de inferencia para segmentación y riesgo
    # Riesgo Alto: Muchos días sin comprar o muy baja frecuencia
    if dias >= 30 or frecuencia <= 3:
        clasificacion = "Cliente con Riesgo Alto"
        nivel_riesgo = "Alto"
        probabilidad = round(min(0.70 + (dias / 100.0) * 0.25, 0.99), 2)
        recomendacion = "Iniciar campaña de reactivación urgente y ofrecer cupones de descuento."
    else:
        clasificacion = "Cliente Activo / Bajo Riesgo"
        nivel_riesgo = "Bajo"
        probabilidad = round(max(0.05, 0.30 - (frecuencia / 50.0)), 2)
        recomendacion = "Mantener fidelización con recomendaciones de nuevos productos."

    return Response({
        "status": "success",
        "prediccion": clasificacion,
        "nivel_riesgo": nivel_riesgo,
        "probabilidad_abandono": probabilidad,
        "datos_recibidos": {
            "frecuencia_compra": frecuencia,
            "monto_promedio": monto,
            "dias_ultima_compra": dias
        },
        "recomendacion": recomendacion
    }, status=status.HTTP_200_OK)
