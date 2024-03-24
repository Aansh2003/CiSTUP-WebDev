FROM python:3.9

WORKDIR /app

# Copying just the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Check if opencv-python is installed before uninstalling
RUN pip freeze | grep -q 'opencv-python' && pip uninstall -y opencv-python || true

# Install opencv-python-headless
RUN pip install opencv-python-headless

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "server.py"]

