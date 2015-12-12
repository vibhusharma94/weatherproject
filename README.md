Weather Monitoring System using wunderground api
===================================================================

1. Dev tools Installations
	* sudo apt-get install build-essential python-dev libevent-dev libxml2-dev libmysqlclient-dev python-setuptools python-pip libpq-dev libxslt1-dev

2. Install Mysql
    * sudo apt-get install mysql-server
    * mysql -u root -p
    * create database weatherdb;
    * sudo service mysql start
    * sudo service mysql stop
   
3. Install Virtualenv
    * pip install virtualenv

4. Virtualenv Setup
    * virtualenv env
    * source bin/activate
    deactivate

5. Install requirements
    * pip install requirements.txt 

6. create tables
   * python manage.py migrate

7. Start Django test server
   * python manage.py runserver 8000
   --------- OR ---------------
   Start Gunicorn
   * pip install gunicorn
   gunicorn weathermonitor.wsgi
   Note. Use nginx to serve static file and as a proxy server with gunicorn

8. Test django app
    * python manage.py test

9. Auto poputale stations date
    * python manage.py shell
    * from apps.apis.weather import service
    * service.auto_populate_station()




    
