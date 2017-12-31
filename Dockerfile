FROM nginx:1.13.7
ENV CERTBOT_INSTALL_DIRECTORY /certbotinstall
# certbot-auto is downloaded instead of doing apt-get install certbot, because
# apt-get can only download an older version of certbot.
RUN apt-get update && \
	apt-get install -y software-properties-common wget rsyslog && \
	mkdir "$CERTBOT_INSTALL_DIRECTORY" && \
	wget -P "$CERTBOT_INSTALL_DIRECTORY" https://dl.eff.org/certbot-auto && \
	chmod a+x "$CERTBOT_INSTALL_DIRECTORY/certbot-auto" && \
	ln -s "$CERTBOT_INSTALL_DIRECTORY/certbot-auto" /usr/bin/certbot && \
	certbot -n --version && \
	wget -P /tmp https://bootstrap.pypa.io/get-pip.py && \
	python3 /tmp/get-pip.py && \
	rm /tmp/get-pip.py && \
	pip3 install -U python-dotenv
ENV CERTBOT_CHALLENGE_DIRECTORY /tmp/letsencrypt/www
ENV CERTBOT_ENABLED "false"
ENV CERTBOT_DOMAINS ""
ENV CERTBOT_EMAIL ""
ENV CERTBOT_STAGING "true"
ENV CERTIFICATES_CHECK_FREQUENCY "0 0,12 * * *"
RUN rm /etc/nginx/conf.d/* /etc/nginx/nginx.conf
COPY nginx /etc/nginx
ENV STARTUP_SCRIPTS_DIRECTORY /scripts
RUN mkdir -p "${CERTBOT_CHALLENGE_DIRECTORY}"
ENV NGINX_CONFIG_DIRECTORY /etc/nginx/conf.d/attached
ENV NGINX_CONFIG_FILENAME index.conf
RUN touch "${NGINX_CONFIG_DIRECTORY}/${NGINX_CONFIG_FILENAME}"
VOLUME [ "/etc/letsencrypt", "${NGINX_CONFIG_DIRECTORY}", "/var/log" ]
COPY scripts "${STARTUP_SCRIPTS_DIRECTORY}"
# FIXME: ENTRYPOINT [ "/scripts/start" ] is needed instead of ENTRYPOINT [
# "${STARTUP_SCRIPTS_DIRECTORY}/start" ], becuase without shell, ENV expansion
# doesn't work. But no shell is required to receive system signals, such as
# SIGTERM and SIGINT, inside of the ENTRYPOINT script, so no ENV expansion is a
# compromise.
ENTRYPOINT [ "/scripts/start" ]