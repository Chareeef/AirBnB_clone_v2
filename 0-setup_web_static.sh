#!/usr/bin/env bash
# Set up nginx server to serve web static content

if ! dpkg -l | grep -q nginx; then
	sudo apt-get update
	sudo apt-get install nginx -y
fi

sudo mkdir -p /etc/nginx/html
echo "Hello World!" | sudo tee /etc/nginx/html/index.html >/dev/null

sudo mkdir -p /etc/nginx/html/error_pages
echo "Ceci n'est pas une page" | sudo tee /etc/nginx/html/error_pages/error_404.html >/dev/null

sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

echo "Testing from $(hostname)" | sudo tee /data/web_static/releases/test/index.html >/dev/null

sudo ln -sf /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data

printf "server {
	listen		80 default_server;
	listen		[::]:80 default_server;
	root		/etc/nginx/html;
	index		index.html;
	server_name	mywonder.tech;

	location / {
		add_header X-Served-By \"%s\";
	}

	location /hbnb_static/ {
		alias /data/web_static/current/;
	}

	location /redirect_me {
		return 301 https://www.linkedin.com/in/youssef-charif-hamidi;
	}

	error_page 404 /error_404.html;

	location = /error_404.html {
		root	/etc/nginx/html/error_pages;
		internal;
	}
}
" "$(hostname)" | sudo tee /etc/nginx/sites-available/default >/dev/null

sudo service nginx reload
