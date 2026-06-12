#!/bin/bash

# Fungsi untuk mematikan semua proses dengan bersih saat tombol Ctrl+C ditekan
cleanup() {
    echo -e "\n[INFO] Mematikan server IronWill..."
    kill $TAILWIND_PID
    exit 0
}

# Tangkap sinyal interupsi (Ctrl+C) dan jalankan fungsi cleanup
trap cleanup SIGINT

echo "[INFO] Mengaktifkan Virtual Environment..."
source venv/bin/activate

echo "[INFO] Menyalakan Mesin Tailwind (Background)..."
python manage.py tailwind start &
TAILWIND_PID=$!

echo "[INFO] Menyalakan Mesin Django (Foreground)..."
python manage.py runserver