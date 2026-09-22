from rest_framework import serializers

class PredictInputSerializer(serializers.Serializer):
    frecuencia_compra = serializers.IntegerField(
        help_text="Número de compras realizadas por el cliente",
        default=1
    )
    monto_promedio = serializers.FloatField(
        help_text="Monto promedio de compra en pesos/dólares",
        default=12000.0
    )
    dias_ultima_compra = serializers.IntegerField(
        help_text="Días transcurridos desde la última compra",
        default=50
    )

class PredictOutputSerializer(serializers.Serializer):
    status = serializers.CharField()
    prediccion = serializers.CharField()
    nivel_riesgo = serializers.CharField()
    probabilidad_abandono = serializers.FloatField()
    datos_recibidos = serializers.DictField()
    recomendacion = serializers.CharField()
