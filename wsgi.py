from hello import app as application #uwsgi expects a variable called application

if __name__ == "__main__":
    application.run()
