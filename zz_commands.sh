#pushing the changes to cloud
git add .
git commit -m "docker setup in progress CI/CD seems done now"
git push origin main



#finally running the server
cd LGB-frontend
npm run dev

#running backend
cd LGB-backend
source env/Scripts/activate
python manage.py runserver
py manage.py createsuperuser

#first time cloud server setup
ssh usr_789spr_gmail_com@34.93.126.189

sudo apt update && sudo apt upgrade -y
sudo apt install git curl unzip -y
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
exit
# Clone the repo on the VM
git clone https://github.com/apsldc-croom/agenticlgb.git /opt/agenticlgb
cd /opt/agenticlgb

# Fill in secrets
cp .env.prod .env.prod.local   # edit with real values

# Start the full stack
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Run migrations + create superuser
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser


#
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "SELECT datname FROM pg_database WHERE datname='lgb';"


# ============================================================
# GITHUB ACTIONS CI/CD SETUP (run ONCE on VM to generate SSH key)
# ============================================================

# STEP 1 — On the VM, generate a deploy SSH key (no passphrase)
ssh usr_789spr_gmail_com@34.93.126.189
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions -N ""
# Add public key to authorized_keys so Actions can SSH in
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
# Print private key — copy this into GitHub Secret VM_SSH_KEY
cat ~/.ssh/github_actions

# STEP 2 — Add these 3 secrets in GitHub:
# Repo → Settings → Secrets and variables → Actions → New repository secret
#   VM_HOST = 34.93.126.189
#   VM_USER = usr_789spr_gmail_com
#   VM_SSH_KEY = (paste the private key printed above)

# STEP 3 — On VM, clone repo and create .env.prod
ssh usr_789spr_gmail_com@34.93.126.189
sudo git clone https://github.com/apsldc-croom/agenticlgb.git /opt/agenticlgb
sudo chown -R usr_789spr_gmail_com:usr_789spr_gmail_com /opt/agenticlgb
cd /opt/agenticlgb
cp .env.prod .env.prod.bak
nano .env.prod   # fill in DJANGO_SECRET_KEY, POSTGRES_PASSWORD etc.

# STEP 4 — First manual deploy (bootstrap)
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
# Verify
curl http://34.93.126.189/api/health/

# STEP 5 — After that, every git push to main auto-deploys via GitHub Actions
# 1. On VM — generate deploy SSH key
ssh usr_789spr_gmail_com@34.93.126.189
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions -N ""
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
cat ~/.ssh/github_actions   # copy this

# 2. Add 3 secrets in GitHub repo → Settings → Secrets → Actions
#   VM_HOST = 34.93.126.189
#   VM_USER = usr_789spr_gmail_com
#   VM_SSH_KEY = (paste private key)

# 3. Clone repo + fill .env.prod on VM, then first manual deploy


ssh usr_789spr_gmail_com@34.93.126.189

# Bootstrap (first time only)
sudo git clone https://github.com/apsldc-croom/agenticlgb.git /opt/agenticlgb
sudo chown -R $USER:$USER /opt/agenticlgb
cd /opt/agenticlgb

# Set secret key (only thing you MUST change in .env.prod)
nano .env.prod
# → change DJANGO_SECRET_KEY to a real 50-char random string

# Start stack
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate
curl http://34.93.126.189/api/health/
