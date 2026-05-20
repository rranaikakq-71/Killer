# logger.py
# NEUTRONNNN_KILLER - COMPLETE LOGGING SYSTEM
# CHUMT KE PYASA, har ek activity log hogi!

import logging
import os
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

# Try to import config
try:
    from config import FileConfig, UserConfig
except ImportError:
    class FileConfig:
        LOG_FILE = "attack_logs.txt"
        ERROR_LOG_FILE = "error_logs.txt"
        ATTACK_STATS_FILE = "attack_stats.json"
        BASE_DIR = "."
    
    class UserConfig:
        SAVE_ATTACK_LOGS = True
        SAVE_ERROR_LOGS = True
        MAX_LOG_SIZE_MB = 10

# ============================================
# LOGGER SETUP
# ============================================

def setup_logger(
    name: str = "NEUTRONNNN_KILLER",
    log_file: str = None,
    level: int = logging.INFO,
    console_output: bool = True
) -> logging.Logger:
    """
    Setup and configure logger
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level
        console_output: Print to console
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file and UserConfig.SAVE_ATTACK_LOGS:
        try:
            # Ensure directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not create file handler: {e}")
    
    return logger

# ============================================
# ATTACK LOGGER
# ============================================

class AttackLogger:
    """
    Specialized logger for attack operations
    """
    
    def __init__(self):
        self.logger = setup_logger(
            "AttackLogger",
            FileConfig.LOG_FILE if UserConfig.SAVE_ATTACK_LOGS else None,
            logging.INFO
        )
        self.attack_stats = []
        self.current_attack = None
    
    def log_attack_start(self, meet_url: str, proxy_count: int, mode: str = "burst"):
        """
        Log attack start
        """
        self.current_attack = {
            'attack_id': datetime.now().strftime('%Y%m%d_%H%M%S_%f'),
            'start_time': datetime.now().isoformat(),
            'meet_url': meet_url,
            'proxy_count': proxy_count,
            'mode': mode,
            'status': 'started'
        }
        
        self.logger.info("=" * 60)
        self.logger.info("💀 ATTACK STARTED 💀")
        self.logger.info(f"   Target: {meet_url}")
        self.logger.info(f"   Proxies: {proxy_count}")
        self.logger.info(f"   Mode: {mode.upper()}")
        self.logger.info("=" * 60)
    
    def log_attack_progress(self, current: int, total: int, success: int, failed: int):
        """
        Log attack progress
        """
        percent = (current / total) * 100 if total > 0 else 0
        self.logger.info(f"   Progress: {current}/{total} ({percent:.1f}%) | Success: {success} | Failed: {failed}")
    
    def log_attack_complete(self, result: Dict):
        """
        Log attack completion
        """
        if not self.current_attack:
            return
        
        self.current_attack['end_time'] = datetime.now().isoformat()
        self.current_attack['status'] = 'completed' if result.get('success') else 'partial'
        self.current_attack['result'] = result
        
        self.logger.info("=" * 60)
        self.logger.info("💀 ATTACK COMPLETED 💀")
        self.logger.info(f"   Status: {'SUCCESS' if result.get('success') else 'PARTIAL'}")
        self.logger.info(f"   Total Requests: {result.get('total_requests', 0)}")
        self.logger.info(f"   Successful: {result.get('successful', 0)}")
        self.logger.info(f"   Failed: {result.get('failed', 0)}")
        self.logger.info(f"   Duration: {result.get('duration_seconds', 0)} seconds")
        self.logger.info(f"   Requests/sec: {result.get('requests_per_second', 0)}")
        self.logger.info("=" * 60)
        
        # Save to stats list
        self.attack_stats.append(self.current_attack)
        
        # Save to file
        self.save_stats()
        
        self.current_attack = None
    
    def log_attack_failed(self, error: str):
        """
        Log attack failure
        """
        if self.current_attack:
            self.current_attack['status'] = 'failed'
            self.current_attack['error'] = error
            self.current_attack['end_time'] = datetime.now().isoformat()
            
            self.logger.error("=" * 60)
            self.logger.error("❌ ATTACK FAILED ❌")
            self.logger.error(f"   Error: {error}")
            self.logger.error("=" * 60)
            
            self.attack_stats.append(self.current_attack)
            self.save_stats()
            self.current_attack = None
    
    def log_request(self, proxy: str, endpoint: str, status: int, duration: float):
        """
        Log individual request (debug level)
        """
        self.logger.debug(f"Request | Proxy: {proxy[:30]}... | Endpoint: {endpoint} | Status: {status} | Time: {duration:.2f}s")
    
    def log_error(self, error: str, details: Any = None):
        """
        Log error with details
        """
        self.logger.error(f"Error: {error}")
        if details:
            self.logger.debug(f"Details: {details}")
        
        # Also save to error log
        if UserConfig.SAVE_ERROR_LOGS:
            error_logger = setup_logger("ErrorLogger", FileConfig.ERROR_LOG_FILE, logging.ERROR, False)
            error_logger.error(f"{error} | Details: {details}")
    
    def save_stats(self):
        """
        Save attack statistics to JSON file
        """
        try:
            with open(FileConfig.ATTACK_STATS_FILE, 'w') as f:
                json.dump({
                    'total_attacks': len(self.attack_stats),
                    'last_updated': datetime.now().isoformat(),
                    'attacks': self.attack_stats[-50:]  # Keep last 50 attacks
                }, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save stats: {e}")
    
    def get_stats_summary(self) -> Dict:
        """
        Get summary of all attacks
        """
        if not self.attack_stats:
            return {'total_attacks': 0, 'successful_attacks': 0, 'failed_attacks': 0}
        
        successful = sum(1 for a in self.attack_stats if a.get('status') == 'completed')
        failed = sum(1 for a in self.attack_stats if a.get('status') == 'failed')
        
        return {
            'total_attacks': len(self.attack_stats),
            'successful_attacks': successful,
            'failed_attacks': failed,
            'success_rate': (successful / len(self.attack_stats)) * 100 if self.attack_stats else 0
        }

# ============================================
# PROXY LOGGER
# ============================================

class ProxyLogger:
    """
    Logger for proxy operations
    """
    
    def __init__(self):
        self.logger = setup_logger("ProxyLogger", None, logging.INFO)
    
    def log_proxy_check_start(self, total: int):
        """
        Log proxy check start
        """
        self.logger.info(f"🔍 Starting proxy check for {total} proxies...")
    
    def log_proxy_check_progress(self, checked: int, total: int, live: int):
        """
        Log proxy check progress
        """
        self.logger.debug(f"Proxy check: {checked}/{total} | Live: {live}")
    
    def log_proxy_check_complete(self, total: int, live: int, dead: int):
        """
        Log proxy check completion
        """
        self.logger.info(f"✅ Proxy check complete | Total: {total} | Live: {live} | Dead: {dead}")
    
    def log_proxy_saved(self, file_path: str, count: int):
        """
        Log proxy save
        """
        self.logger.info(f"💾 Saved {count} proxies to {file_path}")
    
    def log_proxy_loaded(self, file_path: str, count: int):
        """
        Log proxy load
        """
        self.logger.info(f"📁 Loaded {count} proxies from {file_path}")
    
    def log_invalid_proxy(self, proxy: str, reason: str):
        """
        Log invalid proxy
        """
        self.logger.debug(f"Invalid proxy: {proxy[:50]}... | Reason: {reason}")

# ============================================
# BOT LOGGER
# ============================================

class BotLogger:
    """
    Logger for bot operations
    """
    
    def __init__(self):
        self.logger = setup_logger("BotLogger", None, logging.INFO)
    
    def log_bot_start(self):
        """
        Log bot startup
        """
        self.logger.info("=" * 50)
        self.logger.info("🚀 NEUTRONNNN_KILLER Bot Started")
        self.logger.info(f"   Time: {datetime.now().isoformat()}")
        self.logger.info("=" * 50)
    
    def log_bot_stop(self):
        """
        Log bot shutdown
        """
        self.logger.info("=" * 50)
        self.logger.info("🛑 NEUTRONNNN_KILLER Bot Stopped")
        self.logger.info(f"   Time: {datetime.now().isoformat()}")
        self.logger.info("=" * 50)
    
    def log_user_action(self, user_id: int, action: str, details: str = None):
        """
        Log user action
        """
        self.logger.info(f"User {user_id} | Action: {action}" + (f" | Details: {details}" if details else ""))
    
    def log_command(self, user_id: int, command: str):
        """
        Log bot command
        """
        self.logger.info(f"User {user_id} | Command: {command}")
    
    def log_error(self, user_id: int, error: str):
        """
        Log user error
        """
        self.logger.error(f"User {user_id} | Error: {error}")

# ============================================
# MAIN LOGGER - SINGLETON
# ============================================

class MainLogger:
    """
    Main logger instance - use this for all logging
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.attack_logger = AttackLogger()
        self.proxy_logger = ProxyLogger()
        self.bot_logger = BotLogger()
        self.main_logger = setup_logger("MainLogger", None, logging.INFO)
    
    def get_attack_logger(self) -> AttackLogger:
        return self.attack_logger
    
    def get_proxy_logger(self) -> ProxyLogger:
        return self.proxy_logger
    
    def get_bot_logger(self) -> BotLogger:
        return self.bot_logger
    
    def info(self, message: str):
        self.main_logger.info(message)
    
    def error(self, message: str):
        self.main_logger.error(message)
    
    def warning(self, message: str):
        self.main_logger.warning(message)
    
    def debug(self, message: str):
        self.main_logger.debug(message)

