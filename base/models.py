from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator # <--- WAJIB IMPORT INI

class CustomUser(AbstractUser):
    # 1. Kita buat aturan validasi baru yang MEMBOLEHKAN SPASI
    # Perhatikan ada spasi di dalam regex: r'^[\w.@+\- ]+$'
    username_validator = RegexValidator(
        regex=r'^[\w.@+\- ]+$', 
        message='Username hanya boleh mengandung huruf, angka, simbol (@/./+/-/_) dan spasi.',
        flags=0
    )

    # 2. Kita timpa field 'username' bawaan dengan aturan baru tadi
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Wajib. 150 karakter atau kurang. Huruf, angka, dan spasi @/./+/-/_ saja.',
        validators=[username_validator], # <--- Pasang validatornya disini
        error_messages={
            'unique': "Username ini sudah digunakan.",
        },
    )

    nik = models.CharField(max_length=16, unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.username


class Pengaduan(models.Model): 
    STATUS_CHOICES = [
        ('menunggu', 'Menunggu'),
        ('proses', 'Dalam Proses'), 
        ('selesai', 'Selesai'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    tanggal_pelaporan = models.DateField()
    isi_laporan = models.TextField()
    gambar_bukti = models.ImageField(upload_to='bukti_laporan/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='menunggu')
    
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Laporan - {self.tanggal_pelaporan} - {self.status}"