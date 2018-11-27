
# A basic python3 framework using Flask Restful.

The idea was to have a project structure with models, controllers and services, a database (using SQLAlchemy), commands, migrations and some basic functionalities like users authentication and authorization (with roles), create users, uploading files and sending emails (not finished yet). 

### There's still a lot of work in progress and things to fix !!


## Proect organization:
```bash
api
 |_ commands: here goes your classes that define a command to execute from the terminal
 |_ common: shared functionality along the application. Services ho here.
 |_ config: configuration files for the application
 |_ migrations: migrations using alembic
 |_ models: Your data models
 |_ resources: Your controllers
 |_ uploads: uploaded files
 |_ app.py: Here is the heart of the api. Here you define your resources and connect to db.
command.py: executes the command manager
main.py: starts the web server
```

Make a file in api/config/config.py with the structure of config.py.dist and generate the migrations. Go to the api/ dir
```bash
cd api
flask db migrate
flask db upgrade

```

Run the dev server:
```bash
cd ..  # you should be where main.py is, in the base folder
python3 main.py
```

### Some curl examples:

Register user
```bash
curl -X POST 'http://127.0.0.1:3000/register' \
-H 'Content-Type: Application/json' \
-H 'accept: application/json' \
-d '{"username":"monstercode", "password":"123456", "email":"monster@code.com"}'
```

Login
```bash
curl -X POST 'http://127.0.0.1:3000/login' \
-H 'Content-Type: Application/json' \
-H 'accept: application/json' \
-d '{"username":"monstercode", "password":"123456"}'
```

Test that jwt is working
```bash
curl  'http://127.0.0.1:3000/jwt-test' \
-H 'Content-Type: Application/json' \
-H 'accept: application/json' \
-H 'Authorization: Bearer <your_access_token>'
```

Upload a file
```bash
curl -X POST 'http://127.0.0.1:3000/uploads'  \
-H 'Content-Type: multipart/form-data'  \
-H 'accept: application/json'  \
-H 'Authorization: Bearer <your_access_token>'  \
-F "file=@/path/to/your/file/my_image.png" \
```

Download the uploaded file
```bash
curl -X GET 'http://127.0.0.1:3000/uploads?filename=<uid_return_by_upload>' \
-H 'accept: application/octet' \
-H 'Authorization: Bearer <your_access_token>'  > my_image.png
```