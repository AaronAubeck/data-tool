FROM python:3.7-slim

# copy across script dependent pip install requirements
COPY ./development/requirements.txt /opt/python/requirements/requirements.txt

# create dir for scripts
RUN mkdir /opt/scripts/
# copy across Python scripts
COPY ./development/scripts/main.py /opt/scripts/main.py

# Install requirements
RUN pip install -r /opt/python/requirements/requirements.txt

# Default execute script
CMD ["/opt/scripts/main.py"]
ENTRYPOINT ["python"]
