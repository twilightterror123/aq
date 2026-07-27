import os, sys, json, time, re, socket
import requests, base64, random, string, hashlib, subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

VERSION = "2.0"
AUTHOR = "108% Team"
C = type('C', (), {
    'BLUE': '\033[94m', 'CYAN': '\033[96m',
    'WHITE': '\033[97m', 'DARK': '\033[90m',
    'END': '\033[0m', 'BOLD': '\033[1m'
})()

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"""{C.BLUE}
{'='*60}
{C.CYAN}
 
 █████╗  ██████╗ ██╗   ██╗ █████╗     ████████╗ ██████╗  ██████╗ ██╗
██╔══██╗██╔═══██╗██║   ██║██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
███████║██║   ██║██║   ██║███████║       ██║   ██║   ██║██║   ██║██║
██╔══██║██║▄▄ ██║██║   ██║██╔══██║       ██║   ██║   ██║██║   ██║██║
██║  ██║╚██████╔╝╚██████╔╝██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
                 TOOLWAS MADE BY TWILIGHT TERROR
                    https://discord.gg/wfARcwngW3
                        AQUA Owner is AQ ! 𝘅𝘃𝗿
{C.BLUE}
{'='*60}{C.END}""")

def loading_bar(s=1, t="Loading"):
    for i in range(21):
        print(f"\r{C.CYAN}{t}: [{'#'*i}{'.'*(20-i)}] {i*5}%{C.END}", end="")
        time.sleep(s/20)
    print()

def inp(o, p="> "):
    print()
    for k,v in o.items(): print(f"{C.BLUE}  [{k}]{C.CYAN} {v}{C.END}")
    return input(f"{C.CYAN}{p}{C.END}").strip().lower()

def pi(t): print(f"{C.BLUE}  [i]{C.CYAN} {t}{C.END}")
def po(t): print(f"{C.BLUE}  [+]{C.CYAN} {t}{C.END}")
def pw(t): print(f"{C.BLUE}  [!]{C.CYAN} {t}{C.END}")
def pf(t): print(f"{C.BLUE}  [x]{C.CYAN} {t}{C.END}")

def info():
    clear()
    print(f"{C.BLUE}[ INFO ]{C.CYAN}\n  Tool: 108% TOOL v{VERSION}\n  Author: {AUTHOR}\n  Purpose: Authorized penetration testing{C.END}")
    input(f"{C.CYAN}Press Enter...{C.END}")

