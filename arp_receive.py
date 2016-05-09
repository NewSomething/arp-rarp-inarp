#!/usr/bin/python3

import socket
import struct
import binascii
import netifaces as ni
import arp_core


if __name__ == "__main__":
	
	count = 0
	
	# RawSocket
	#
	#
	rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
	
	try:
		while True:
			# Receive packet
			#
			#
			#
			packet = rawSocket.recvfrom(2048)
			
			
			# Unpack Ethernet header
			#
			#
			#			
			ethernet_header = packet[0][0:14]
			ethernet_layer = struct.unpack("!6s6s2s", ethernet_header)
			
			# ARP packet filter
			#
			#
			#
			ethernet_type = binascii.hexlify(ethernet_layer[2]).decode('ascii')
			if ethernet_type == "0806" or ethernet_type == "8035":
				
				# Unpack ARP header
				#
				#
				#
				arp_header = packet[0][14:42]
				arp_layer = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
				
				# Decode packet
				#
				#
				#
				
				# Ethernet Layer
				dest_mac   = "%x:%x:%x:%x:%x:%x" % struct.unpack("BBBBBB", ethernet_layer[0])
				source_mac = "%x:%x:%x:%x:%x:%x" % struct.unpack("BBBBBB", ethernet_layer[1])
				
				# ARP Layer
				hardware_type = binascii.hexlify(arp_layer[0]).decode('ascii')
				protocol_type = binascii.hexlify(arp_layer[1]).decode('ascii')
				hardware_size = binascii.hexlify(arp_layer[2]).decode('ascii')
				protocol_size = binascii.hexlify(arp_layer[3]).decode('ascii')
				opcode        = binascii.hexlify(arp_layer[4]).decode('ascii')
				sender_mac    = "%x:%x:%x:%x:%x:%x" % struct.unpack("BBBBBB",ethernet_layer[0])
				sender_ip     = socket.inet_ntoa(arp_layer[6])
				target_mac    = "%x:%x:%x:%x:%x:%x" % struct.unpack("BBBBBB",ethernet_layer[0])
				target_ip     = socket.inet_ntoa(arp_layer[8])
				
				
				# Packet Information
				#
				#
				#
				#
				print()
				
				count = count + 1
				print("Packet {0}".format(count))
				print()
				
				print("****************_ETHERNET_FRAME_****************")
				
				print("Dest MAC        :", dest_mac)
				print("Source MAC      :", source_mac)
				print("Type            :", ethernet_type)
				
				print("******************_ARP_HEADER_******************")
				
				print("Hardware type   :", hardware_type)
				print("Protocol type   :", protocol_type)
				print("Hardware size   :", hardware_size)
				print("Protocol size   :", protocol_size)
				print("Opcode          :", opcode)
				print("Sender MAC      :", sender_mac)
				print("Sender IP       :", sender_ip)
				print("Target MAC      :", target_mac)
				print("Target IP       :", target_ip)
				
				print("*************************************************")
				
				print()
				
				# ARP Request Filter
				#
				#
				#
				if opcode == "1":
					
					# Network Interfaces
					#
					#
					#
					network_interfaces = arp_core.Interfaces()
					
					for network_interface in network_interfaces:
						
						# MAC Addresses
						#
						#
						#
						interface_ip_addresses = arp_core.InterfaceMacAddresses(network_interface)
						
						if target_ip in interface_ip_addresses:
							
							# Send reply packet
							#
							#
							#
							arp_core.SendArpReplyPacket()
			
	except:
		pass