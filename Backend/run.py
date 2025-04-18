from app import create_app

app, celery = create_app()

if __name__ == '__main__':
    app.run(port=4243,debug=True)