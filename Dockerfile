FROM python:3.10

# İş qovluğu - manage.py-nin olduğu yerdə qurulmalıdır
WORKDIR /app/moviepro

# requirements.txt əlavə et və quraşdır
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# bütün layihəni konteynerə kopyala
COPY . .

# port aç
EXPOSE 8000

# container start zamanı işləyəcək komanda
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
