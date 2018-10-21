---------------------WIP---------------------





TODO: make sure the default page works and requests are redirected to HTTPS, except the one for hadling ACME challenges.

Why did I create this image:
- I didn't want to modify my NGINX files by using Certbot's NGINX plugin. Instead, I manually applied its changes.
- I wanted an easier way of replicating the reverse proxy across multiple docker swarm nodes.
- I wanted to easily reload the server with new NGINX configuration.


`docker build playfulcorgi/nginx-letsencrypt-webroot-style .`

/etc/letsencrypt on the container can be attached to the host to save Let's Encrypt's certificates locally for future reuse.



<!-- TODO: add a commented out example of http handling for a domain in NGINX conf files. -->

By default, certbot will not periodically check the age of the SSL certificate for provided domains. To enable Certbot automatic SSL renewal, `CERTBOT_ENABLED` environment variable must be set to `true`. This is to prevent creating multiple replicas of this Docker image (ex. using `docker service create` with each trying to download a new certificate when the existing one becomes old and using up all the quota for SSL certificates by accident.

<!-- TODO: Decide how to share the newest certificate between multiple Docker Swarm replicas. -->

<!-- Make sure NGINX finds the new certificate. I'm not sure if a restart of NGINX is needed to pick up a new certificate. -->


A file is created at /etc/nginx/nginx-variables.conf that can be included in the nginx configuration to provide the IP address of the Docker container. It's not a bulletproof solution, but useful in some situations, for example when a NGINX is used as reverse proxy to make a request to a different port on the same machine.

<!-- TODO: mention volume where to put NGINX .confs -->

<!-- TODO: add information about what needs to be added to a NGINX location instruction to use a Let's Encrypt certificate for https -->


Let's Encrypt will put files for the challenge under /tmp/letsencrypt/www/.well-known/acme-challenge, in separate folders, one for each domain. NGINX serves files from that location so that Let's Encrypt can make a GET request for them on port 80 and confirm they're available and the domain is owned by the user running the server.

<!-- TODO: write exmple configuration in readme to use let's encrypt's certificate in NGINX -->

```bash
docker run \
	--rm \
	-ti \
	-v /home/ubuntu/letsencrypt:/etc/letsencrypt \
	--env-file .env \
	-p 80:80 \
	-p 443:443 \
	playfulcorgi/reverse-proxy
```
(change /home/ubuntu/letsencrypt to wherever you want to store Certbot configuration and certificates from Let's Encrypt)

```
docker pull playfulcorgi/nginx-letsencrypt-webroot-style
```

<!-- ```bash
docker service create \
    --mount type=bind,source=/root/nginx-reverse-proxy-configuration/domains.txt,destination=/etc/letsencrypt-domains.txt \
    --mount type=bind,source=/root/nginx-reverse-proxy-configuration/rest.conf,destination=/etc/nginx/conf.d/attached/rest.conf \
    --mount type=bind,source=/root/nginx-reverse-proxy-configuration/options-ssl-nginx.conf,destination=/etc/nginx/options-ssl-nginx.conf \
    --mount type=bind,source=/root/nginx-reverse-proxy-configuration/letsencrypt,destination=/etc/letsencrypt \
    -p 80:80 \
    -p 443:443 \
    -e EMAIL="email@email.com" \
    --detach=false \
    --name nginx-reverse-proxy \
    playfulcorgi/nginx-letsencrypt-webroot-style
``` -->


TODO: make sure this docker image is safe to use as a Docker service, at least when --replicate 1, but it should be deployable on any node picked by docker's load balancer.









Note: Certbot, if enabled, will renew the SSL certificate for all domains, even if the list of domains changes only partially. This is to make handling of the certificate easier internally.

`CERTBOT_DOMAINS` is a string of domains separated by spaces.


if certbot is enabled (`CERTBOT_ENABLED`), `CERTBOT_EMAIL` is required.


TODO: provide link to certbot documentation: https://certbot.eff.org/docs/using.html



After testing if certbot works properly, for Certbot to use real certificates, add the env variable CERTBOT_STAGING="true"

# TODO: make sure nginx reload works without quitting Docker



<!-- TODO: write what happens with .template.conf files, which ${<name>} will be replaced and by what.


<!-- TODO: provide example of routing with SSL cert in use -->

<!-- TODO: provide example .env file CERTBOT_ENABLED=true
CERTBOT_EMAIL=
CERTBOT_STAGING=true
CERTBOT_DOMAINS='example.com www.example.com example2.com www.example2.com'
 -->

 <!-- TODO: write that no env variables are required to start the container but without any options it will just run NGINX -->


 <!-- If trying to run multiple replicas of this Docker image for the same domains, make sure only one is resposible for periodic certificate renewals or modify source code so that different images try to renew the certificate at different times. Once certificates are renewed, spread the new certificates to replicas that don't automatically renew them (CERTBOT_ENABLED is not set to true). These replicas observe the /etc/letsencrypt directory for changes and will automatically reload NGINX when there's something new in it. -->

 <!-- Known issues: a new certificate will be requested whenever a new domain is added or an old one removed from letsencrypt. Let's encrypt limits the number of cert generations one can make for the same domain every month. It's currently 10 per month. --> TODO: check how the limit works - if I refresh a certificate for old domains but also add new, is the limit increased for all domains separately?

 sprobowac umieścic dostępne env variables i volumes w tabelce żeby było czytelniej

 Warning: on container run, all environment variables will be copied to a file in the container so that cron can properly run certificate renewals with the same environment variables as provided when starting the container and first renewal attempt.

 Warning: by itself, this image's containers will not automatically distribute certificates across replicas. However, if Certbot is not enabled (CERTBOT_ENABLED !== 'true'), a container will check twice a day if certificates inside `/etc/letsencrypt` have changed and reload the server if they did. If there's a need to immediately pick up a new certificate, run `/scripts/useNewCerts` inside the container using `docker exec <container name> /scripts/useNewCerts`.

 Logs for cron jobs are saved in `/var/log/syslog`. Logs for the running container can be obtained from docker using [docker logs](https://docs.docker.com/engine/reference/commandline/logs/), for example.

 TODO: Add legal part, that I'm not responsible for any damages caused by this software and it's distributed as is.


 Pull Requests on GitHub are welcome.


 green console messages refer to subprocesses


 # For the Certbot certificate renewal, NGINX has to respond to requests such as: 12.123.432.36 - - [05/Jan/2016:20:11:24 -0500] "GET /.well-known/acme-challenge/ASDFASDcasdfasdf-323e1aw HTTP/1.1" 200 87 "-" "Mozilla/5.0 (compatible; Let's Encrypt validation server; +https://www.letsencrypt.org)"

 Make sure your server allows requests from ports 80 (for the Certbot challenge) and 443.


 You may also want to mount /var/log/letsencrypt to save logs to a safe location.







 server{
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    # (coveredexample.com - address covered by HTTPS using nginx (isn't HTTPS))
    # proxy_set_header Host coveredexample.com;
    # proxy_ssl_server_name on;
    # client_max_body_size 100M;
    # server_name .example.com; # The . at the beginning will allow 'www.' before the address.
    
    # location / {
    #     proxy_pass https://coveredexample.com/prod/;
    # }

	ssl_certificate ${certs}/example.com/fullchain.pem;
	ssl_certificate_key ${certs}/example.com/privkey.pem;
    include conf.d/attached/options-ssl-nginx.conf;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}







<!-- Use with caution. This software may contain serious bugs. I can not be made responsible for any damage the software may cause to your system or files. -->






<!-- License

Copyright (C) 2011-2017 by <name> <surname> <email>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/. -->




FIXME: if volumes are empty, copy default files into them
TODO: Document how volumes are filled when empty and what those volumes contain. Create a way for people to fill those volumes manually by copying default files to them and modifying those files however they need. Empty directories should be checked and filled just before they're needed.

TODO: Show example terminal output when running this docker image, or even a gif with output showing up.

Logs from NGINX will be returned directly to stdout of Docker. To output logs from Docker Swarm, use `docker service logs nginx-reverse-proxy`.


The directory name with the certificate for all domains will be located under letsencrypt/live/<first domain provided on list>.