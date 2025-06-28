FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl ca-certificates fonts-liberation libnss3 libxss1 \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libx11-xcb1 libgtk-3-0 \
    libgbm1 libxcomposite1 libxdamage1 libxrandr2 libxext6 libxfixes3 \
    libpci3 libxinerama1 libxkbcommon0 libdrm2 libxshmfence1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Installer Python libs
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer les navigateurs Playwright
RUN python -m playwright install --with-deps

# Copier le reste du code
COPY . .

# Exposer le port automatiquement fourni par Render
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:${PORT}", "main:app"]
