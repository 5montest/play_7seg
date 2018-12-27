#!/usr/bin/python
# -*- coding: utf-8 -*-

import pigpio
import subprocess
import time

latch = 8
clock = 3
data = 9

#pigpio initalize
pi = pigpio.pi()
pi.set_mode(latch, pigpio.OUTPUT)
pi.set_mode(clock, pigpio.OUTPUT)
pi.set_mode(data, pigpio.OUTPUT)

pi.write(clock,0)
pi.write(data,0)
pi.write(latch,1)

#get ip_address
ip_show = "hostname -I"
ip = subprocess.check_output(ip_show.split()).strip()
print ip
#convert ip to byte
nTab = [0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90]
dTab = [0x40,0x79,0x24,0x30,0x19,0x12,0x02,0x58,0x00,0x10]

def send(bit):
  pi.write(latch,0)
  for i in range(8):
    pi.write(clock,0)
    output = (bit & 0b10000000) >> 7
    pi.write(data,output)
    bit = bit << 1
    pi.write(clock,1)
  pi.write(latch,1)
  time.sleep(sp)

#7seg initalize
for i in range(8):
  sp = 0.1
  send(0xff)

sp = 0.5

#get length
last = len(ip) - 1

#send signal
num = 0
for j in range(last - 2):
  if ip[last - num] == '.':
    ipbyte = dTab[ int(ip[last - num - 1]) ]
    num = num + 2
  else:
    ipbyte = nTab[ int(ip[last - num]) ]
    num = num + 1
  print ipbyte
  send(ipbyte)

for i in range(8):
  send(0xff)
