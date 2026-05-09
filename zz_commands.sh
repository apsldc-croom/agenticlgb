git add .
git commit -m "frotnend pm added and need to be checked"
git push origin main

cd LGB-frontend
npm run dev


source env/Scripts/activate
cd LGB-backend
python manage.py runserver

py manage.py createsuperuser