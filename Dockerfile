# 1. Use an official Python runtime as a base image
FROM python:3.13.5-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your app’s code
COPY . .

# 5. Expose the port your app runs on
EXPOSE 8000

# 6. Command to run the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
