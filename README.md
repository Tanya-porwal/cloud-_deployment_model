# Cloud Deployment Lab

A small Flask web application for the containerization and AWS EC2 deployment lab. The home page displays a welcome message, an application owner name, and the application version. Both values can be configured using environment variables.

## Prerequisites

- Python 3.12+ for running without Docker
- Docker Desktop (or Docker Engine) for building and running the container
- An AWS account and an EC2 key pair for the deployment exercise
- Git and a GitHub account

## Run locally with Python

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
$env:APP_NAME = "Your Name"
$env:APP_VERSION = "1.0.0"
py app.py
```

Open <http://localhost:5000>. The health endpoint is <http://localhost:5000/health>.

Run the tests with:

```powershell
py -m unittest discover -s tests -v
```

## Build and test the Docker image locally

From the repository root:

```powershell
docker build -t cloud-deployment-lab:1.0.0 .
docker run --rm -d --name cloud-deployment-lab `
  -p 5000:5000 `
  -e APP_NAME="Your Name" `
  -e APP_VERSION="1.0.0" `
  cloud-deployment-lab:1.0.0
```

Verify the running container and application:

```powershell
docker ps
Invoke-WebRequest http://localhost:5000
Invoke-RestMethod http://localhost:5000/health
docker logs cloud-deployment-lab
docker stop cloud-deployment-lab
```

The container runs as a non-root user. Set `APP_NAME` to your name and `APP_VERSION` to the release you are deploying.

## Create and push the GitHub repository

Create a public or private GitHub repository named **cloud-deployment-lab** (without initializing it with a README), then from this project directory run:

```powershell
git add app.py templates/index.html requirements.txt Dockerfile .dockerignore .gitignore tests/test_app.py README.md
git commit -m "Add Flask app and Docker deployment instructions"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/cloud-deployment-lab.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your account name. If `origin` is already set, update it with `git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/cloud-deployment-lab.git` rather than adding it again. Use additional descriptive commits as you refine the app or its deployment configuration.

## Deploy on AWS EC2

### 1. Launch and configure the instance

1. Launch an Ubuntu Server 24.04 LTS EC2 instance and select or create a key pair. Assign a public IPv4 address (an Elastic IP is recommended if the address must remain stable).
2. In the instance's security group, add inbound rules:
   - SSH, TCP port 22, **your IP address only**.
   - Custom TCP, port 5000, your IP for a restricted test, or `0.0.0.0/0` if the lab requires public access. Restrict the source again when testing is complete.
3. Connect to the instance using the SSH command and key file shown by the EC2 console:

```powershell
ssh -i .\YOUR_KEY.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 2. Install Docker and deploy

Run these commands in the SSH session on the Ubuntu instance:

```bash
sudo apt-get update
sudo apt-get install -y docker.io git
sudo systemctl enable --now docker
sudo docker --version

git clone https://github.com/YOUR_GITHUB_USERNAME/cloud-deployment-lab.git
cd cloud-deployment-lab
sudo docker build -t cloud-deployment-lab:1.0.0 .
sudo docker run -d --name cloud-deployment-lab \
  --restart unless-stopped \
  -p 5000:5000 \
  -e APP_NAME="Your Name" \
  -e APP_VERSION="1.0.0" \
  cloud-deployment-lab:1.0.0
```

Replace `YOUR_GITHUB_USERNAME` and `Your Name` with your values. If you update the application and need to recreate the container, run `sudo docker rm -f cloud-deployment-lab`, rebuild the image, and rerun the `docker run` command.

### 3. Verify public access

On the EC2 instance, check `sudo docker ps` and `sudo docker logs cloud-deployment-lab`. From your computer, open `http://YOUR_EC2_PUBLIC_IP:5000` or run:

```powershell
Invoke-WebRequest http://YOUR_EC2_PUBLIC_IP:5000
Invoke-RestMethod http://YOUR_EC2_PUBLIC_IP:5000/health
```

The page should display the welcome message, configured name, and version. Do not use `https://` unless you separately configure TLS and a domain or reverse proxy.

## Evidence and submission

Capture and include your own screenshots in the lab submission:

1. `docker ps` showing the running local or EC2 container.
2. The app loaded in a browser using the EC2 public IP and port.
3. The GitHub repository page showing the source and meaningful commit history.

This repository does not include screenshots or claim a live EC2 deployment; those require your AWS account and must be captured after you perform the steps above. Submit the repository URL, screenshots, and a short account of any issues you encountered and how you resolved them.

During local validation, Python was not installed on the Windows host, so the unit tests were run successfully inside the built Docker image instead. The image build and local container checks completed successfully. GitHub repository creation/push and EC2 deployment still need to be performed in your accounts; record any issues from those steps and their resolutions here or in your submission.

## Troubleshooting

- **Browser cannot connect:** Confirm the instance has a public IPv4 address, the container is running (`sudo docker ps`), and the security group allows inbound TCP 5000 from your client address. Check `sudo docker logs cloud-deployment-lab`.
- **Container exits immediately:** Inspect `sudo docker logs cloud-deployment-lab`; rebuild after confirming `requirements.txt`, `app.py`, and `templates/index.html` are present.
- **Port 5000 is already in use:** Stop the previous container, or map another host port, for example `-p 8080:5000`, and allow that port in the security group.
- **SSH times out:** Verify the instance is running, the SSH key is correct, and inbound TCP 22 is restricted to and allowed from your current public IP.
- **GitHub clone or push is denied:** Check the repository URL and visibility. For a private repository, configure GitHub authentication on the client or instance before cloning.