def sql_scan():
    clear()
    print(f"{C.BLUE}[ SQL Vulnerability Scanner ]{C.END}\n")
    url = input(f"{C.CYAN}Target URL: {C.END}")
    payloads = ["'", '"', "1' OR '1'='1", '1" OR "1"="1', "' OR 1=1 --", "admin' --", "' UNION SELECT 1,2,3 --", "1' AND 1=1 --"]
    errs = ['sql', 'mysql', 'syntax error', 'unclosed', 'quotation mark', 'odbc', 'microsoft ole db', 'oracle', 'postgresql']
    print(f"\n{C.BLUE}[+]{C.CYAN} Testing {url}...{C.END}\n")
    v = False
    for p in payloads:
        try:
            u = url + p if '?' in url else url.replace('=', f'={p}', 1)
            r = requests.get(u, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            for e in errs:
                if e.lower() in r.text.lower():
                    pw(f"Potential SQLi: {u}")
                    print(f"  {C.DARK}Error: {e}{C.END}")
                    v = True; break
        except: pass
        time.sleep(0.3)
    if not v: po("No SQL vulnerabilities found")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def web_scan():
    clear()
    print(f"{C.BLUE}[ Website Scanner ]{C.END}\n")
    url = input(f"{C.CYAN}Target URL: {C.END}")
    if not url.startswith('http'): url = 'https://' + url
    print(f"\n{C.BLUE}[+]{C.CYAN} Scanning {url}...{C.END}\n")
    try:
        r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        h = r.headers
        pi(f"URL: {url}\nStatus: {r.status_code}\nServer: {h.get('Server','Unknown')}\nSize: {len(r.text)} Bytes")
        print(f"\n{C.DARK}Security Headers:{C.END}")
        pi(f"X-Content-Type-Options: {h.get('X-Content-Type-Options','Not set')}")
        pi(f"X-Frame-Options: {h.get('X-Frame-Options','Not set')}")
        pi(f"HSTS: {h.get('Strict-Transport-Security','Not set')[:50]}")
        pi(f"CSP: {h.get('Content-Security-Policy','Not set')[:50]}")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def url_scan():
    clear()
    print(f"{C.BLUE}[ URL Scanner ]{C.END}\n")
    url = input(f"{C.CYAN}Target URL: {C.END}")
    if not url.startswith('http'): url = 'https://' + url
    print(f"\n{C.BLUE}[+]{C.CYAN} Extracting URLs from {url}...{C.END}\n")
    try:
        r = requests.get(url, timeout=10)
        urls = [u for u in re.findall(r'href=[\'"]?([^\'" >]+)', r.text) if u.startswith('http')][:30]
        for u in urls: print(f"  {C.BLUE}->{C.CYAN} {u}{C.END}")
        po(f"{len(urls)} URLs found")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def ip_scan():
    clear()
    print(f"{C.BLUE}[ IP Scanner ]{C.END}\n")
    t = input(f"{C.CYAN}Target (IP/Domain): {C.END}")
    try:
        ip = socket.gethostbyname(t)
        pi(f"Domain: {t}\nIP: {ip}")
        r = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()
        if r.get('status') == 'success':
            pi(f"City: {r.get('city','N/A')}\nCountry: {r.get('country','N/A')}\nISP: {r.get('isp','N/A')}\nCoords: {r.get('lat','N/A')}, {r.get('lon','N/A')}")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def port_scan():
    clear()
    print(f"{C.BLUE}[ Port Scanner ]{C.END}\n")
    t = input(f"{C.CYAN}Target (IP/Domain): {C.END}")
    ports = [21,22,23,25,53,80,110,139,143,443,445,993,995,1433,1521,2049,3306,3389,5432,5900,6379,8080,8443,9090,27017]
    print(f"\n{C.BLUE}[+]{C.CYAN} Scanning {t} on {len(ports)} ports...{C.END}\n")
    try:
        ip = socket.gethostbyname(t); open_ports = []
        def sp(p):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((ip, p)) == 0: open_ports.append(p)
            s.close()
        with ThreadPoolExecutor(max_workers=50) as e: e.map(sp, ports)
        if open_ports:
            pw(f"Open ports ({len(open_ports)}):")
            for p in sorted(open_ports):
                try: sv = socket.getservbyport(p, 'tcp')
                except: sv = 'unknown'
                print(f"  {C.BLUE}-{C.CYAN} {p}/tcp - {sv}{C.END}")
        else: po("No open ports found")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def pinger():
    clear()
    print(f"{C.BLUE}[ Pinger ]{C.END}\n")
    t = input(f"{C.CYAN}Target: {C.END}")
    c = input(f"{C.CYAN}Count (Enter=4): {C.END}")
    c = int(c) if c.isdigit() else 4
    print(f"\n{C.BLUE}[+]{C.CYAN} Pinging {t} ({c}x)...{C.END}\n")
    try:
        flag = '-n' if os.name == 'nt' else '-c'
        r = subprocess.run(['ping', flag, str(c), t], capture_output=True, text=True, timeout=30)
        print(f"{C.CYAN}{r.stdout[-500:] if len(r.stdout)>500 else r.stdout}{C.END}")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def dox_create():
    clear()
    print(f"{C.BLUE}[ Dox Creator ]{C.END}\n")
    d = {k: input(f"{C.CYAN}{k}: {C.END}") for k in ['Name','Age','City','Country','Email','Phone','IP','Social Media','Employer','School/Uni','Notes']}
    fn = f"dox_{d['Name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(f"{'='*40}\nDOX - {datetime.now().strftime('%d.%m.%Y %H:%M')}\n{'='*40}\n\n")
        f.writelines(f"{k.upper()}: {v}\n" for k,v in d.items() if v)
    po(f"Saved: {fn}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def dox_track():
    clear()
    print(f"{C.BLUE}[ Dox Tracker ]{C.END}\n")
    files = [f for f in os.listdir('.') if f.startswith('dox_') and f.endswith('.txt')]
    if files:
        pi(f"{len(files)} dox files:\n")
        for f in files: pi(f"{f} ({os.path.getsize(f)} Bytes) - {datetime.fromtimestamp(os.path.getmtime(f)).strftime('%d.%m.%Y %H:%M')}")
    else: pw("No dox files found")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def exif():
    clear()
    print(f"{C.BLUE}[ EXIF Reader ]{C.END}\n")
    p = input(f"{C.CYAN}Path: {C.END}")
    if not os.path.exists(p): pf("Not found"); input(f"\n{C.CYAN}Press Enter...{C.END}"); return
    print(f"\n{C.BLUE}[+]{C.CYAN} Reading {p}...{C.END}\n")
    try:
        s = os.stat(p)
        pi(f"File: {os.path.basename(p)}\nSize: {s.st_size} Bytes\nCreated: {datetime.fromtimestamp(s.st_ctime)}\nModified: {datetime.fromtimestamp(s.st_mtime)}")
        try:
            from PIL import Image, ExifTags
            ex = Image.open(p)._getexif()
            if ex:
                print(f"\n{C.DARK}EXIF:{C.END}")
                for tid,v in ex.items():
                    tag = ExifTags.TAGS.get(tid, tid)
                    if tag in ['Make','Model','DateTime','GPSInfo','Software','ExifImageWidth','ExifImageLength','ISOSpeedRatings','FNumber','ExposureTime','FocalLength']:
                        pi(f"{tag}: {v}")
            else: pw("No EXIF data")
        except ImportError: pw("Pillow not installed")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def dorking():
    clear()
    print(f"{C.BLUE}[ Google Dorking ]{C.END}\n")
    dorks = {'Admin Panels':['inurl:admin','inurl:login','intitle:admin'],'SQL Errors':['intext:"sql syntax error"','intext:"mysql_fetch"','intext:"ORA-00942"'],'Config Files':['filetype:env','filetype:sql','ext:cfg "database_password"'],'Log Files':['filetype:log "password"','filetype:log "admin"'],'Cameras':['inurl:view/index.shtml','intitle:"Live View / - AXIS"'],'WordPress':['inurl:wp-admin','inurl:wp-content/uploads']}
    cats = list(dorks.keys())
    for i,cat in enumerate(cats,1): print(f"{C.BLUE}  [{i}]{C.CYAN} {cat}{C.END}")
    print(f"{C.BLUE}  [{len(cats)+1}]{C.CYAN} Custom Dork\n  [0]{C.CYAN} Back{C.END}")
    c = input(f"\n{C.CYAN}> {C.END}")
    if c == '0': return
    if c == str(len(cats)+1):
        d = input(f"{C.CYAN}Dork: {C.END}")
        po(f"Dork: {d}\nhttps://www.google.com/search?q={d.replace(' ','+')}")
    elif c.isdigit() and 1<=int(c)<=len(cats):
        print(f"\n{C.CYAN}[{cats[int(c)-1]}]{C.END}")
        for d in dorks[cats[int(c)-1]]: print(f"\n{C.BLUE}->{C.CYAN} {d}{C.END}\nhttps://www.google.com/search?q={d.replace(' ','+')}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def user_track():
    clear()
    print(f"{C.BLUE}[ Username Tracker ]{C.END}\n")
    u = input(f"{C.CYAN}Username: {C.END}")
    sites = {'GitHub':f'https://github.com/{u}','Twitter/X':f'https://twitter.com/{u}','Instagram':f'https://instagram.com/{u}','Reddit':f'https://reddit.com/user/{u}','YouTube':f'https://youtube.com/@{u}','TikTok':f'https://tiktok.com/@{u}','Twitch':f'https://twitch.tv/{u}','Telegram':f'https://t.me/{u}','Steam':f'https://steamcommunity.com/id/{u}'}
    print(f"\n{C.BLUE}[+]{C.CYAN} Searching '{u}'...{C.END}\n")
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(requests.get, url, timeout=3, allow_redirects=True): site for site,url in sites.items()}
        for f in futs:
            try:
                r = f.result()
                po(f"{futs[f]}: {sites[futs[f]]}") if r.status_code==200 else pf(f"{futs[f]}: Not found ({r.status_code})")
            except: pf(f"{futs[f]}: Error")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def iplookup():
    clear()
    print(f"{C.BLUE}[ IP Lookup ]{C.END}\n")
    ip = input(f"{C.CYAN}IP: {C.END}")
    print(f"\n{C.BLUE}[+]{C.CYAN} Looking up {ip}...{C.END}\n")
    try:
        d = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()
        if d.get('status')=='success':
            pi(f"IP: {d.get('query','N/A')}\nCity: {d.get('city','N/A')}\nRegion: {d.get('regionName','N/A')}\nCountry: {d.get('country','N/A')}\nCoords: {d.get('lat','N/A')},{d.get('lon','N/A')}\nISP: {d.get('isp','N/A')}\nOrg: {d.get('org','N/A')}\nASN: {d.get('as','N/A')}\nZIP: {d.get('zip','N/A')}")
            if d.get('lat') and d.get('lon'): print(f"\n{C.BLUE}->{C.CYAN} Maps: https://www.google.com/maps?q={d['lat']},{d['lon']}{C.END}")
        else: pf("No data")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def phonelookup():
    clear()
    print(f"{C.BLUE}[ Phone Lookup ]{C.END}\n")
    p = input(f"{C.CYAN}Number (with country code): {C.END}")
    pw("No public API available. Manual search:\n")
    print(f"{C.BLUE}->{C.CYAN} https://www.google.com/search?q={p}\n{C.BLUE}->{C.CYAN} https://www.numlookup.com/{p}{C.END}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def ipgen():
    clear()
    print(f"{C.BLUE}[ IP Generator ]{C.END}\n")
    c = input(f"{C.CYAN}Count (Enter=10): {C.END}")
    c = int(c) if c.isdigit() else 10
    ips = [f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}" for _ in range(c)]
    for ip in ips: print(f"  {C.BLUE}-{C.CYAN} {ip}{C.END}")
    fn = f"ips_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(fn,'w') as f: f.write('\n'.join(ips))
    po(f"{c} IPs -> {fn}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def pwgen():
    clear()
    print(f"{C.BLUE}[ Password Generator ]{C.END}\n")
    l = input(f"{C.CYAN}Length (Enter=16): {C.END}")
    l = int(l) if l.isdigit() else 16
    pw = ''.join(random.choices(string.ascii_letters+string.digits+"!@#$%^&*()_+-=[]{}|;:',.<>?", k=l))
    print(f"\n{C.CYAN}Password ({l}):{C.END}\n{C.BLUE}  -> {C.CYAN}{pw}{C.END}")
    print(f"\n{C.DARK}Hashes:{C.END}")
    pi(f"MD5: {hashlib.md5(pw.encode()).hexdigest()}\nSHA1: {hashlib.sha1(pw.encode()).hexdigest()}\nSHA256: {hashlib.sha256(pw.encode()).hexdigest()}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def hashgen():
    clear()
    print(f"{C.BLUE}[ Hash Generator ]{C.END}\n")
    t = input(f"{C.CYAN}Text: {C.END}")
    print(f"\n{C.DARK}Text: {t}{C.END}\n")
    pi(f"MD5: {hashlib.md5(t.encode()).hexdigest()}\nSHA1: {hashlib.sha1(t.encode()).hexdigest()}\nSHA256: {hashlib.sha256(t.encode()).hexdigest()}\nSHA512: {hashlib.sha512(t.encode()).hexdigest()}\nBase64: {base64.b64encode(t.encode()).decode()}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def pwned():
    clear()
    print(f"{C.BLUE}[ HaveIBeenPwned ]{C.END}\n")
    e = input(f"{C.CYAN}Email: {C.END}")
    print(f"\n{C.BLUE}[+]{C.CYAN} Searching {e}...{C.END}\n")
    try:
        r = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{e}', headers={'hibp-api-key':''}, timeout=10)
        if r.status_code==200:
            d = r.json()
            pw(f"{len(d)} breaches found:\n")
            for b in d[:10]:
                print(f"{C.BLUE}  -----{C.END}")
                pi(f"Name: {b.get('Name','?')}\nDomain: {b.get('Domain','N/A')}\nDate: {b.get('BreachDate','N/A')}\nData: {', '.join(b.get('DataClasses',[]))}\n")
        elif r.status_code==404: po("No breaches found")
        else: pf(f"Error: {r.status_code}")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def dc_token():
    clear()
    print(f"{C.BLUE}[ Discord Token Info ]{C.END}\n")
    t = input(f"{C.CYAN}Token: {C.END}")
    h = {'Authorization':t,'User-Agent':'Mozilla/5.0'}
    print(f"\n{C.BLUE}[+]{C.CYAN} Requesting data...{C.END}\n")
    try:
        r = requests.get('https://discord.com/api/v9/users/@me', headers=h, timeout=5)
        if r.status_code==200:
            d = r.json()
            pi(f"User: {d.get('username','?')}#{d.get('discriminator','?')}\nID: {d.get('id','?')}\nEmail: {d.get('email','?')}\nPhone: {d.get('phone','?')}\n2FA: {'Yes' if d.get('mfa_enabled') else 'No'}\nNitro: {'Yes' if d.get('premium_type',0)>0 else 'No'}\nVerified: {'Yes' if d.get('verified') else 'No'}")
            try:
                b = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=h, timeout=5)
                if b.status_code==200 and b.json():
                    print(f"\n{C.DARK}Payment sources:{C.END}")
                    for s in b.json(): pi(f"{s.get('type','?')} - {s.get('brand','?')} (****{s.get('last_4','')})")
            except: pass
        else: pf(f"Invalid token ({r.status_code})")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def dc_webhook_info():
    clear()
    print(f"{C.BLUE}[ Webhook Info ]{C.END}\n")
    u = input(f"{C.CYAN}Webhook URL: {C.END}")
    print(f"\n{C.BLUE}[+]{C.CYAN} Loading data...{C.END}\n")
    try:
        d = requests.get(u, timeout=5).json()
        pi(f"Name: {d.get('name','?')}\nID: {d.get('id','?')}\nChannel: {d.get('channel_id','?')}\nGuild: {d.get('guild_id','?')}\nToken: {d.get('token','?')[:20]}...")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def dc_webhook_spam():
    clear()
    print(f"{C.BLUE}[ Webhook Spammer ]{C.END}\n")
    u = input(f"{C.CYAN}Webhook URL: {C.END}")
    m = input(f"{C.CYAN}Message: {C.END}")
    c = input(f"{C.CYAN}Count (Enter=10): {C.END}")
    c = int(c) if c.isdigit() else 10
    print(f"\n{C.BLUE}[+]{C.CYAN} Sending {c}x...{C.END}\n")
    for i in range(c):
        try:
            r = requests.post(u, json={'content':f'{m} [{i+1}/{c}]'}, timeout=5)
            po(f"[{i+1}/{c}] OK") if r.status_code==204 else pf(f"[{i+1}/{c}] {r.status_code}")
        except Exception as e: pf(f"[{i+1}/{c}] {e}")
        time.sleep(0.5)
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def dc_webhook_del():
    clear()
    print(f"{C.BLUE}[ Webhook Deleter ]{C.END}\n")
    u = input(f"{C.CYAN}Webhook URL: {C.END}")
    try:
        r = requests.delete(u, timeout=5)
        if r.status_code==204: po("Deleted")
        elif r.status_code==404: pw("Already deleted")
        else: pf(f"Error: {r.status_code}")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def dc_server():
    clear()
    print(f"{C.BLUE}[ Server Info ]{C.END}\n")
    i = input(f"{C.CYAN}Invite (discord.gg/xxx): {C.END}")
    if 'discord.gg/' in i: code = i.split('discord.gg/')[1]
    elif 'discord.com/invite/' in i: code = i.split('discord.com/invite/')[1]
    else: code = i
    print(f"\n{C.BLUE}[+]{C.CYAN} Loading {code}...{C.END}\n")
    try:
        d = requests.get(f'https://discord.com/api/v9/invites/{code}?with_counts=true', timeout=5).json()
        g = d.get('guild',{})
        pi(f"Name: {g.get('name','?')}\nID: {g.get('id','?')}\nMembers: ~{d.get('approximate_member_count','?')}\nOnline: ~{d.get('approximate_presence_count','?')}\n2FA: {'Yes' if g.get('mfa_level') else 'No'}\nBoost: Level {g.get('premium_tier',0)}")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def dc_nitro():
    clear()
    print(f"{C.BLUE}[ Nitro Generator ]{C.END}\n")
    c = input(f"{C.CYAN}Count (Enter=5): {C.END}")
    c = int(c) if c.isdigit() else 5
    print(f"\n{C.BLUE}[+]{C.CYAN} Generating {c} codes...{C.END}\n")
    pw("Random codes - mostly invalid.\n")
    for _ in range(c):
        code = ''.join(random.choices(string.ascii_letters+string.digits, k=24))
        pi(f"https://discord.gift/{code}")
        try:
            if requests.get(f'https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true', timeout=3).status_code==200:
                po("VALID!")
        except: pass
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def rb_cookie_login():
    clear()
    print(f"{C.BLUE}[ Roblox Cookie Check ]{C.END}\n")
    c = input(f"{C.CYAN}.ROBLOSECURITY: {C.END}")
    try:
        d = requests.get('https://www.roblox.com/mobileapi/userinfo', cookies={'.ROBLOSECURITY':c}, timeout=5).json()
        if d.get('UserName'):
            po("Cookie valid!")
            pi(f"User: {d.get('UserName','?')}\nID: {d.get('UserID','?')}\nRobux: {d.get('RobuxBalance','?')}\nPremium: {'Yes' if d.get('IsPremium') else 'No'}")
        else: pf("Cookie invalid")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def rb_cookie_info():
    clear()
    print(f"{C.BLUE}[ Roblox Cookie Info ]{C.END}\n")
    c = input(f"{C.CYAN}.ROBLOSECURITY: {C.END}")
    try:
        d = requests.get('https://www.roblox.com/mobileapi/userinfo', cookies={'.ROBLOSECURITY':c}, timeout=5).json()
        if d.get('UserName'):
            pi(f"Username: {d.get('UserName','?')}\nID: {d.get('UserID','?')}\nEmail: {d.get('Email','?')}\nRobux: {d.get('RobuxBalance','?')}\nPremium: {'Yes' if d.get('IsPremium') else 'No'}")
            fr = requests.get(f'https://friends.roblox.com/v1/users/{d["UserID"]}/friends/count', cookies={'.ROBLOSECURITY':c}, timeout=5)
            if fr.status_code==200: pi(f"Friends: {fr.json().get('count','?')}")
        else: pf("Cookie invalid")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def rb_user():
    clear()
    print(f"{C.BLUE}[ Roblox User Info ]{C.END}\n")
    uid = input(f"{C.CYAN}User ID: {C.END}")
    try:
        d = requests.get(f'https://users.roblox.com/v1/users/{uid}', timeout=5).json()
        if d.get('displayName'):
            pi(f"Username: {d.get('displayName','?')}\nDescription: {d.get('description','None')[:100]}\nCreated: {d.get('created','?')[:10]}\nVerified: {'Yes' if d.get('hasVerifiedBadge') else 'No'}\nProfile: https://www.roblox.com/users/{uid}/profile")
        else: pf("Not found")
    except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def rb_id():
    clear()
    print(f"{C.BLUE}[ Roblox ID <-> Username ]{C.END}\n")
    c = input(f"{C.CYAN}1=ID->Name | 2=Name->ID: {C.END}")
    if c=='1':
        uid = input(f"{C.CYAN}ID: {C.END}")
        try:
            d = requests.get(f'https://users.roblox.com/v1/users/{uid}', timeout=5).json()
            po(f"ID {uid} = {d.get('name','N/A')}") if d.get('name') else pf("Not found")
        except Exception as e: pf(f"Error: {e}")
    elif c=='2':
        n = input(f"{C.CYAN}Username: {C.END}")
        try:
            d = requests.post('https://users.roblox.com/v1/usernames/users', json={'usernames':[n],'excludeBannedUsers':False}, timeout=5).json().get('data',[])
            po(f"{n} = ID {d[0].get('id','?')}") if d else pf("Not found")
        except Exception as e: pf(f"Error: {e}")
    input(f"\n{C.CYAN}Press Enter...{C.END}")

def net_menu():
    while True:
        clear()
        print(f"{C.BLUE}[ NETWORK SCANNER ]{C.END}")
        c = inp({'1':'SQL Scanner','2':'Website Scanner','3':'URL Scanner','4':'IP Scanner','5':'Port Scanner','6':'Pinger','0':'Back'})
        if c=='1': sql_scan()
        elif c=='2': web_scan()
        elif c=='3': url_scan()
        elif c=='4': ip_scan()
        elif c=='5': port_scan()
        elif c=='6': pinger()
        elif c=='0': break

def osint_menu():
    while True:
        clear()
        print(f"{C.BLUE}[ OSINT ]{C.END}")
        c = inp({'1':'Dox Creator','2':'Dox Tracker','3':'EXIF Reader','4':'Google Dorking','5':'Username Tracker','6':'IP Lookup','7':'Phone Lookup','0':'Back'})
        if c=='1': dox_create()
        elif c=='2': dox_track()
        elif c=='3': exif()
        elif c=='4': dorking()
        elif c=='5': user_track()
        elif c=='6': iplookup()
        elif c=='7': phonelookup()
        elif c=='0': break

def util_menu():
    while True:
        clear()
        print(f"{C.BLUE}[ UTILITIES ]{C.END}")
        c = inp({'1':'IP Generator','2':'Password Generator','3':'Hash Generator','4':'HaveIBeenPwned','0':'Back'})
        if c=='1': ipgen()
        elif c=='2': pwgen()
        elif c=='3': hashgen()
        elif c=='4': pwned()
        elif c=='0': break

def dc_menu():
    while True:
        clear()
        print(f"{C.BLUE}[ DISCORD TOOLS ]{C.END}")
        c = inp({'1':'Token Info','2':'Webhook Info','3':'Webhook Spammer','4':'Webhook Deleter','5':'Server Info','6':'Nitro Generator','0':'Back'})
        if c=='1': dc_token()
        elif c=='2': dc_webhook_info()
        elif c=='3': dc_webhook_spam()
        elif c=='4': dc_webhook_del()
        elif c=='5': dc_server()
        elif c=='6': dc_nitro()
        elif c=='0': break

def rb_menu():
    while True:
        clear()
        print(f"{C.BLUE}[ ROBLOX TOOLS ]{C.END}")
        c = inp({'1':'Check Cookie','2':'Cookie Info','3':'User Info','4':'ID<->Name','0':'Back'})
        if c=='1': rb_cookie_login()
        elif c=='2': rb_cookie_info()
        elif c=='3': rb_user()
        elif c=='4': rb_id()
        elif c=='0': break

if __name__ == "__main__":
    try:
        while True:
            banner()
            print(f"{C.DARK}   Main Menu:{C.END}\n")
            print(f"{C.BLUE}   [1]{C.CYAN} Info\n   [2]{C.CYAN} Network Scanner\n   [3]{C.CYAN} OSINT\n   [4]{C.CYAN} Utilities\n   [5]{C.CYAN} Discord Tools\n   [6]{C.CYAN} Roblox Tools\n   [0]{C.CYAN} Exit{C.END}\n")
            c = input(f"{C.CYAN}> {C.END}").strip()
            if c == '1': info()
            elif c == '2': net_menu()
            elif c == '3': osint_menu()
            elif c == '4': util_menu()
            elif c == '5': dc_menu()
            elif c == '6': rb_menu()
            elif c == '0': clear(); print(f"\n{C.CYAN}Goodbye.{C.END}\n"); sys.exit(0)
    except KeyboardInterrupt: print(f"\n\n{C.CYAN}Aborted{C.END}"); sys.exit(0)
    except Exception as e: print(f"\n{C.CYAN}Error: {e}{C.END}"); sys.exit(1)
