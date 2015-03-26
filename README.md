## Bookshelf

A web app for tracking one's reading. Written in Django.

### Installation

These installation instructions assume some basic knowledge of Django.

- Clone the repo
- Create a virtualenv for the project if you want
- Copy `local_settings_sample.py` to `local_settings.py` and edit to taste (and make sure you put something in `SECRET_KEY`)
- `pip install -r requirements.txt`
- `./manage.py migrate`
- `./manage.py createsuperuser`
- `./manage.py runserver 8001`

### Keyboard shortcuts

- `/` to focus on the search box
- `h` to return to the dashboard
- `a` to add a book
