FROM python:3.9-slim

# Çalışma dizinini oluştur
WORKDIR /app

# Gereksinimleri kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Botu çalıştır
CMD ["python", "-u", "background_monitor.py"]
