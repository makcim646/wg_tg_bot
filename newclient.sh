#!/bin/bash

new_client_setup () {
	# Given a list of the assigned internal IPv4 addresses, obtain the lowest still
	# available octet. Important to start looking at 2, because 1 is our gateway.
	octet=2
	#echo $yggsubnet $octet
	while grep AllowedIPs /etc/wireguard/wg0.conf | cut -d "." -f 4 | cut -d "/" -f 1 | grep -q "$octet"; do
		(( octet++ ))
	done
	# Don't break the WireGuard configuration in case the address space is full
	if [[ "$octet" -eq 255 ]]; then
		echo "253 clients are already configured. The WireGuard internal subnet is full!"
		exit
	fi
	yggsubnet=$(yggdrasilctl getSelf | grep "IPv6 subnet" | awk '{print $3}' | tr "//" " " | awk '{print $1}' | tr -d '\r\n')
	key=$(wg genkey)
	psk=$(wg genpsk)
	HOME_DIR="${PWD}"
	# Configure client in the server
	cat << EOF >> /etc/wireguard/wg0.conf
# BEGIN_PEER $CLIENT_NAME
[Peer]
PublicKey = $(wg pubkey <<< $key)
PresharedKey = $psk
AllowedIPs = 10.7.0.$octet/32, $yggsubnet$octet/128
# END_PEER $CLIENT_NAME
EOF
	# Create client configuration
	cat << EOF > "${HOME_DIR}/conf/${CLIENT_NAME}.conf"
[Interface]
Address = 10.7.0.$octet/24, $yggsubnet$octet/64
DNS = 300:6223::53, 8.8.8.8
PrivateKey = $key

[Peer]
PublicKey = $(grep PrivateKey /etc/wireguard/wg0.conf | cut -d " " -f 3 | wg pubkey)
PresharedKey = $psk
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = $(grep '^# ENDPOINT' /etc/wireguard/wg0.conf | cut -d " " -f 3):$(grep ListenPort /etc/wireguard/wg0.conf | cut -d " " -f 3)
PersistentKeepalive = 25
EOF

qrencode  -l L <"${HOME_DIR}/conf/${CLIENT_NAME}.conf" -o "png/${CLIENT_NAME}.png"
}

CLIENT_NAME=$1
new_client_setup
wg addconf wg0 <(sed -n "/^# BEGIN_PEER $CLIENT_NAME/,/^# END_PEER $CLIENT_NAME/p" /etc/wireguard/wg0.conf)
