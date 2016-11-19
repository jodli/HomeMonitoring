FROM alpine:3.1

# Update
RUN apk add --update python py-pip libxml2-dev libxslt-dev build-base

# Copy app to container
ADD $PWD/src /src

# Install app dependencies
RUN pip install -r /src/requirements.txt

# Set default directory
WORKDIR /src

# Start app
CMD python fritzscraper.py
