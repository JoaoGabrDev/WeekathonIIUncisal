from django.db import models

class Paciente(models.Model):
    TIPO_SANGUINEO_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    alergias = models.TextField(blank=True)
    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=TIPO_SANGUINEO_CHOICES,
        blank=True,
        null=True
    )
    ativo = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.cpf}"


class Prescricao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="prescricoes")
    medicamento = models.CharField(max_length=100)
    dosagem = models.CharField(max_length=50)
    frequencia = models.CharField(max_length=50)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medicamento} ({self.dosagem})"

