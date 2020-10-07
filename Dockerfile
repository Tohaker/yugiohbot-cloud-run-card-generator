FROM python:3.8-buster

# Variables from CLI
ARG GCP_SA_KEY

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Install Chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Create credentials file
RUN echo $GCP_SA_KEY > base64.txt
RUN base64 --decode base64.txt > gcp_terraform.json

# Set display port to avoid crash
ENV DISPLAY=:99
ENV PYTHONPATH=yugiohbot
ENV CHROMEDRIVER=/usr/local/bin/chromedriver
ENV CHROME=/usr/bin/google-chrome-stable
ENV GOOGLE_APPLICATION_CREDENTIALS=gcp_terraform.json

# Install pip modules
COPY requirements.txt $HOME/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY yugiohbot ./
COPY gcp_terraform.json ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
