## API for AirBnB_clone_v3

**3-Status of your API**
It’s time to start your API!

Your first endpoint (route) will be to return the status of your API:

guillaume@ubuntu:~/AirBnB_v3$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
...

In another terminal:

guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/status
{
  "status": "OK"
}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET -s http://0.0.0.0:5000/api/v1/status -vvv 2>&1 | grep Content-Type
< Content-Type: application/json
guillaume@ubuntu:~/AirBnB_v3$ 

Magic right? (No need to have a pretty rendered output, it’s a JSON, only the structure is important)

Ok, let starts:

    Create a folder api at the root of the project with an empty file __init__.py
    Create a folder v1 inside api:
        create an empty file __init__.py
        create a file app.py:
            create a variable app, instance of Flask
            import storage from models
            import app_views from api.v1.views
            register the blueprint app_views to your Flask instance app
            declare a method to handle @app.teardown_appcontext that calls storage.close()
            inside if __name__ == "__main__":, run your Flask server (variable app) with:
                host = environment variable HBNB_API_HOST or 0.0.0.0 if not defined
                port = environment variable HBNB_API_PORT or 5000 if not defined
                threaded=True
    Create a folder views inside v1:
        create a file __init__.py:
            import Blueprint from flask doc
            create a variable app_views which is an instance of Blueprint (url prefix must be /api/v1)
            wildcard import of everything in the package api.v1.views.index => PEP8 will complain about it, don’t worry, it’s normal and this file (v1/views/__init__.py) won’t be check.
        create a file index.py
            import app_views from api.v1.views
            create a route /status on the object app_views that returns a JSON: "status": "OK" (see example)


**4-Some stats?**
Create an endpoint that retrieves the number of each objects by type:

    In api/v1/views/index.py
    Route: /api/v1/stats
    You must use the newly added count() method from storage

**5-Not found**
Designers are really creative when they have to design a “404 page”, a “Not found”… 34 brilliantly designed 404 error pages

Today it’s different, because you won’t use HTML and CSS, but JSON!

In api/v1/app.py, create a handler for 404 errors that returns a JSON-formatted 404 status code response. The content should be: "error": "Not found"

