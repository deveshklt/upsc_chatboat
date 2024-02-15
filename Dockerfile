FROM python:3.10-slim-buster

RUN apt update -y && apt install awscli -y

# Set environment variables
ENV PORT=8501

# Set working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt .
COPY streamlit_app.py .   

# Install dependencies
RUN pip install -r requirements.txt

# Expose the app port
EXPOSE $PORT

# Command to run the Streamlit app
CMD ["streamlit", "run", "--server.port", "$PORT", "streamlit_app.py"]  
