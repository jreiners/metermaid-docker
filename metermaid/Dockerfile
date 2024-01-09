
# Use a minimal Python 3 image
FROM python:3-alpine

# Install necessary packages
RUN apk --update add --no-cache \
    rtl-sdr \
    go \
    wget

# Create necessary directories
RUN mkdir -p /projects /app/bin /data

# Set environment variables for Go
ENV GOROOT=/usr/lib/go
ENV GOPATH=/projects
ENV PATH=$GOPATH/bin:$GOROOT/bin:$PATH:/app/bin

# Install rtlamr
RUN go install github.com/bemasher/rtlamr@latest

# Copy the code into the container
COPY code /app/bin/


# Set the working directory
WORKDIR /app/bin/

# Specify the entrypoint script

ENTRYPOINT ["python3", "/app/bin/metermaid.py"]
