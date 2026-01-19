from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required, user_passes_test 
from datetime import datetime
from .forms import UserRegisterForm, LoginForm, PengaduanForm 
from .models import Pengaduan, ChatLaporan

# --- Helper Function ---
def is_admin(user):
    return user.is_staff or user.is_superuser

# --- Public Views ---
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
        {'number': 1, 'title': 'Daftar Akun', 'description': 'Buat akun gratis untuk mulai menggunakan layanan kami.'},
        {'number': 2, 'title': 'Kirim Laporan', 'description': 'Isi formulir laporan dengan detail lengkap dan kirimkan.'},
        {'number': 3, 'title': 'Pantau Status', 'description': 'Lacak perkembangan laporan Anda secara real-time.'},
    ]

    context = {
        'current_year': datetime.now().year,
        'stats': stats_data,
        'features': features_data,
        'steps': steps_data,
    }
    return render(request, 'index.html', context)

# --- Authentication Views ---
def masuk(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user) 
            # Jika admin masuk, arahkan ke dashboard admin, jika user ke halaman lapor
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('laporan') 
        else:
            messages.error(request, "Username atau password salah!")
            
    return render(request, 'masuk.html')

def daftar(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akun berhasil dibuat, silakan login.")
            return redirect('masuk')
    else:
        form = UserRegisterForm()
    return render(request, 'daftar.html', {'form': form})

def keluar(request):
    logout(request)
    return redirect('beranda')

# --- User Views ---
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
    laporan_list = Pengaduan.objects.filter(user=request.user).order_by('-dibuat_pada')
    return render(request, 'my laporan.html', {'laporan_list': laporan_list})

# --- Fitur Chat & Detail ---
@login_required
def detail_laporan(request, laporan_id):
    laporan_obj = get_object_or_404(Pengaduan, id=laporan_id)
    
    # Keamanan: Hanya pemilik atau Admin yang bisa melihat
    if not request.user.is_staff and laporan_obj.user != request.user:
        messages.error(request, "Akses dilarang.")
        return redirect('laporan_saya')

    chats = laporan_obj.chats.all().order_by('dikirim_pada')

    if request.method == "POST":
        pesan_teks = request.POST.get('pesan')
        file_gambar = request.FILES.get('foto')

        if pesan_teks or file_gambar:
            ChatLaporan.objects.create(
                pengaduan=laporan_obj,
                pengirim=request.user,
                pesan=pesan_teks,
                file_pendukung=file_gambar
            )

            # Logika Status Otomatis oleh Admin
            if request.user.is_staff:
                if file_gambar:
                    laporan_obj.status = 'selesai'
                else:
                    laporan_obj.status = 'proses'
                laporan_obj.save()

            messages.success(request, "Pesan terkirim.")
            return redirect('detail_laporan', laporan_id=laporan_id)

    return render(request, 'detail_laporan.html', {'laporan': laporan_obj, 'chats': chats})

# --- Admin Views ---
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
        messages.success(request, "Status laporan berhasil diperbarui.")
    return redirect('admin_dashboard')