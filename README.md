# 🚀 Flask App Deployment to AWS EC2 via GitHub Actions

This guide walks through the complete process of building and deploying a Python Flask web application to an AWS EC2 instance using GitHub Actions. It includes infrastructure setup, application development, CI/CD configuration, and end-to-end testing.

---

## 📁 Project Overview

We will:
- Create a Flask web application
- Launch an EC2 instance on AWS
- Configure GitHub Actions to deploy the app
- Set up systemd to manage the app as a service
- Use Nginx as a reverse proxy
- Validate the deployment with end-to-end testing

---

## ✅ Prerequisites

- GitHub account
- AWS account
- SSH key pair for EC2 access
- Basic knowledge of Python and Linux


Build & Deploy a Flask App on EC2 via GitHub Actions 

1. Create a GitHub Account 

Go to https://github.com 

Sign up if you don’t have an account already. 

2. Create a GitHub Repository 

Log in to GitHub. 

Click New Repository and name it (e.g., flask-webapp01). 

Initialize with a README file. 

Add a .gitignore for Python to ignore unnecessary files. 

3. Create an AWS Account 

Sign up at https://aws.amazon.com if you don’t have an account. 

Create an IAM user with programmatic access (access keys). 

Save the Access Key ID and Secret Access Key securely. 

4. Launch an EC2 Instance 

Go to the AWS Management Console > EC2. 

Launch a new instance using  Ubuntu. 

Choose t3.micro (Free Tier eligible). 

Configure Security Group to open ports: 

22 (SSH) 

80 (HTTP) 

Launch and connect to your instance via SSH: 

    ssh -i your-key.pem ubuntu@your-ec2-public-ip 
 

5. Build a Sample Python (Flask) App 

On your local machine or EC2, create a Flask app file (app.py): 

from flask import Flask 

app = Flask(__name__) 

@app.route("/") 

def hello_world(): 

    return "<p>Hello, Welcome to Agilisium Devops Team!</p>" 

@app.route("/hello/<name>") 

def hello_name(name): 

    return f"<h1>Hello, Welcome to Agilisium Devops Team {name}!</h1>" 

if __name__ == "__main__": 

    app.run(port=5000) 


Create a requirements.txt: 

 Flask 


6. Configure GitHub Actions Pipeline to Deploy to EC2 

In your GitHub repo, create .github/workflows/python-.app.yml: 

name: Python application 

on: 

  push: 

    branches: [ "main" ] 

  pull_request: 

    branches: [ "main" ] 

permissions: 

  contents: read 

jobs: 

  build: 

    runs-on: ubuntu-latest 

    steps: 

    - uses: actions/checkout@v4 

    - name: Set up Python 3.10 

      uses: actions/setup-python@v3 

      with: 

        python-version: "3.10" 

    - name: Install dependencies 

      run: | 

        python -m pip install --upgrade pip 

        pip install flake8 pytest 

        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi 

  

    - name: Copy files to EC2 

      uses: appleboy/scp-action@master 

      with: 

        host: ${{ secrets.EC2_HOST }} 

        username: ${{ secrets.EC2_USER }} 

        key: ${{ secrets.EC2_KEY }} 

        source: "." 

        target: "/home/ubuntu/app" 

  

    - name: SSH and restart service 

      uses: appleboy/ssh-action@master 

      with: 

        host: ${{ secrets.EC2_HOST }} 

        username: ${{ secrets.EC2_USER }} 

        key: ${{ secrets.EC2_KEY }} 

        script: | 

          cd /home/ubuntu/app 

          pip3 install -r requirements.txt 

          sudo systemctl restart flaskapp 

Add Secrets in GitHub Repository Settings (under Settings > Secrets and variables > Actions): 

EC2_HOST: Your EC2 public IP 

EC2_USER: Username (ubuntu for Ubuntu) 

EC2_KEY: Contents of your private SSH key (the .pem file) 

 

7. Configure a Systemd Service for the Backend on EC2 

Create a service file /etc/systemd/system/flaskapp.service: 

[Unit]  

Description=Flask App  

 

[Service]  

 

User=ubuntu  

WorkingDirectory=/home/ubuntu/app  

ExecStart=/home/ubuntu/flaskenv/bin/python /home/ubuntu/app/app.py  

Restart=always  

 

[Install]  

WantedBy=multi-user.target 

 
 

Reload systemd, enable and start the service: 

sudo systemctl daemon-reload 
sudo systemctl enable flaskapp.service 
sudo systemctl start flaskapp.service 
 

 

8. Set Up Nginx as a Reverse Proxy 

Install Nginx on EC2: 

sudo apt update 
sudo apt install nginx 

Configure Nginx by editing /etc/nginx/nginx.conf  
 
		server { 

        listen 80; 

        server_name  <your-ec2-instancepublic-ip >; 

        access_log /var/log/nginx/access.log; 

        error_log /var/log/nginx/error.log; 

        location / { 

        proxy_pass http://127.0.0.1:5000; 

  } 

} 
 

Restart Nginx: 

sudo systemctl restart nginx 
 

 

9. Run an End-to-End Test 

Push your code changes to GitHub: 

git add . 
git commit -m "Setup Flask app with deployment" 
git push origin main 
 

GitHub Actions will run and deploy the app to your EC2 instance. 

Visit http://your-ec2-public-ip in your browser. 

You should see: Hello from EC2! 

 
