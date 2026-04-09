#!/usr/bin/env bash
# By using env, the script will work as long as bash is available in the user's PATH, making it more flexible and suitable for use in various environments.

# This option makes the script exit immediately if any command within the script returns a non-zero status (indicating failure).
# It helps prevent the script from continuing to execute subsequent commands after an error has occurred, which can be useful for debugging and ensuring that the script does not perform unintended actions.
set -o errexit

# This option makes the script exit with an error if it attempts to use an uninitialized variable.
# It helps catch typos and mistakes where variables might be misspelled or not set properly before being used.
set -o nounset

# This option ensures that the exit status of a pipeline (a series of commands connected by pipes) is the exit status of the last command in the pipeline to return a non-zero status, rather than the default behavior, which is to return the status of the last command.
# It is particularly useful for catching errors in complex pipelines where the failure of any command in the pipeline should cause the entire pipeline to fail.
set -o pipefail


: "${DB_HOST:=maktabiya-db}"
: "${DB_PORT:=3306}"


# We need this line to make sure that DB is reachable
wait-for-it \
  --host="$DB_HOST" \
  --port="$DB_PORT" \
  --timeout=90 \
  --strict

# It is also possible to wait for other services as well: redis, elastic, mongo
echo "Maktabiya DB ${DB_HOST}:${DB_PORT} is UP"

# Wait for the database to be ready
python manage.py wait_for_db

# Get the current hostname
hostname=$(hostname)
#echo $hostname
# Check if the hostname contains "maktabiya-app"
# run only in the backend app not in the task
if [[ $hostname == *"maktabiya-app"* ]]; then
    echo "Collecting static files and images..."
    python manage.py collectstatic --noinput &&
    chown -R maktabiya:maktabiya '/app/static_root_dir'
    #sleep 31 &&
    echo "Migration stuffs doing..." &&
    python manage.py makemigrations && 
    python manage.py migrate
    if [ "$CREATE_DEFAULT_ADMIN" = "True" ]; then
        echo "Checking if superuser ${DJANGO_SUPERUSER_USERNAME} exists"
        if ! python manage.py check_user_exists "${DJANGO_SUPERUSER_USERNAME}"; then
            echo "Creating superuser ${DJANGO_SUPERUSER_USERNAME}..."
            python manage.py createsuperuser \
                --noinput \
                --username "$DJANGO_SUPERUSER_USERNAME" \
                --email "$DJANGO_SUPERUSER_EMAIL"
        fi
    fi
fi
# app start is handled by honcho with procfile
# "$@"
# Evaluating passed command (do not touch):
readonly cmd=("$@")  # Store all arguments in an array
exec "${cmd[@]}"  # Expand array elements as separate arguments