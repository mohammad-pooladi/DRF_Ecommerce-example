## project setup

1- clone project
```shell
git clone https://github.com/mohammad-pooladi/DRF_Ecommerce-example.git
```
```
cd DRF_Ecommerce-example
```

2- SetUp venv
```
virtualenv -p python3.12 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements_dev.txt
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py migrate
```

6- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

7- run the project
```
python manage.py runserver
```