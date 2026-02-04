#!/bin/bash
SSH_USER="server"  # Replace with Policy-Server username
POLICY_SERVER="192.168.56.2"
 
log() {
    echo "$(date) - $1" >> /var/log/nac_control.log
}
 
while true; do
    for client in client1 client2; do
        status=$(ssh -i ~/.ssh/nac_policy_server  "$SSH_USER@$POLICY_SERVER" "cat /tmp/${client}_status 2>/dev/null")
        if [ -z "$status" ]; then
            log "Failed to get status for $client"
            continue
        fi
 
        if [ "$client" == "client1" ]; then
            ip="192.168.56.101"
        else
            ip="192.168.56.102"
        fi
 
        sudo iptables -D FORWARD -s "$ip" -j ACCEPT 2>/dev/null
        sudo iptables -D FORWARD -s "$ip" -j DROP 2>/dev/null
 
        if [ "$status" == "compliant" ]; then
            sudo iptables -A FORWARD -s "$ip" -j ACCEPT
            log "Set $client ($ip) to ACCEPT"
        else
            sudo iptables -A FORWARD -s "$ip" -j DROP
            log "Set $client ($ip) to DROP"
        fi
    done
    sleep 60
done