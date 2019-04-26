# Create the container from the alpine linux image
FROM python:3-onbuild

RUN pip install -r requirements.txt
COPY . /usr/src/app
CMD ["python", "api.py"]

 