# DevOps Practice Project

A hands-on DevOps practice project demonstrating core Linux server administration skills including web server configuration, process management, database setup, and version control.

## 🛠️ Skills Covered

- Linux basics
- Nginx reverse proxy
- systemd service management
- MySQL setup & configuration
- SSH key authentication
- Git & GitHub

---

## 📁 Project Structure

```
devops-practice/
├── myapp.py          # Python HTTP server (port 5000)
├── myapp.service     # systemd service unit file
├── server_config     # Nginx virtual host configuration
└── README.md
```

---

## ⚙️ Setup & Configuration

### 1. Linux Basics

This project was built and tested on **Ubuntu (WSL2)** — fully compatible with **Amazon EC2**.

Key commands used:
```bash
ss -tulnp              # View active ports and services
lsof -i -P -n          # List open ports
ps aux                 # View running processes
```

---

### 2. Nginx Reverse Proxy

Nginx is configured to serve a static HTML file on `/` and proxy API requests to the Python app on `/api`.

**Install Nginx:**
```bash
sudo apt update
sudo apt install nginx
```

**Configuration (`server_config`):**
```nginx
server {
    listen 80;

    location / {
        root /var/www/html;
        index index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable the config:**
```bash
sudo ln -s /etc/nginx/sites-available/server_config /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### 3. Python App (`myapp.py`)

A minimal Python HTTP server for testing the reverse proxy setup.

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Hello from Python App!</h1>")

HTTPServer(('0.0.0.0', 5000), Handler).serve_forever()
```

---

### 4. systemd Service (`myapp.service`)

Configured as a systemd service so the Python app runs permanently and restarts automatically on failure.

```ini
[Unit]
Description=My Python App
After=network.target

[Service]
User=cool_boy
WorkingDirectory=/home/cool_boy
ExecStart=/usr/bin/python3 /home/cool_boy/myapp.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Manage the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl start myapp
sudo systemctl enable myapp
sudo systemctl status myapp
```

---

### 5. MySQL Setup

MySQL installed and configured with a dedicated user and database — following production best practices.

```bash
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

**Create database and user:**
```sql
CREATE DATABASE myapp;
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON myapp.* TO 'myuser'@'localhost';
FLUSH PRIVILEGES;
```

---

### 6. SSH Key & GitHub

Generated a dedicated ED25519 SSH key for GitHub authentication.

```bash
ssh-keygen -t ed25519 -C "your@email.com" -f ~/.ssh/id_github
```

**SSH config (`~/.ssh/config`):**
```
Host github.com
    IdentityFile ~/.ssh/id_github
    User git
```

**Test connection:**
```bash
ssh -T git@github.com
```

---

## 🏗️ Architecture

```
Browser
   ↓  http://your-ip/
 Nginx (port 80)
   ├── /        → Static HTML (/var/www/html)
   └── /api     → Python App (port 5000)
                    ↓
                 MySQL (port 3306)
```

---

## 🚀 EC2 Compatibility

All configurations in this project are fully compatible with **Amazon EC2 (Ubuntu)**. The same setup can be deployed on an EC2 instance with no modifications.

---

## 📚 What's Next

- [ ] Docker & Docker Compose
- [ ] CI/CD with GitHub Actions
- [ ] Deploy to AWS EC2
- [ ] SSL/HTTPS with Let's Encrypt
- [ ] Monitoring with Prometheus & Grafana
