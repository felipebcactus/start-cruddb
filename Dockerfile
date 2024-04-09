FROM python:3.9-slim

WORKDIR /app

# RUN python3 -m venv .env
# RUN . .env/bin/activate
# ENV PATH="/env/bin:$PATH"

RUN apt-get update && apt-get install -y pkg-config
RUN python3 -m pip install --upgrade pip
RUN pip install Flask SQLAlchemy flask-sqlalchemy flask-bootstrap wtforms PyMySQL gunicorn Werkzeug Flask-WTF python-dotenv

COPY . ./
COPY .env /app/

RUN pip install -r ./requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "cruddb:app"]
