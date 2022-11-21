# local deploy project
docker compose stop
docker compose rm web -f
docker image rm infra_web
docker compose up -d 
docker compose exec web python manage.py migrate
docker compose exec web python manage.py loaddata
docker compose exec web python manage.py collectstatic --no-input 

# local debug
docker compose stop
docker compose up