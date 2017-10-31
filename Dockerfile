FROM nginx

RUN apt update
RUN apt install -y wget
RUN wget https://dl.eff.org/certbot-auto
RUN chmod +x certbot-auto
