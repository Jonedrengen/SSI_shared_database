# Use the official Python 3.12.2 image as the base image
FROM python:3.12.2

# set the working directory inside the container to /test_app
WORKDIR /test_app

# Copy the requirements.txt file from the local machine to the container at /app
COPY requirements.txt .

# Install the required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#copy all files from the current directory on the local machine to the container
COPY . .

# Run the main.py file when the container starts
CMD ["python", "main.py"]