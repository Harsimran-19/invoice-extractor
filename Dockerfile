FROM ubuntu:16.04
FROM python:3.6.5

# Update and install any additional dependencies if needed
# Example:
# RUN apt-get update && apt-get install -y <package-name>

# Copy requirements.txt and install dependencies
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Specify the command to run the application
CMD ["python", "api.py"]
