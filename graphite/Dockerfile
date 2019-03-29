FROM graphiteapp/graphite-statsd:1.1.5-10
ADD storage-schemas.conf /opt/graphite/conf
ADD carbon.conf /opt/graphite/conf
# Resolve a current nginx issue
RUN adduser -u 1000 -D -S -G www-data www-data
