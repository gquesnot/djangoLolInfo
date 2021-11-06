export APPNAME="djangoLolInfo"
apt-get update
apt-get install -y git python3-dev python3-venv python3-pip supervisor nginx vim libpq-dev
# shellcheck disable=SC2164
cd $APPNAME
pathon3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

apt-get install nginx
echo "server {
        listen 80 default_server;
        listen [::]:80 default_server;


        location /static/ {
            alias /home/ubuntu/"+$APPNAME+"/static/;
        }


        location /media/ {
            alias /home/ubuntu/djangoapp/media/;
        }


        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header X-Forwarded-Host \$server_name;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_redirect off;
            add_header P3P \'CP=\"ALL DSP COR PSAa OUR NOR ONL UNI COM NAV\"\';
            add_header Access-Control-Allow-Origin *;
        }
}" > /etc/nginx/sites-available/$APPNAME

ln -s /etc/nginx/sites-available/$APPNAME /etc/nginx/sites-enabled/$APPNAME
systemctl nginx restart
echo "[program:djangoapp]
command = /home/ubuntu/"+$APPNAME+"/venv/bin/gunicorn "+$APPNAME+".wsgi  -b 127.0.0.1:8000 -w 2 --timeout 90
autostart=true
autorestart=true
directory=/home/ubuntu/"+$APPNAME+"
stderr_logfile=/var/log/game_muster.err.log
stdout_logfile=/var/log/game_muster.out.log"
supervisorctl reread
supervisorctl update
supervisorctl restart djangoapp