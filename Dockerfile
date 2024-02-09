FROM python:3
# Ensure realtime, unbuffered Python output to stdout, stderr
ENV PYTHONUNBUFFERED 1
# Create /app dir to house django project & app
RUN mkdir /app
# Change working directory to /app
WORKDIR /app
# Copy requirements file
COPY requirements.txt /app/
# Install dependencies from requirements
RUN pip install -r requirements.txt
# Copy local project root dir contents to /app
COPY . /app/
