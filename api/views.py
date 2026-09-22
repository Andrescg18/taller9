from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import PredictInputSerializer, PredictOutputSerializer

class PredictView(GenericAPIView):
    """
    Endpoint de Inferencia de IA:
    Predice el nivel de riesgo y comportamiento del cliente a partir de:
    - frecuencia_compra (int/float)
    - monto_promedio (float)
    - dias_ultima_compra (int/float)
    """
    serializer_class = PredictInputSerializer

    def get_serializer(self, *args, **kwargs):
        # Precarga automáticamente el formulario HTML del navegador con el JSON deseado
        if not args and not kwargs:
            s = PredictInputSerializer(data={
                "frecuencia_compra": 2,
                "monto_promedio": 15000,
                "dias_ultima_compra": 45
            })
            s.is_valid()
            return s
        return super().get_serializer(*args, **kwargs)

    @extend_schema(
        responses={200: PredictOutputSerializer},
        description="Información y estado del endpoint de inferencia.",
        summary="Estado de Inferencia"
    )
    def get(self, request, *args, **kwargs):
        return Response({
            "mensaje": "Endpoint de inferencia de IA activo. Envía una petición POST con los datos del cliente.",
            "ejemplo_payload": {
                "frecuencia_compra": 2,
                "monto_promedio": 15000,
                "dias_ultima_compra": 45
            }
        }, status=status.HTTP_200_OK)

    @extend_schema(
        request=PredictInputSerializer,
        responses={200: PredictOutputSerializer},
        description="Inferencia de IA para análisis de riesgo y predicción de comportamiento de compra del cliente.",
        summary="Predicción de Riesgo de Cliente",
        examples=[
            OpenApiExample(
                'Ejemplo de Inferencia',
                value={
                    "frecuencia_compra": 2,
                    "monto_promedio": 15000,
                    "dias_ultima_compra": 45
                },
                request_only=True,
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
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

predict_view = PredictView.as_view()
