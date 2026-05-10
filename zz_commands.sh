git add .
git commit -m "pm dashboard little bit improved"
git push origin main

cd LGB-frontend
npm run dev


cd LGB-backend
source env/Scripts/activate
python manage.py runserver

py manage.py createsuperuser