from rest_framework import serializers

class PredictInputSerializer(serializers.Serializer):
    frecuencia_compra = serializers.IntegerField(
        help_text="Número de compras realizadas por el cliente",
        default=2
    )
    monto_promedio = serializers.IntegerField(
        help_text="Monto promedio de compra",
        default=15000
    )
    dias_ultima_compra = serializers.IntegerField(
        help_text="Días transcurridos desde la última compra",
        default=45
    )

class PredictOutputSerializer(serializers.Serializer):
    status = serializers.CharField()
    prediccion = serializers.CharField()
    nivel_riesgo = serializers.CharField()
    probabilidad_abandono = serializers.FloatField()
    datos_recibidos = serializers.DictField()
    recomendacion = serializers.CharField()
