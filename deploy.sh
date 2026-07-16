#!/bin/bash
set -e

echo ""
echo "======================================"
echo "   MasonTrack — Deploy Script"
echo "======================================"
echo ""

# ── 1. Install docker-compose if missing ──
if ! command -v docker-compose &> /dev/null; then
    echo "[1/6] Installing docker-compose..."
    sudo apt-get update -qq
    sudo apt-get install -y docker-compose
else
    echo "[1/6] docker-compose already installed ✓"
fi

# ── 2. Add current user to docker group if needed ──
if ! groups $USER | grep -q docker; then
    echo "[2/6] Adding $USER to docker group..."
    sudo usermod -aG docker $USER
    echo "      NOTE: You may need to log out and back in for this to take effect."
else
    echo "[2/6] User already in docker group ✓"
fi

# ── 3. Stop any existing containers ──
echo "[3/6] Stopping existing containers..."
docker-compose -f docker-compose.yml down --remove-orphans 2>/dev/null || true

# ── 4. Build and start ──
echo "[4/6] Building and starting containers..."
docker-compose -f docker-compose.yml up --build -d

# ── 5. Wait for web to be ready ──
echo "[5/6] Waiting for app to be ready..."
sleep 8
for i in $(seq 1 20); do
    if docker-compose exec -T web python manage.py check --deploy 2>/dev/null | grep -q "no issues"; then
        echo "      App is ready ✓"
        break
    fi
    sleep 3
done

# ── 6. Create superuser if none exists ──
echo "[6/6] Checking superuser..."
docker-compose exec -T web python manage.py shell -c "
from users.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('mason', 'rakitamason@gmail.com', 'mason1234')
    print('Superuser created: username=mason password=mason1234')
else:
    print('Superuser already exists ✓')
"

echo ""
echo "======================================"
echo "   DEPLOYED SUCCESSFULLY"
echo "======================================"
echo ""
echo "  App:    http://localhost"
echo "  Admin:  http://localhost/mt-admin-x9k2/"
echo "  Login:  username=mason  password=mason1234"
echo ""
echo "  Logs:   docker-compose logs -f web"
echo "  Stop:   docker-compose down"
echo ""
