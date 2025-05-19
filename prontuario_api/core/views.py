from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Paciente, Prescricao
from .serializers import PacienteSerializer
from .utils import gerar_qrcode

@api_view(['GET'])
def gerar_qr_paciente(request, cpf):
    try:
        paciente = Paciente.objects.get(cpf=cpf, ativo=True)
        serializer = PacienteSerializer(paciente)
        qr_code_base64 = gerar_qrcode(str(serializer.data))
        return Response({
            "qr_code_base64": qr_code_base64,
            "paciente": serializer.data
        })
    except Paciente.DoesNotExist:
        return Response({"erro": "Paciente não encontrado ou inativo."}, status=404)

@csrf_exempt
@api_view(['POST'])
def cadastrar_gerar_qr(request):
    # Copia os dados para retirar a prescrição antes de serializar o paciente
    data = request.data.copy()
    presc = data.pop('prescricao', None)

    # Valida e salva o paciente
    serializer = PacienteSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    paciente = serializer.save()

    # Cria a prescrição vinculada, se tiver vindo no JSON
    if presc:
        Prescricao.objects.create(
            paciente=paciente,
            medicamento=presc.get('medicamento', ''),
            dosagem=presc.get('dosagem', ''),
            frequencia=presc.get('frequencia', ''),
            observacoes=presc.get('observacoes', '')
        )

    # Re-serializa para incluir a prescrição recém-criada
    final_serializer = PacienteSerializer(paciente)
    qr_code_base64 = gerar_qrcode(str(final_serializer.data))

    return Response({
        "paciente": final_serializer.data,
        "qr_code_base64": qr_code_base64
    })

@api_view(['POST'])
def dar_alta(request, cpf):
    try:
        paciente = Paciente.objects.get(cpf=cpf, ativo=True)
        paciente.ativo = False
        paciente.save()
        return Response({"mensagem": "Paciente recebeu alta com sucesso."})
    except Paciente.DoesNotExist:
        return Response({"erro": "Paciente não encontrado ou já está inativo."}, status=404)

def home(request):
    return render(request, 'index.html') 