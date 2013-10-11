# Deployment notes

## Software Stack

The deployed stack for <http://food.hypertexthero.com> consists of the following components running on webfaction:

- [NGINX](http://nginx.org/en/) - public facing web server - serves media and proxies dynamic requests to Gunicorn. Currently using webfactions system-wide nginx.
- [Gunicorn](http://gunicorn.org/ "Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.") - internal HTTP application server
- [PostgreSQL](http://www.postgresql.org/) - database
- [Django](http://djangoproject.com/) web application in Git repository

## Restarting Server After Updates {#restart}

**Note that we will eventually have a [Fabric](http://docs.fabfile.org/en/1.6/) script that will do all of the below with one command. =TODO: Set up Fabric deployment script.**

1. Login to webfaction via SSH

2. Change to the hypertexthero project virtual environment directory, activate the Python virtual environment of the project, change into the project directory:

        cd ~/webapps/foodnews/fn-env/ && . bin/activate && cd fn

3. Find out the number of the Gunicorn process:

        ps aux | grep gunicorn

4. Kill the process gracefully (replace #### with the number from the output above):

        kill -HUP ####

5. If necessary, restart the Gunicorn server:

        python manage.py run_gunicorn --daemon -b 127.0.0.1:17734 -w 2 --max-requests 500


## Deploying Code

1. Login to webfaction via SSH

2. Change to the IT Wishlist project virtual environment directory, activate the Python virtual environment of the project, change into the project directory:

        cd ~/webapps/foodnews/fn-env/ && . bin/activate && cd fn

3. Pull changes from the Github repository master branch:

        git pull origin master

4. Collect static files to static directories in case you changed CSS, JavaScript, site design images, etc (say 'yes' when it asks to overwrite):

        python manage.py collectstatic

5. If you changed Python code, you need to <a href="#restart">restart</a> the server, too. If you only changed code in templates, there is no need to restart.

## Data migrations using South app after changing models

Make sure 'south' is present in your INSTALLED_APPS IN settings.py.

If you add new fields or change certain values of existing ones such as blank or null in the main application, you need to do a data migration to synchronize the database:

1. Everytime you make a change in your models do the following:

    `./manage.py schemamigration your_app --auto`  
    `./manage.py migrate your_app`

2. If you want to rever to a previous migration, look for the previous migration number in ippc/migrations and replace #### with the migration number in the following command:

    `manage.py migrate your_app ####`

## Reverting to Previous Commit in Case You Break Something

1. Login to webfaction via SSH

2. Change to the IT Wishlist project virtual environment directory, activate the Python virtual environment of the project, change into the project directory:

        cd ~/webapps/foodnews/fn-env/ && . bin/activate && cd fn

3. [Find the hash of the previous commit in your repository](http://git-scm.com/book/en/Git-Basics-Viewing-the-Commit-History):

        git log

4. Checkout previous commit from [the Github repository master branch](https://github.com/hypertexthero/hypertexthero.com/commits/master) using [these instructions](http://stackoverflow.com/a/4114122/412329) or the command below:

         git reset --hard HashOfPreviousCommitHereLotsOfNumberAndLetters

5. [Restart server](#restart)

# Cron

This is the cron job to make sure gunicorn is running.
ssh into webfaction account, type ‘crontab -e’ to edit the cron file and append the following to the bottom of the file:

  30 * * * * cd ~/webapps/foodnews/fn-env/ && /webapps/foodnews/fn-env/bin/python /webapps/foodnews/fn-env/hth/manage.py run_gunicorn --daemon -b 127.0.0.1:17734 -w 2 --max-requests 500