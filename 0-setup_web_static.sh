#!/usr/bin/env bash
# This script sets up my web server for the deployment of
# web_static

# Install Nginx
apt-get -y update
apt-get -y install nginx

# Create directories
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/
sed -i "38i location /hbnb_static/ {\n alias /data/web_static/current/;\n}" /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart
