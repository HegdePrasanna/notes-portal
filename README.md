# Notes Portal
Welcome to the Notes Portal, a Django REST application for managing your notes.

## Swagger Documentation
The APIs are deployed on AWS and can be accessed using [this link](http://15.207.84.124:8000/api/docs/)
```bash
http://15.207.84.124:8000/api/docs/
```

## How to Run in Local Machine
To clone this repository, use the following command:
```bash
git clone https://github.com/HegdePrasanna/notes-portal.git
```
```bash
cd notes_management
```
Create Anaconda Environment
```bash
conda env create -f environment.yml
```
Migrate Changes to Database
```bash
python manage.py makemigrations
python manage.py migrate
```
Create a superuser
```bash
python manage.py createsuperuser
```
Run the APIs
```bash
python manage.py runserver
```

## Features
1. Users can register themselves
2. Authenticated users can create notes
3. Authorized users (owner of the note) can share the note with other existing users with proper permissions.
4. Authorized users can read, edit and delete notes.
5. Every modification to the note is logged in version history
