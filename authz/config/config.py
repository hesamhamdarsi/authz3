from os import environ

class AuthConfig:
    ENV = environ.get("AUTHZ_ENV" , "development")
    DEBUG = bool(environ.get("AUTHZ_DEBUG" , False))
    TESTING = bool(environ.get("AUTHZ_TESTING" , False))
    #through this we make our connection stream to database. it could be any database
    #for mysql we need to use this:
    #export AUTHZ_DATABASE_URL=mysql+pymysql://authz:authz@localhost:3306/authz
    #this means:
    #export AUTHZ_DATABASE_URL=DB_type+Driver://user:password@localhost:3306/DB_name
    SQLALCHEMY_DATABASE_URI = environ.get("AUTHZ_DATABASE_URI" , None)  #if didn't set, retrun None which means dtabase is not set
    #this value if to show errors on STDOUT (if its true), so we assign DEBUG to it, why?
    #because we want if we are in production env (ENV=TRUE) we see the logs, otherwise, do not
    SQLALCHEMY_ECHO = DEBUG  
    SQLALCHEMY_TRACK_MODIFICATIONS = DEBUG     #too see the changes that we have on objects 

    JWT_TOKEN_LIFETIME = int(environ.get("AUTHZ_JWT_TOKEN_LIFETIME" , 100))
    SECRET = environ.get("AUTH_SECRET" , "Hard-secret")