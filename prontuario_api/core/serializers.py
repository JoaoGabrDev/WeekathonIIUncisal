from rest_framework import serializers
from .models import Paciente, Prescricao

class PrescricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescricao
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    prescricoes = PrescricaoSerializer(many=True, read_only=True)

    class Meta:
        model = Paciente
        fields = ['id', 'nome', 'cpf', 'alergias','tipo_sanguineo', 'ativo', 'prescricoes']
