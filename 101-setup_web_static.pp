# Set up nginx server to serve web static content

exec { 'Update apt':
  command  => 'sudo apt-get update',
  provider => shell,
  before   => Exec['Nginx'],
}

exec { 'Nginx':
  command  => 'sudo apt-get install nginx -y',
  provider => shell,
  before   => Exec['Header'],
}

exec { 'Header':
  command  => 'sudo sed -i "s#server_name _;#server_name _;\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html;\n\t}\n#" /etc/nginx/sites-available/default',
  provider => shell,
  before   => Exec['Restart'],
}

exec { 'Restart':
  command  => 'sudo service nginx restart',
  provider => shell,
}
