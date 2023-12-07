# Set up nginx server to serve web static content

$nginx_conf = "server {
	listen	80 default_server;
	listen	[::]:80 default_server;

	location /hbnb_static/ {
		alias /data/web_static/current/;
		index index.html;
	}
}
"

exec { 'Update apt':
  command  => 'sudo apt-get update',
  provider => shell,
}

-> exec { 'Nginx':
  command  => 'sudo apt-get install nginx -y',
  provider => shell,
}

-> exec { 'test directory':
  command  => 'sudo mkdir -p /data/web_static/releases/test',
  provider => shell,
}

-> exec { 'shared directory':
  command  => 'sudo mkdir -p /data/web_static/shared',
  provider => shell,
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => 'Testing...',
}
-> exec { 'link current':
  command  => 'sudo ln -sf /data/web_static/releases/test /data/web_static/current',
  provider => shell,
}

-> exec { 'chmod':
  command  => 'sudo chown -R ubuntu:ubuntu /data/',
  provider => shell,
}

file{ '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => $nginx_conf,
}

exec { 'Restart':
  command  => 'sudo service nginx restart',
  provider => shell,
}
