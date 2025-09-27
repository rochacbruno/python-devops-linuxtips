# Gancho takes websocket payload and perform actions

## Usage:

On github set websocket for the desired events,
recommended [create, push, ping].

## Installation

```bash
# Service directories
mkdir p /opt/gancho

# Service User
sudo useradd -r -s /usr/sbin/nologin -d /opt/gancho -M gancho

# This gives permission to manipulate /var/www, adjust for your needs
sudo chown -R gancho:www-data /opt/gancho
sudo chown -R root:www-data /var/www
sudo chmod -R 775 /var/www
sudo usermod -aG www-data gancho

# Environment
cd /opt/gancho
uv venv
uv pip install gancho

```

## Test it

```console
$ /opt/gancho/.venv/bin/gancho

INFO:     Started server process [4321]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)]
```

On a separate terminal

```bash
curl -X POST localhost:5000 -H "x-github-event:ping"
```


## Service Daemon

Soket directory

```bash
sudo mkdir -p /run/gancho
sudo chown gancho:www-data /run/gancho
sudo chmod 770 /run/gancho
```

/etc/systemd/system/gancho.socket
```ini
[Unit]
Description=Socket do gancho

[Socket]
ListenStream=/run/gancho/gancho.sock
SocketMode=0660
SocketUser=gancho
SocketGroup=www-data

[Install]
WantedBy=sockets.target
```

/etc/systemd/system/gancho.service
```ini
[Unit]
Description=gancho daemon
Requires=gancho.socket
After=network.target

[Service]
User=gancho
Group=www-data
WorkingDirectory=/opt/gancho
ExecStart=/opt/gancho/.venv/bin/gancho --uds /run/gancho/gancho.sock
Restart=always
RestartSec=5
StandardInput=socket
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gancho.socket
sudo systemctl status gancho.service   # will start only when socket is used
```

```bash
$ systemctl status gancho
○ gancho.service - gancho daemon
     Loaded: loaded (/etc/systemd/system/gancho.service; disabled; preset: enabled)
     Active: inactive (dead)
TriggeredBy: ● gancho.socket
```

Logs

```bash
journalctl -u gancho.service -f
```

## Nginx host

Replace `example.com` with your host


/etc/nginx/sites-available/gancho
```conf
server {
    listen 80;
    server_name webhook.example.com;

    location / {
        proxy_pass http://unix:/run/gancho/gancho.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
ln -s /etc/nginx/sites-available/gancho /etc/nginx/sites-enabled/gancho
```
```bash
nginx -t
sudo systemctl restart nginx
```

## Notes:

- Ensure your default nginx site is cleaned up and not catching all domains
- If using https, ensure certificate is enabled to the new domain, example: `certbot --nginx -d webhook.example.com`


## Deployments


For a repo `my-username/my-repo` the following will be the deploy script.

`/opt/gancho/deployment/my-username/my-repo/deploy.sh`
```bash
#!/usr/bin/bash

echo "deploying"
```
```bash
chmod +x /opt/gancho/deployment/my-username/my-repo/deploy.sh 
```



