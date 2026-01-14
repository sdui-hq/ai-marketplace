#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, and pipeline failures
IFS=$'\n\t'       # Stricter word splitting

# Log to both stderr and a file for debugging
LOG_FILE="/tmp/init-firewall.log"
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE" >&2
}

log "=== Starting firewall initialization ==="

# 1. Extract Docker DNS info BEFORE any flushing
log "Step 1: Extracting Docker DNS rules..."
DOCKER_DNS_RULES=$(iptables-save -t nat | grep "127\.0\.0\.11" || true)
log "Step 1 complete. Found rules: ${DOCKER_DNS_RULES:-'(none)'}"

# Flush existing rules and delete existing ipsets
log "Step 2: Flushing iptables rules..."
iptables -F || { log "ERROR: iptables -F failed"; exit 1; }
iptables -X || { log "ERROR: iptables -X failed"; exit 1; }
iptables -t nat -F || { log "ERROR: iptables -t nat -F failed"; exit 1; }
iptables -t nat -X || { log "ERROR: iptables -t nat -X failed"; exit 1; }
iptables -t mangle -F || { log "ERROR: iptables -t mangle -F failed"; exit 1; }
iptables -t mangle -X || { log "ERROR: iptables -t mangle -X failed"; exit 1; }
log "Step 2 complete."

log "Step 3: Destroying existing ipset..."
ipset destroy allowed-domains 2>/dev/null || true
log "Step 3 complete."

# 2. Selectively restore ONLY internal Docker DNS resolution
log "Step 4: Restoring Docker DNS rules..."
if [ -n "$DOCKER_DNS_RULES" ]; then
    log "Found Docker DNS rules to restore"
    iptables -t nat -N DOCKER_OUTPUT 2>/dev/null || true
    iptables -t nat -N DOCKER_POSTROUTING 2>/dev/null || true
    echo "$DOCKER_DNS_RULES" | xargs -r -L 1 iptables -t nat
else
    log "No Docker DNS rules to restore"
fi
log "Step 4 complete."

# First allow DNS and localhost before any restrictions
log "Step 5: Setting up basic firewall rules..."
# Allow outbound DNS
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
# Allow inbound DNS responses
iptables -A INPUT -p udp --sport 53 -j ACCEPT
# Allow outbound SSH
iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT
# Allow inbound SSH responses
iptables -A INPUT -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
# Allow localhost
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
log "Step 5 complete."

# Create ipset with CIDR support
log "Step 6: Creating ipset..."
ipset create allowed-domains hash:net
log "Step 6 complete."

# Fetch GitHub meta information and aggregate + add their IP ranges
log "Step 7: Fetching GitHub IP ranges..."
gh_ranges=$(curl -s https://api.github.com/meta)
if [ -z "$gh_ranges" ]; then
    log "ERROR: Failed to fetch GitHub IP ranges"
    exit 1
fi

if ! echo "$gh_ranges" | jq -e '.web and .api and .git' >/dev/null; then
    log "ERROR: GitHub API response missing required fields"
    exit 1
fi

log "Step 8: Processing GitHub IPs..."
while read -r cidr; do
    if [[ ! "$cidr" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$ ]]; then
        log "ERROR: Invalid CIDR range from GitHub meta: $cidr"
        exit 1
    fi
    log "Adding GitHub range $cidr"
    ipset add allowed-domains "$cidr" -exist
done < <(echo "$gh_ranges" | jq -r '(.web + .api + .git)[]' | aggregate -q)
log "Step 8 complete."

# Resolve and add other allowed domains
log "Step 9: Resolving allowed domains..."
for domain in \
    "registry.npmjs.org" \
    "api.anthropic.com" \
    "sentry.io" \
    "statsig.anthropic.com" \
    "statsig.com" \
    "sdui.atlassian.net" \
    "www.notion.so" \
    "www.slack.com" \
    "coralogix.com" \
    "grafana.intranet-sdui.de" \
    "tms.sdux.de" \
    "ims.sdux.de" \
    "ums.sdux.de" \
    "git.sdui.de" \
    "firebase.google.com" \
    "play.google.com" \
    "console.firebase.google.com" \
    "marketplace.visualstudio.com" \
    "vscode.blob.core.windows.net" \
    "update.code.visualstudio.com"; do
    log "Resolving $domain..."
    ips=$(dig +noall +answer A "$domain" | awk '$4 == "A" {print $5}')
    if [ -z "$ips" ]; then
        log "ERROR: Failed to resolve $domain"
        exit 1
    fi

    while read -r ip; do
        if [[ ! "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
            log "ERROR: Invalid IP from DNS for $domain: $ip"
            exit 1
        fi
        log "Adding $ip for $domain"
        ipset add allowed-domains "$ip" -exist
    done < <(echo "$ips")
done
log "Step 9 complete."

# Get host IP from default route
log "Step 10: Detecting host network..."
HOST_IP=$(ip route | grep default | cut -d" " -f3)
if [ -z "$HOST_IP" ]; then
    log "ERROR: Failed to detect host IP"
    exit 1
fi

HOST_NETWORK=$(echo "$HOST_IP" | sed "s/\.[0-9]*$/.0\/24/")
log "Host network detected as: $HOST_NETWORK"

# Set up remaining iptables rules
log "Step 11: Setting up final firewall rules..."
iptables -A INPUT -s "$HOST_NETWORK" -j ACCEPT
iptables -A OUTPUT -d "$HOST_NETWORK" -j ACCEPT

# Set default policies to DROP first
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# First allow established connections for already approved traffic
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Then allow only specific outbound traffic to allowed domains
iptables -A OUTPUT -m set --match-set allowed-domains dst -j ACCEPT

# Explicitly REJECT all other outbound traffic for immediate feedback
iptables -A OUTPUT -j REJECT --reject-with icmp-admin-prohibited
log "Step 11 complete."

log "Step 12: Verifying firewall rules..."
if curl --connect-timeout 5 https://example.com >/dev/null 2>&1; then
    log "ERROR: Firewall verification failed - was able to reach https://example.com"
    exit 1
else
    log "Firewall verification passed - unable to reach https://example.com as expected"
fi

# Verify GitHub API access
if ! curl --connect-timeout 5 https://api.github.com/zen >/dev/null 2>&1; then
    log "ERROR: Firewall verification failed - unable to reach https://api.github.com"
    exit 1
else
    log "Firewall verification passed - able to reach https://api.github.com as expected"
fi

log "=== Firewall initialization complete ==="
