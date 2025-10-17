FROM public.ecr.aws/docker/library/python:3.13
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PYTHONPATH=/app
ENV SQLALCHEMY_DATABASE_URI=postgresql://postgres:<password>@<host>:5432/blacklists
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.app:app"]
