## Introduction

This python code zips a files in a certain location and sends it through SFTP to another device. It automatically scans the target device using the MAC address by utilizing the `arp` command in Linux. I used it to organize the code I need to update on locations that does not have Internet connection. Sort of an automation script.

## Usage

You can easily configure the config file for your purpose since it has intuitive names. The code is meant to run on Linux. Configure the config file and set up ssh on both source device and target device to allow inbound and outbound traffic. Then, 
`sudo chmod +x main.py`
`main.py`

## Limitation

This code is written assuming that you are  connected to the source device via ssh. 
