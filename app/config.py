import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'     # Flask-WTF uses it to protect from CSRF

    WTF_CSRF_SECRET_KEY = SECRET_KEY

    os.environ[
        "DATABASE_URL"] = "postgres://buuzvdtusoaaqi:339ae0c9ab3a80f649353d13207687b6cbc5be855ccdb3ef55f3d66a74e8" \
                          "99d6@ec2-174-129-231-100.compute-1.amazonaws.com:5432/d9fmk2vkh5brl6"


    # Check for environment variable
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


