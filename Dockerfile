FROM public.ecr.aws/lambda/python:3.11

# Set a working directory in the container
WORKDIR /var/task

# Copy requirements.txt
COPY requirements.txt .

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY file_validation.py .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "file_validation.lambda_handler" ]
