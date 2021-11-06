export APPNAME="djangoLolInfo"
apt-get update
apt install software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt install -y python3.9
apt install -y python3.9-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 10
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 10
python3 get-pip.py
rm -rf get-pip.py
apt-get install -y git python3-venv python3-pip supervisor nginx vim libpq-dev

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

apt-get install nginx
echo "server {
        listen 80 default_server;
        listen [::]:80 default_server;


        location /static/ {
            alias /home/ubuntu/$APPNAME/static/;
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
#echo "[program:djangoapp]
#command = /home/ubuntu/$APPNAME/venv/bin/gunicorn $APPNAME.wsgi  -b 127.0.0.1:8000 -w 2 --timeout 90
#autostart=true
#autorestart=true
#directory=/home/ubuntu/$APPNAME
#stderr_logfile=/var/log/game_muster.err.log
#stdout_logfile=/var/log/game_muster.out.log"
#supervisorctl reread
#supervisorctl update
#supervisorctl restart djangoapp