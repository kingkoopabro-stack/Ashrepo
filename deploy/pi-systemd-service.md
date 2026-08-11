On Raspberry Pi (Raspbian / Raspberry Pi OS) using systemd to run a tiny Flask/Node backend for Stripe Checkout:

Example systemd unit (if running a Python Flask app on port 5000):

Create /etc/systemd/system/rare-candy-api.service:
```
[Unit]
Description=Rare Candy API
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/rare-candy
ExecStart=/usr/bin/python3 -m venv venv && /home/pi/rare-candy/venv/bin/python -m gunicorn -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
sudo systemctl daemon-reload
sudo systemctl enable --now rare-candy-api

If only serving static Hugo files, Hugo's generated site is in public/ and Nginx can serve it directly.