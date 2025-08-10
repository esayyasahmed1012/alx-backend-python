# Use official Python 3.10 base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code to the working directory
COPY . .

# Expose port 8000 (default for Django)
EXPOSE 8000

# Command to run the Django app with gunicorn (production server)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]