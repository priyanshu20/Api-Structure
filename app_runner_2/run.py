from app_structure_2 import create_app

app=create_app()

#for production conventionally a wsgi.py file is create which works similar to this, it serves the app object to a gunicorn server

if __name__ =='__main__':
    app.run()
