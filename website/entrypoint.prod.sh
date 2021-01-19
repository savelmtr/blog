#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

touch /home/app/web/staticfiles/robots.txt
cat <<EOF > /home/app/web/staticfiles/robots.txt
# Common rules
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /django-admin/
Disallow: /search/
Disallow: /api/

Sitemap: $BASE_URL/sitemap.xml
EOF
exec "$@"