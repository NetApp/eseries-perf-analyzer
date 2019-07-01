FROM graphiteapp/graphite-statsd:1.1.5-11
ADD storage-schemas.conf /opt/graphite/conf
ADD carbon.conf /opt/graphite/conf
RUN (ping -c 1 google.com && sed -i -e 's/v3\.8/edge/g' /etc/apk/repositories) || \
(printf 'http://repomirror-ict.eng.netapp.com/alpine-linux/edge/main\nhttp://repomirror-ict.eng.netapp.com/alpine-linux/edge/community' > /etc/apk/repositories) && apk update && apk upgrade
# Resolve a current nginx issue
RUN adduser -u 1000 -D -S -G www-data www-data
