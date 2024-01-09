
# Use a minimal Python 3 image
FROM python:3-alpine

# Create necessary directories
RUN mkdir -p /data /app/bin

# Copy the code into the container
COPY code /app/bin/

RUN pip install requests simplejson

# Set the working directory
WORKDIR /app/bin/

# Set environment variables for API key and location
ENV API_KEY=fd3a41ccb4f3d1242381c0d007883e4d
ENV LOCATION=Omaha

# Specify the entrypoint script

ENTRYPOINT python3 /app/bin/weather.py $API_KEY $LOCATION