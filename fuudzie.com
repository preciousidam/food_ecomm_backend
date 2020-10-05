server {
    listen 80;
    listen [::]:80;
    index index.html;
    server_name fuudzie.com www.fuudzie.com;
    location / {

        proxy_pass           http://localhost:3000;


        proxy_connect_timeout       900;
        proxy_send_timeout          900;
        proxy_read_timeout          900;
        send_timeout                900;

        proxy_redirect       off;
        proxy_set_header     Host $http_host;
        proxy_set_header     X-Real-IP $remote_addr;
        proxy_set_header     X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-NginX-Proxy true;

    }
}

server {
    listen 80;
    listen [::]:80;
    server_name api.fuudzie.com;

    location / {

        proxy_set_header X-Real-IP 
        $remote_addr;
        proxy_set_header 
        X-Forwarded-For 
        $proxy_add_x_forwarded_for;
        proxy_set_header Host 
        $http_host;
        proxy_set_header 
        X-NginX-Proxy true; proxy_pass 
        http://127.0.0.1:5050/;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade 
        $http_upgrade;
        proxy_set_header Connection 
        "upgrade";
        proxy_redirect off;
        proxy_set_header 
        X-Forwarded-Proto $scheme;

    }
}

server {
    listen 80;
    listen [::]:80;
    server_name v2.fuudzie.com;

    location / {

        proxy_set_header X-Real-IP 
        $remote_addr;
        proxy_set_header 
        X-Forwarded-For 
        $proxy_add_x_forwarded_for;
        proxy_set_header Host 
        $http_host;
        proxy_set_header 
        X-NginX-Proxy true; proxy_pass 
        http://127.0.0.1:4000;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade 
        $http_upgrade;
        proxy_set_header Connection 
        "upgrade";
        proxy_redirect off;
        proxy_set_header 
        X-Forwarded-Proto $scheme;

    }
}