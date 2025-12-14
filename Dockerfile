FROM maven:3.9-eclipse-temurin-21

# ------------------------
# Install system dependencies
# ------------------------
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    x11vnc \
    xvfb \
    fluxbox \
    novnc \
    python3-websockify \
    python3-numpy \
    libgtk-3-0 \
    libglib2.0-0 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxinerama1 \
    libxcursor1 \
    && rm -rf /var/lib/apt/lists/*

# ------------------------
# Set working directory
# ------------------------
WORKDIR /language-proximity-analysis

# ------------------------
# Python dependencies (cached)
# ------------------------
COPY app/requirements.txt app/requirements.txt
RUN pip3 install -r app/requirements.txt --break-system-packages

# ------------------------
# Maven dependencies (cached)
# ------------------------
COPY gui/pom.xml gui/pom.xml
RUN mvn -f gui/pom.xml dependency:go-offline

# ------------------------
# Application code
# ------------------------
COPY app app
COPY gui/src gui/src

# Build GUI
RUN mvn -f gui/pom.xml clean package -DskipTests

# ------------------------
# Runtime
# ------------------------
COPY data data

# Entry point
RUN echo '#!/bin/bash\n\
echo "=== Step 1: Running Analysis Pipeline ==="\n\
python3 app/pipeline.py || exit 1\n\
\n\
echo "=== Step 2: Starting GUI Server ==="\n\
rm -f /tmp/.X11-unix/X0\n\
export DISPLAY=:0\n\
Xvfb :0 -screen 0 1024x768x16 &\n\
sleep 1\n\
fluxbox &\n\
x11vnc -display :0 -forever -nopw -quiet -listen localhost -xkb &\n\
websockify --web /usr/share/novnc/ 6080 localhost:5900 &\n\
\n\
# Run JavaFX GUI via Maven\n\
mvn -f gui/pom.xml javafx:run -Djavafx.platform=linux\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

# Expose NoVNC port
EXPOSE 6080

CMD ["/entrypoint.sh"]
