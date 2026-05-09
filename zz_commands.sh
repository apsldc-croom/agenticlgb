git add .
git commit -m "frontend pm is working but need to lot added"
git push origin main

cd LGB-frontend
npm run dev


cd LGB-backend
source env/Scripts/activate
python manage.py runserver

py manage.py createsuperuser