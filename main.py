import requests
import json
from anticaptchaofficial.hcaptchaproxyless import *
from twocaptcha import TwoCaptcha
import threading, json
import string
import random

import tls_client

from colorama import Fore,Style

import websocket
import os
import ctypes
import time

def len_token():
    while True:
        time.sleep(0.01)
        Title = f"Token generated : {token_len} | Error Found : {error} | Total : {total}"
        ctypes.windll.kernel32.SetConsoleTitleW(Title)

def purplepink(text):
    os.system(""); faded = ""
    red = 40
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
        if not red == 255:
            red += 15
            if red > 255:
                red = 255
    return faded

def purple(text):
    os.system("")
    faded = ""
    down = False

    for line in text.splitlines():
        red = 40
        for character in line:
            if down:
                red -= 3
            else:
                red += 3
            if red > 254:
                red = 255
                down = True
            elif red < 1:
                red = 30
                down = False
            faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
    return faded
error = 0
total = 0
token_len = 0
ctypes.windll.kernel32.SetConsoleTitleW("[>] SIMON TOKEN GEN")
banner = """
\n
╔╦╗╔═╗╦╔═╔═╗╔╗╔  ╔═╗╔═╗╔╗╔
 ║ ║ ║╠╩╗║╣ ║║║  ║ ╦║╣ ║║║
 ╩ ╚═╝╩ ╩╚═╝╝╚╝  ╚═╝╚═╝╝╚╝                                                                      
\n\n"""

print(purplepink(banner))

invite = input(Fore.LIGHTMAGENTA_EX + ('        [>] Enter The Invite Code :'))
name = input(Fore.LIGHTMAGENTA_EX + ('        [>] Enter The Token Name : '))
thread = input(Fore.LIGHTMAGENTA_EX + ('        [>] Enter The Number Of Threads: '))

threading.Thread(target=len_token).start()
config_json = open('config.json', encoding = 'utf-8')
config = json.load(config_json)


def solve_cap():

    if config['SIMONTOKENGEN']['captcha'] == "anticaptcha":
        solver = hCaptchaProxyless()
        solver.set_key(config['SIMONTOKENGEN']['anticaptcha'])
        solver.set_website_url("https://discord.com/")
        solver.set_website_key("4c672d35-0701-42b2-88c3-78380b0db560")
        g_response = solver.solve_and_return_solution()
        if g_response != 0:
            return g_response
        
    if config['SIMONTOKENGEN']['captcha'] == "twocaptcha":
        solver = TwoCaptcha(config['SIMONTOKENGEN']['twocaptcha'])
        result = solver.hcaptcha(sitekey='4c672d35-0701-42b2-88c3-78380b0db560', url='https://discord.com/')
        return result




def joiner():
    global total, error, token_len
    while True:
        proxy = random.choice(open('proxies.txt','r').readlines())
        proxy = str(proxy).strip('\n').replace(' ','')


        session = tls_client.Session(client_identifier='chrome_105')

        request_url = "https://discord.com/api/v9/experiments?with_guild_experiments=true"

        try: 
            r = session.get(request_url, proxy=f'http://{proxy}')
        except:
            continue
        
        fingerprint = r.json()['fingerprint']

        captcha_token = solve_cap()

        string_pool = string.ascii_letters

        password = ""

        for i in range(10) :
            password += random.choice(string_pool)

        email = ""

        for i in range(10) :
            email += random.choice(string_pool)
        email = email + "@gmail.com"

        try:

            r = session.post('https://discord.com/api/v9/auth/register',json={

                'captcha_key': str(captcha_token),

                'consent': True,

                "gift_code_sku_id": "null",

                'invite': invite,

                'fingerprint': fingerprint,

                'username': name,

                'date_of_birth' : f'{str(random.randrange(1988,2007))}-{str(random.randrange(1,13))}-{str(random.randrange(1,20))}',

                'email' : email,

                'password' : password

            },headers={

                'origin': 'https://discord.com',

                'referer': f'https://discord.gg/{invite}',

                'x-discord-locale': 'en-US',

                'x-debug-options': 'bugReporterEnabled',

                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',

                'x-fingerprint': fingerprint,

                'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6Im5sLU5MIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwOC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA4LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE3MTg0MiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='

            }, proxy=f'http://{proxy}'

            )

        except:
            total += 1
            error += 1
            print(r.json())
            print(Fore.WHITE + '[' + Fore.RED + 'TOKEN GEN FALL' + Fore.WHITE + ']' + Fore.RED)
            continue

        if "token" in r.text:
            token = r.json()['token']
            total += 1
            token_len += 1
            print(Fore.WHITE + '[' + Fore.GREEN + 'TOKEN GEN SUCCESS' + Fore.WHITE + ']' + Fore.WHITE + ":" + token)
            
            continue


os.system('cls')

print(purplepink(banner))

for i in range(int(thread)):
    time.sleep(0.1)
    threading.Thread(target=joiner).start()


