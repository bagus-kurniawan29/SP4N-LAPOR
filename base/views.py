from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required, user_passes_test 
from datetime import datetime
from .forms import UserRegisterForm, LoginForm, PengaduanForm 
from .models import Pengaduan


def is_admin(user):
    return user.is_staff or user.is_superuser



def beranda(request):
    stats_data = [
        {'value': '1.568', 'label': 'Laporan Diterima'},
        {'value': '1.245', 'label': 'Laporan Ditindaklanjuti'},
        {'value': '20', 'label': 'Instansi Terlibat'},
        {'value': '90%', 'label': 'Tingkat Kepuasan'},
    ]
    
    features_data = [
        {
            'icon_path': 'M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122',
            'title': 'Mudah Digunakan', 
            'description': 'Antarmuka yang intuitif untuk semua kalangan.',
            'color': 'blue-600',
        },
        {
            'icon_path': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
            'title': 'Aman & Terpercaya', 
            'description': 'Data Anda dilindungi dengan standar keamanan tinggi.',
            'color': 'yellow-600',
        },
        {
            'icon_path': 'M13 10V3L4 14h7v7l9-11h-7z',
            'title': 'Responsif', 
            'description': 'Tindak lanjut cepat dari instansi terkait.',
            'color': 'red-600',
        },
    ]
    steps_data = [
        {'number': 1, 'title': 'Daftar Akun', 'description': 'Buat akun untuk mulai mengirim laporan.'},
        {'number': 2, 'title': 'Kirim Laporan', 'description': 'Isi formulir laporan dengan detail yang jelas.'},
        {'number': 3, 'title': 'Tindak Lanjut', 'description': 'Pantau status laporan Anda secara real-time.'},
    ]
    hilmi_pengaduan_data =[
         {
            'title': 'Jalan Rusak di Depan Sekolah',
            'description': 'Jalan di depan SDN 01 rusak parah, membahayakan siswa yang berangkat sekolah.',
            'image_url': 'https://example.com/images/jalan_rusak.jpg',
            'status': 'Dalam Proses',
         },
        {
                'title': 'Lampu Jalan Mati',
                'description': 'Lampu jalan di komplek perumahan kami sering mati, rawan kecelakaan.',
                'image_url': 'https://example.com/images/lampu_jalan.jpg',
                'status': 'Selesai',
        },
        {
                'title': 'Sampah Menumpuk di Taman Kota',
                'description': 'Taman kota tidak terawat, banyak sampah berserakan yang mengganggu kenyamanan warga.',
                'image_url': 'https://example.com/images/taman_sampah.jpg',
                'status': 'Menunggu',
        }
     ]
    
    context = {
        'current_year': datetime.now().year,
        'stats': stats_data,
        'features': features_data,
        'hilmi_pengaduan': hilmi_pengaduan_data,
        'steps': steps_data,
    }
    return render(request, 'index.html', context)


def masuk(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user) 
            return redirect('laporan') 
        else:
            messages.error(request, "Username atau password salah!")
            
    return render(request, 'masuk.html')

def daftar(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('masuk')
    else:
        form = UserRegisterForm()

    return render(request, 'daftar.html', {'form': form})


def keluar(request):
    logout(request)
    return redirect('beranda')

@login_required
def laporan(request):
    if request.method == 'POST':
        form = PengaduanForm(request.POST, request.FILES)
        if form.is_valid():
            laporan_obj = form.save(commit=False)
            laporan_obj.user = request.user 
            laporan_obj.save()
            messages.success(request, "Laporan berhasil dikirim!")
            return redirect('laporan_saya') 
    
    
    return render(request, 'lapor.html')

@login_required
def laporan_saya(request):
    laporan_user = Pengaduan.objects.filter(user=request.user).order_by('-dibuat_pada')
    
    context = {
        'laporan_list': laporan_user,
    }
    return render(request, 'my laporan.html', context) 

@user_passes_test(is_admin) 
def admin_dashboard(request):
    laporan_list = Pengaduan.objects.all().order_by('-dibuat_pada')
    return render(request, 'admin_dashboard.html', {'laporan_list': laporan_list})

@user_passes_test(is_admin)
def update_status(request, laporan_id):
    if request.method == "POST":
        laporan_obj = get_object_or_404(Pengaduan, id=laporan_id)
        status_baru = request.POST.get('status')
        laporan_obj.status = status_baru
        laporan_obj.save()
    return redirect('admin_dashboard')