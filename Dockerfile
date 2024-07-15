# Use the official Django image
FROM python:3.12.3

# Set the working directory
WORKDIR /PytubeProject

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN python PytubeProject/manage.py migrate
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install ffmpeg

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "PytubeProject/manage.py", "runserver", "0.0.0.0:8000"]
