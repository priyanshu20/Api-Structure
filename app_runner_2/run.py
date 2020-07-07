from app_structure_2 import create_app

app=create_app()
#During product a wsgi.py file is created similar to this which is server to gunicorn etc.
if __name__ =='__main__':
    app.run()
