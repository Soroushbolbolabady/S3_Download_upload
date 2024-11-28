# S3 Downloader/uploader

This project automate the download and upload from and to s3.

## Installation

Create a virtualenv

```bash
python3 -m venv venv
```

Active the venv(Linux)
```bash
source venv/bin/activate
```
Active the venv(Windows)
```bash
\venv\Scripts\activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.


```bash
pip install -r requirments 
```
add .env file to your project

```.env
AWS_ACCESS_KEY_ID="Your-ACCESS-KEY"
AWS_SECRET_ACCESS_KEY="Your-SECRET-KEY"
S3_BUCKET_NAME="Your-Bucketname"

```

## Running

```bash
python main.py
```

