FROM vimagick/scrapyd

MAINTAINER WILLNIGHT

CMD HOST_IP=$(awk "/$HOSTNAME/{ print \$1}" < /etc/hosts)&&curl -X PUT -d "{\"id\": \"$HOSTNAME\",\"name\": \"$HOSTNAME\",\"address\": \"$HOST_IP\",\"port\": 6800,\"tags\": [\"scrapyd\"],\"checks\": [{\"http\": \"http://$HOST_IP:6800\",\"interval\": \"5s\"}]}" http://$CONSUL_IP:8500/v1/agent/service/register && scrapyd

