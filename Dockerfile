FROM python:3.10-slim-buster

RUN apt update -y && apt install awscli -y


# Set working directory
WORKDIR /app

COPY . /app  

# Install dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y sqlite3


CMD ["streamlit", "run", "streamlit_chatbot.py", "--server.port=8501", "--server.address=0.0.0.0"] 