# ============================================
# CONVENIENCE FUNCTIONS
# ============================================

def get_logger() -> MainLogger:
    """
    Get the main logger instance
    """
    return MainLogger()

def log_attack_start(meet_url: str, proxy_count: int, mode: str = "burst"):
    get_logger().get_attack_logger().log_attack_start(meet_url, proxy_count, mode)

def log_attack_complete(result: Dict):
    get_logger().get_attack_logger().log_attack_complete(result)

def log_attack_failed(error: str):
    get_logger().get_attack_logger().log_attack_failed(error)

def log_proxy_check_start(total: int):
    get_logger().get_proxy_logger().log_proxy_check_start(total)

def log_proxy_check_complete(total: int, live: int, dead: int):
    get_logger().get_proxy_logger().log_proxy_check_complete(total, live, dead)

def log_bot_start():
    get_logger().get_bot_logger().log_bot_start()

def log_bot_stop():
    get_logger().get_bot_logger().log_bot_stop()

# ============================================
# TEST FUNCTION
# ============================================

def test_logger():
    """
    Test the logging system
    """
    print("\n🧪 Testing Logger System...")
    print("=" * 50)
    
    # Test main logger
    logger = get_logger()
    
    print("\n📝 Test 1: Basic Logging")
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")
    
    print("\n📝 Test 2: Attack Logging")
    log_attack_start("https://meet.google.com/test-123", 50, "burst")
    log_attack_complete({
        'success': True,
        'total_requests': 500,
        'successful': 450,
        'failed': 50,
        'duration_seconds': 5.5,
        'requests_per_second': 90.9
    })
    
    print("\n📝 Test 3: Proxy Logging")
    log_proxy_check_start(100)
    log_proxy_check_complete(100, 75, 25)
    
    print("\n📝 Test 4: Bot Logging")
    log_bot_start()
    logger.get_bot_logger().log_user_action(123456789, "START_BOT")
    logger.get_bot_logger().log_command(123456789, "/attack")
    log_bot_stop()
    
    print("\n📝 Test 5: Stats Summary")
    stats = logger.get_attack_logger().get_stats_summary()
    print(f"   Total Attacks: {stats['total_attacks']}")
    print(f"   Successful: {stats['successful_attacks']}")
    print(f"   Failed: {stats['failed_attacks']}")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")
    
    print("\n✅ Logger tests completed!")
    print(f"📁 Log file: {FileConfig.LOG_FILE}")
    print(f"📁 Error log: {FileConfig.ERROR_LOG_FILE}")
    print(f"📁 Stats file: {FileConfig.ATTACK_STATS_FILE}")

if __name__ == "__main__":
    test_logger()