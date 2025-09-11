from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class UserProfile(models.Model):
    # Este modelo extiende el User por defecto de Django para añadir el rol de cada persona que ingrese 
    USER_ROLES = (
        ('buyer', 'Comprador'),
        ('seller', 'Vendedor'),
        ('agent', 'Agente'),
        ('officer', 'Oficial de Escrow'),
        ('lender', 'Prestamista'),
        ('admin', 'Administrador'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    phone_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Transaction(models.Model):
    TRANSACTION_STATUS = (
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('awaiting_signatures', 'Esperando Firmas'),
        ('awaiting_payment', 'Esperando Pago'),
        ('complete', 'Completada'),
        ('cancelled', 'Cancelada'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_transactions')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (${self.amount})"

class Document(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    title = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    requires_signature = models.BooleanField(default=False)
    is_signed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    