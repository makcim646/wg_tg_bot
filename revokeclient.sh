#!/bin/bash
function revokeClient() {
	NUMBER_OF_CLIENTS=$(grep -c -E "^### Client" "/etc/wireguard/${SERVER_WG_NIC}.conf")
	if [[ ${NUMBER_OF_CLIENTS} == '0' ]]; then
		exit 1
	fi

	# remove [Peer] block matching $CLIENT_NAME
	sed -i "/^### Client ${CLIENT_NAME}\$/,/^$/d" "/etc/wireguard/${SERVER_WG_NIC}.conf"

	# remove generated client file
	HOME_DIR="${PWD}"
	rm -f "${HOME_DIR}/conf/${CLIENT_NAME}.conf"
	rm -f "${HOME_DIR}/png/${CLIENT_NAME}.png"

	# restart wireguard to apply changes
	wg syncconf "${SERVER_WG_NIC}" <(wg-quick strip "${SERVER_WG_NIC}")
}
source /etc/wireguard/params
CLIENT_NAME=$1
revokeClient
