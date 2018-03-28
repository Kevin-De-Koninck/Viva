class Unattended_upgrades:
  class Unattended_upgrades:
    filename = "/etc/apt/apt.conf.d/50unattended-upgrades"
    content = """
Unattended-Upgrade::Allowed-Origins {
        "${distro_id}:${distro_codename}";
        "${distro_id}:${distro_codename}-security";
        "${distro_id}ESM:${distro_codename}";
};

Unattended-Upgrade::Package-Blacklist {
};

Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
"""

  class Auto_upgrades:
    filename = "/etc/apt/apt.conf.d/20auto-upgrades"
    content = """
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "3";
APT::Periodic::Download-Upgradeable-Packages "1";
"""

class NginX:
  class sites_available_default:
    filename = "/etc/nginx/sites-available/default"
    PHPMyAdmin_port = 9999
    content = """
server {
     listen 80;
     server_name localhost;
     access_log /var/log/nginx/access.log;
     error_log /var/log/nginx/error.log;
     index index.php index.htm index.html;

     location / {
          try_files $uri $uri/ =404;
    }

     error_page 404 /404.html;
     error_page 500 502 503 504 /50x.html;
     location = /50x.html {
          root /usr/share/nginx/html;
    }

     location ~ \.php$ {
          try_files $uri =404;
          fastcgi_split_path_info ^(.+\.php)(/.+)$;
          fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
          fastcgi_index index.php;
          fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
          include fastcgi_params;
    }
}

server {
  listen %(PHPMyAdmin_port)s;
  server_name localhost;
  root /usr/share/phpmyadmin;
  index index.php index.html index.htm;
  if ( !-e $request_filename ) {
    rewrite ^/(.+)$ /index.php?url=$1 last;
    break;
  }
  location ~ .php$ {
    try_files $uri =404;
    fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
    fastcgi_index index.php;
     fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include /etc/nginx/fastcgi_params;
  }
}
""" % {'PHPMyAdmin_port': str(PHPMyAdmin_port)}