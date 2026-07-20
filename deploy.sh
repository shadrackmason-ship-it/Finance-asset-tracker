#!/bin/bash
set -e

echo ""
echo "======================================"
echo "   MasonTrack — Deploy Script"
echo "======================================"
echo ""

# 1. Check docker is available
if ! command -v docker &> /dev/null; then
    echo "[1/6] Installing docker..."
    sudo apt-get update -qq
    sudo apt-get install -y docker.io docker-compose-plugin
else
    echo "[1/6] Docker already installed"
fi

# 2. Add current user to docker group if needed
if ! groups $USER | grep -q docker; then
    echo "[2/6] Adding $USER to docker group..."
    sudo usermod -aG docker $USER
    echo "      NOTE: Log out and back in for this to take effect."
else
    echo "[2/6] User already in docker group"
fi

# 3. Stop existing containers
echo "[3/6] Stopping existing containers..."
docker compose down --remove-orphans 2>/dev/null || true

# 4. Build and start all services
echo "[4/6] Building and starting containers..."
docker compose up --build -d

# 5. Wait for backend to be ready
echo "[5/6] Waiting for backend to be ready..."
sleep 10
for i in $(seq 1 20); do
    if docker compose exec -T backend python manage.py check 2>/dev/null | grep -q "no issues"; then
        echo "      Backend is ready"
        break
    fi
    sleep 3
done

# 6. Create superuser if none exists
echo "[6/6] Checking superuser..."
docker compose exec -T backend python manage.py shell -c "
from users.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('mason', 'admin@masontrack.com', 'ChangeMe123!')
    print('Superuser created: username=mason password=ChangeMe123!')
else:
    print('Superuser already exists')
"

echo ""
echo "======================================"
echo "   DEPLOYED SUCCESSFULLY"
echo "======================================"
echo ""
echo "  App:   http://localhost"
echo "  Logs:  docker compose logs -f backend"
echo "  Stop:  docker compose down"
echo ""
