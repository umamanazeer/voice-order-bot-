# Dockerfile

# Stage 1: Base Image Selection
# FROM instruction Docker ko batati hai ki hum kis base image se shuru kar rahe hain.
# 'python:3.10-slim-buster' ek lightweight (chota size) Python image hai jo Debian Buster Linux par based hai.
# Yeh aapke bot ke liye basic operating system aur Python runtime environment provide karega.
FROM python:3.10-slim-buster

# Stage 2: Environment Setup
# ENV instruction environment variables set karti hai container ke andar.
# PYTHONUNBUFFERED=1: Yeh ensure karta hai ki Python ke print statements (jaise aapke 'print' logs)
# console par dikhen, buffering na ho. Yeh debugging aur logging ke liye acha hai.
ENV PYTHONUNBUFFERED 1

# APP_HOME variable define kar rahe hain jahan hum apni application ko rakhenge container ke andar.
ENV APP_HOME /app
# WORKDIR instruction working directory set karti hai container ke andar.
# Iske baad ke saare commands (COPY, RUN) isi directory mein execute honge.
WORKDIR $APP_HOME

# Stage 3: Dependencies Installation
# COPY instruction 'requirements.txt' file ko current working directory (jo ki /app hai) mein copy karti hai.
# Hum isko pehle copy karte hain taaki Docker ke layer caching ka fayda utha saken.
COPY requirements.txt .

# RUN instruction shell commands ko execute karti hai Docker image banate waqt.
# 'pip install --no-cache-dir -r requirements.txt': Yeh 'requirements.txt' mein listed saari Python libraries install karega.
# '--no-cache-dir' flag disk space bachata hai aur image size ko chota rakhta hai.
RUN pip install --no-cache-dir -r requirements.txt

# Stage 4: Application Code Copying
# COPY . . instruction aapke local project folder ke saare content (jo .dockerignore mein nahi hain) ko
# container ke current working directory (/app) mein copy karti hai.
COPY . .

# Stage 5: Port Exposure
# EXPOSE instruction batati hai ki container kis network port par listen karega.
# Aapki FastAPI application default roop se port 8000 par chalegi.
# Jab yeh container deploy hoga cloud par, toh cloud service is internal port ko ek public port se map kar dega.
EXPOSE 8000

# Stage 6: Container Startup Command
# CMD instruction container ke start hone par kaunsi command execute hogi, yeh specify karti hai.
# Yahan hum Uvicorn (ASGI server) ko apni FastAPI app ko chalanay ke liye keh rahe hain.
# 'main:app': Iska matlab hai 'main.py' file mein 'app' naam ka FastAPI instance.
# '--host 0.0.0.0': Isse Uvicorn container ke andar saari network interfaces se connections accept karega.
# '--port 8000': Uvicorn ko port 8000 par listen karne ko kahega.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]