FROM kennethreitz/pipenv
ENV PORT '80'
COPY . /app
CMD python3 main.py
EXPOSE 80
