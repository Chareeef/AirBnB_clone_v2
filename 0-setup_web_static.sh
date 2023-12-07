#!/usr/bin/env bash
# Set up nginx server to serve web static content

if ! dpkg -l | grep -q nginx; then
	sudo apt-get update
	sudo apt-get install nginx -y
fi

sudo mkdir -p '/data/web_static/releases/test'
sudo mkdir -p '/data/web_static/shared'

echo "<h2>Testing...</h2>" | sudo tee '/data/web_static/releases/test/index.html' >/dev/null

sudo ln -sf '/data/web_static/releases/test' '/data/web_static/current'

sudo chown -R ubuntu:ubuntu /data/

printf "server {
	listen	80 default_server;
	listen	[::]:80 default_server;

	location /hbnb_static/ {
		alias /data/web_static/current/;
		index index.html;
	}

}
" | sudo tee '/etc/nginx/sites-available/default' >/dev/null

sudo service nginx restart
