export APPNAME="djangoLolInfo"
apt update -y
apt install -y software-properties-common supervisor nodejs npm nginx vim libpq-dev python3 python3-django python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
add-apt-repository ppa:deadsnakes/ppa -y
apt install -y python3.9 python3.9-distutils
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 10
update-alternatives --install /usr/bin/python python /usr/bin/python3.9 10
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
rm -rf get-pip.py


python3 -m pip install -r requirements.txt
python3 -m pip install gunicorn

echo "server {
        listen  80;
        server_name \"13.36.2.198\";

        location /static/ {
            alias /home/ubuntu/$APPNAME/static/;
        }

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header X-Forwarded-Host \$server_name;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_redirect off;
            add_header P3P 'CP=\"ALL DSP COR PSAa OUR NOR ONL UNI COM NAV\"';
            add_header Access-Control-Allow-Origin *;
        }
}" > /etc/nginx/sites-available/$APPNAME
if ! test -f "/etc/nginx/sites-enabled/$APPNAME"; then
  ln -s /etc/nginx/sites-available/$APPNAME /etc/nginx/sites-enabled/$APPNAME
fi

systemctl restart nginx
echo "[program:djangoapp]
command = gunicorn $APPNAME.wsgi  -b 127.0.0.1:8000 -w 4 --timeout 90
autostart=true
autorestart=true
directory=/home/ubuntu/$APPNAME
stderr_logfile=/var/log/game_muster.err.log
stdout_logfile=/var/log/game_muster.out.log" > /etc/supervisor/conf.d/djangoapp.conf
supervisorctl reread
supervisorctl update
supervisorctl restart djangoapp