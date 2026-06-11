⚔️ IronWill

"Tempa Kebiasaanmu, Bangun Legenda."

📜 Tentang IronWill

IronWill bukanlah habit tracker biasa. Ini adalah proyek SaaS (Software as a Service) sumber terbuka (Open-Core) yang menggabungkan manajemen produktivitas tingkat lanjut dengan mekanik hardcore RPG.

Berhenti melihat tugas harian sebagai beban. Di IronWill, kehidupan nyatamu adalah dunia game yang kejam namun penuh reward. Selesaikan quest, kumpulkan Gold, bangun Skill Tree, pelajari sihir secara RNG, dan bangun tempat berlindungmu sendiri. Namun hati-hati, kemalasan akan menguras Health Points (HP) karaktermu dan membawa konsekuensi fatal.

✨ Fitur Utama

🛠️ 1. Manajemen Quest Multi-Format (Productivity Engine)

Pilih gaya manajemen tugas yang paling cocok untuk otakmu. IronWill mendukung 8 format rendering tugas yang bisa diganti kapan saja:

✅ To-Do List Klasik

📋 Kanban Board

📥 Inbox / GTD Pipeline

🌳 Hierarchical Outliner / Infinite Tree

📊 Gantt Chart / Timeline

🟩 Grid Heatmap (Seinfeld Method)

📅 Time-Blocking / Calendar View

⚖️ Eisenhower Matrix

⚔️ 2. Mekanik RPG & Gamifikasi Hardcore

Sistem Status & Class: Pilih class awalmu dan tingkatkan status (STR, INT, AGI) melalui penyelesaian kebiasaan di dunia nyata.

Skill Tree & RNG Magic: Dapatkan skill pasif dan pelajari sihir secara acak (RNG) dari penyelesaian quest tingkat tinggi.

Punishment System: Kehilangan konsistensi (streak) akan memberikan damage pada HP karaktermu.

🏰 3. Ekonomi, Companions & Housing

Gold & Shop: Gunakan Gold hasil produktivitas untuk membeli reward kustom di dunia nyata atau item in-game.

Inventory & Equipment: Kumpulkan armor dan senjata untuk memperkuat status.

Pets & Mounts: Temukan dan rawat pendamping yang akan memberikan buff pasif.

Housing System: Beli dan hias rumah virtualmu sendiri sebagai simbol kesuksesan produktivitas.

🌍 4. Fitur Sosial & Leaderboard

Papan peringkat berdasarkan wilayah (Region) hingga skala Global.

Sistem Challenge komunitas (misal: "Selesaikan 100 Quest di Bulan Ini").

🏗️ Tech Stack

IronWill dibangun menggunakan arsitektur Monolith modern yang tangguh dan mudah dikembangkan:

Backend Engine: Python, Django 5.x

Database: PostgreSQL (Production) / SQLite (Development)

Frontend / UI: Django Templates, Tailwind CSS, DaisyUI

Arsitektur: Micro-Apps Structure (accounts, quests, rpg_engine, economy, social).

🚀 Panduan Instalasi (Development)

Panduan ini ditujukan untuk lingkungan Linux (Disarankan: EndeavourOS, Arch, Ubuntu).

Prasyarat

Pastikan sistem Anda sudah terpasang:

Python 3.10+

PostgreSQL

Node.js & npm (untuk proses build Tailwind CSS)

Langkah-langkah Setup

Kloning Repositori

git clone [https://github.com/username-kamu/IronWill.git](https://github.com/username-kamu/IronWill.git)
cd IronWill


Buat Virtual Environment & Install Dependencies

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Konfigurasi Environment
Salin file contoh konfigurasi dan isi dengan kredensial database lokalmu.

cp .env.example .env


Migrasi Database

python manage.py migrate


Setup Tailwind CSS
Masuk ke direktori theme dan install dependensi Node.js.

python manage.py tailwind install


Jalankan Server Development
Kamu butuh dua terminal.

Terminal 1 (Build CSS Tailwind secara real-time):

python manage.py tailwind start


Terminal 2 (Menjalankan server Django):

python manage.py runserver


Akses aplikasi di http://127.0.0.1:8000. Akses panel Admin di /forge-control/.

⚖️ Lisensi

IronWill (Web version) didistribusikan di bawah lisensi GNU AGPLv3.
Anda bebas menggunakan, memodifikasi, dan mendistribusikan perangkat lunak ini asalkan modifikasi yang berjalan di jaringan/web juga bersifat open-source.

Dibuat dengan ❤️ oleh Saeful Risqi.