FROM python:3.6-slim-jessie

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
# ENTRYPOINT ["python3", "app.py"]
ENTRYPOINT ["./gunicorn.sh"]