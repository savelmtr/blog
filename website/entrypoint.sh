#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

./manage.py flush --no-input
./manage.py migrate
./manage.py shell <<EOF
from django.contrib.auth import get_user_model
from blog.models import RootPage, BlogPage
from wagtail.core.models import Page, Site
from datetime import datetime
from django.utils import timezone

User = get_user_model();

User.objects.create_superuser('admin', '', 'admin')

r = RootPage(title='Test Blog', subtitle="Just 'cause we can")
root = Page.objects.get(id=1).specific
root.add_child(instance=r)
r.save()
r.save_revision().publish()

site = Site.objects.get(id=1)
site.root_page = r
site.save()

posts = [
	{"title": 'Man must explore, and this is exploration at its greatest',
	 "subtitle": "Problems look mighty small from 150 miles up",
	 "date": timezone.make_aware(datetime(2019, 9, 24)),
	},
	{"title": 'I believe every human has a finite number of heartbeats. I don\'t intend to waste any of mine.',
	 "subtitle": "",
	 "date": timezone.make_aware(datetime(2019, 9, 18)),
	},
	{"title": 'Science has not yet mastered prophecy',
	 "subtitle": "We predict too much for the next year and yet far too little for the next ten.",
	 "date": timezone.make_aware(datetime(2019, 8, 24)),
	},
	{"title": 'Failure is not an option',
	 "subtitle": "Many say exploration is part of our destiny, but it’s actually our duty to future generations.",
	 "date": timezone.make_aware(datetime(2019, 7, 8)),
	},
]
for p in posts:
	b = BlogPage(title=p["title"], subtitle=p["subtitle"], date=p["date"])
	r.add_child(instance=b)
	b.save()
	b.save_revision().publish()

EOF

exec "$@"