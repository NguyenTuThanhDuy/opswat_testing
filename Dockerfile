FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the backend directory to the working directory
COPY PythonProject/backend /app/backend

WORKDIR /app/backend
# Install the project dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Expose the port that the application will listen on
EXPOSE 8000

# Define the command to run your application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]