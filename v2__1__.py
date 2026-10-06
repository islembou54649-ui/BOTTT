"""
================================================================
Advanced Trading Signals Telegram Bot (Single File Version)
================================================================
Built with python-telegram-bot v22.8

Features:
- Mixed keyboard layout (2-1-2-1-2-1-2-1-2 pattern)
- 14 colored buttons (English) with DISTINCTIVE CUSTOM EMOJIS
- SQLite database for referrals
- Admin control panel
- Broadcast & signal sending to channel
- Welcome message + referral system
- Auto-fetches bot username on startup
- <tg-emoji emoji-id=\"5231101979903675433\">✨</tg-emoji> ALL EMOJIS ARE NOW PREMIUM COLORFUL CUSTOM EMOJIS <tg-emoji emoji-id=\"5231101979903675433\">✨</tg-emoji>
- <tg-emoji emoji-id=\"5298780919207844086\">✅</tg-emoji> FIXED: Callback query timeout error
- <tg-emoji emoji-id=\"5298780919207844086\">✅</tg-emoji> UPDATED: Future Signals icon (Neon Diamond)
- <tg-emoji emoji-id=\"5298780919207844086\">✅</tg-emoji> UPDATED: Token input from terminal

Just run: python bot.py
================================================================
"""

import logging
import os
import sys
import sqlite3
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode, KeyboardButtonStyle

# ============================================================
# 1) CONFIGURATION & PREMIUM COLORFUL CUSTOM EMOJI IDs
# ============================================================

# Bot token from terminal
BOT_TOKEN = input("Enter your bot token: ")
BOT_USERNAME = "QuantVexa_bot"

JOIN_CHANNEL_URL = "https://t.me/your_channel"
LIVE_CHART_URL = "https://www.tradingview.com/chart/"
QUOTEX_HUB_URL = "https://quotex.io/"
SIGNALS_CHANNEL_ID = "@your_signals_channel"
RESULTS_CHANNEL_URL = "https://t.me/your_results_channel"
SUPPORT_URL = "https://t.me/Siam_Trader5"
FREE_BOTS_URL = "https://t.me/your_free_bots"

WEBAPP_CHARTS_URL = "https://t.me/qxview_bot/Charts"
WEBAPP_BOTS_URL = "https://t.me/qxview_bot/Bots"
WEBAPP_SUPPORT_URL = "https://t.me/qxview_bot/support"
WEBAPP_PLANS_URL = "https://t.me/qxview_bot/planss"

ADMIN_IDS = [123456789]  # Replace with your Telegram user ID

# ✨ PREMIUM COLORFUL CUSTOM EMOJI IDs ✨
EMOJI_IDS = {
    # Main Menu - COLORFUL Selection
    "speaker": "5424818078833715060",      # 📣 NewsEmoji - Megaphone (Red/Orange)
    "chart": "5197503331215361533",        # 📈 FinanceEmoji - Chart (Green)
    "lightning": "5373066076558996568",    # ⚡ NeonEmoji - Lightning (Yellow Neon)
    "diamond": "5465283645788937267",      # 💎 NeonEmoji - Diamond (Blue/Purple Neon)
    "stats": "5190806721286657692",        # 📊 FinanceEmoji - Stats (Blue)
    "clock": "5431807687136395567",        # ⏰ CuteEmoji - Clock (Colorful)
    "gift": "5411271889421086677",         # 🎁 NeonEmoji - Gift Box (Neon)
    "money": "5373350287429872269",        # 💲 NeonEmoji - Dollar Sign (Green Neon)
    "crystal": "5465283645788937267",      # 💎 NeonEmoji - Diamond (Blue/Purple Neon) - UPDATED
    "clipboard": "5334882760735598374",    # 📝 FaceEmoji - Clipboard (Colorful)
    "link": "5375129357373165375",         # 🔗 TopicIcons - Link (Blue)
    "tools": "5462921117423384478",        # 🛠 GameEmoji - Tools (Colorful)
    "user": "5422683699130933153",         # 🪪 RestrictedEmoji - ID Card (Colorful)
    "headset": "5404350824501491839",      # 📞 NeonEmoji - Phone (Neon)
    "sos": "5429262837409138106",          # 🆘 CuteEmoji - SOS (Red)
    "house": "5465226866321268133",        # 🏠 RestrictedEmoji - House (Colorful)
    
    # Plans & Features
    "free": "5364112491381006601",         # 🆓 RestrictedEmoji - Free (Green)
    "calendar": "5364233403300330811",     # 📅 TopicIcons - Calendar (Red)
    "crown": "5348306023889254367",        # 👑 TopicIcons - Crown (Gold)
    "check": "5427009714745517609",        # ✅ RestrictedEmoji - Check (Green)
    "cross": "5465665476971471368",        # ❌ RestrictedEmoji - Cross (Red)
    
    # Modern Robot & Tech - PREMIUM
    "robot": "5465385711391752862",        # 🤖 HeartEmoji - Modern Robot (Colorful)
    "bell": "5361643005444899140",         # 🔔 TopicIcons - Bell (Gold)
    "newspaper": "5361740436778009413",    # 📰 TopicIcons - Newspaper (Colorful)
    "abacus": "5472404950673791399",       # 🧮 RestrictedEmoji - Abacus (Wood)
    "gem": "5348296214183950233",          # 💎 TopicIcons - Gem (Blue)
    "target": "5461009483314517035",       # 🎯 TONEmoji - Target (Red/White)
    "currency": "5471899089425667918",     # 💱 RestrictedEmoji - Currency (Green)
    
    # Effects & Status - PREMIUM
    "fire": "5373310043586310463",         # 🔥 NeonEmoji - Fire (Orange Neon)
    "warning": "5431445849026611010",      # ⚠️ CuteEmoji - Warning (Yellow)
    "star": "5408977655330517200",         # ⭐️ NeonEmoji - Star (Yellow Neon)
    "heart": "5429277624981538430",        # ❤️ CuteEmoji - Heart (Red)
    "rocket": "5361930420361378687",       # 🚀 TopicIcons - Rocket (Red/White)
    "coin": "5379600444098093058",         # 🪙 TopicIcons - Coin (Gold)
    "sparkles": "5472164874886846699",     # ✨ RestrictedEmoji - Sparkles (Yellow)
    "money_bag": "5375296873982604963",    # 💰 TopicIcons - Money Bag (Green)
    "trophy": "5345892905103932200",       # 🏆 TopicIcons - Trophy (Gold)
    "medal": "5345843457145453967",        # 🥇 TopicIcons - Medal (Gold)
    "unicorn": "5411459442052969769",      # 🦄 NeonEmoji - Unicorn (Colorful)
    
    # Additional button icons - PREMIUM DISTINCTIVE emojis
    "gear": "5267334530171169409",          # ⚙️ LoveDayEmoji - Settings (distinctive)
    "magnifier": "5231012545799666522",     # 🔍 NewsEmoji - Checker (distinctive)
    "globe": "5395330710280093235",         # 🌐 MovieIcons - Live Market (distinctive)
    "crystal_ball": "5458799228719472718",  # 🌟 RestrictedEmoji - Future Live (glowing star, non-white)
    "satellite": "5256134032852278918",     # 📡 LoveDayEmoji - Live Signal (premium)
    "bug": "5199544484358013013",           # 🐛 AnimalIcons - Bug Signal (distinctive)
    "person": "5373012449597335010",        # 👤 RestrictedEmoji - AI Filter
    "swirl": "5429187589582111255",         # 🌀 CuteEmoji - Formatter
    "swap": "5375338737028841420",          # 🔄 NewsEmoji - Swap C/P (distinctive)
    "alarm": "5386415655253730366",         # ⏰ CatPawsEmoji - TZ Converter (distinctive)
    "target_check": "5461009483314517035",  # 🎯 TONEmoji - Target (for checkers)
    "chart_market": "5197503331215361533",  # 📈 FinanceEmoji - Market FS (distinctive)
    "sparkle_premium": "5231101979903675433",  # ✨ SparklesEmoji - Whiteout/News (premium)
    "cross_premium": "5343968063970632884", # ❌ CandyFontEmoji - Blackout (distinctive)
    "calendar_premium": "5192784923093652913",  # 📅 MadEmoji2 - Schedule (distinctive)
    "stats_premium": "5190806721286657692", # 📊 FinanceEmoji - Market Filters (distinctive)
    "diamond_premium": "5283139309740765379",  # 💎 UnicornEmoji - Payouts (distinctive)
    "clock_premium": "5431807687136395567", # ⏰ CuteEmoji - Time Schedule (distinctive)
    "lightning_premium": "5373066076558996568",  # ⚡ NeonEmoji - Live Signal (neon animated)
    "balloon_premium": "5231339534544817038",    # 🎈 SparklesEmoji - Referral (sparkling)
    "lock": "5206432422194849059",               # 🔒 FaceEmoji - Lock (colored, distinctive)
    "lock_open": "5472308992514464048",          # 🔐 RestrictedEmoji - Open lock (colored)
}

# Helper function for TEXT messages (HTML format)
def emj(name, base_emoji=""):
    return f'<tg-emoji emoji-id="{EMOJI_IDS[name]}">{base_emoji}</tg-emoji>'

# ============================================================
# AUTO-LOADED EMOJI MAP (from Emoji.json - 7000+ premium emojis)
# ============================================================
import json as _json_module
_EMOJI_JSON_PATH = None
for _path in [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "Emoji.json"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "ايموجي"),
    os.path.join(os.getcwd(), "Emoji.json"),
    "Emoji.json",
]:
    if os.path.exists(_path):
        _EMOJI_JSON_PATH = _path
        break
_EMOJI_MAP_CACHE = {}  # base emoji -> custom_emoji_id
_EMOJI_MAP_LOADED = False

# ============================================================
# PREMIUM LUXURY EMOJI OVERRIDES (40 hand-picked premium emoji IDs)
# These are the user-specified "luxury" custom emojis that take
# HIGHEST PRIORITY over any other mapping from Emoji.json.
# ============================================================
_LUXURY_EMOJI_OVERRIDES = {
    "\U0001F606": "5323523560080158541",  # 😆 - Laughing with closed eyes
    "\U0001F605": "5199468807034253648",  # 😅 - Sweating smile
    "\U0001F60A": "5352899869369446268",  # 😊 - Smiling eyes
    "\U0001F609": "5339267587337370029",  # 😉 - Winking
    "\U0001F60D": "5217824874487101321",  # 😍 - Heart eyes
    "\U0001F618": "5307736407056331791",  # 😘 - Kissing heart
    "\U0001F61D": "5460631951394225073",  # 😝 - Squinting tongue
    "\U0001F928": "5352640560718949874",  # 🤨 - Raised eyebrow
    "\U0001F929": "5353025608832004653",  # 🤩 - Star struck
    "\U0001F973": "5197630131534836123",  # 🥳 - Partying face
    "\U0001F97A": "5458378137240877666",  # 🥺 - Pleading face
    "\U0001F622": "5323329096845897690",  # 😢 - Crying
    "\U0001F62D": "5339124569221377480",  # 😭 - Sobbing
    "\U0001F621": "5217467090826441505",  # 😡 - Pouting
    "\U0001F92F": "5197564405650307134",  # 🤯 - Exploding head
    "\U0001F976": "5197581306346617713",  # 🥶 - Cold face
    "\U0001F631": "5197706972794731241",  # 😱 - Screaming in fear
    "\U0001F628": "5460958179930158488",  # 😨 - Fearful
    "\U0001FAE2": "5197404349399054490",  # 🫢 - Hand over mouth
    "\U0001FAE1": "5323772371830588991",  # 🫡 - Saluting face
    "\U0001FAE0": "5197170531379459422",  # 🫠 - Melting face
    "\U0001F62C": "5352609143033180462",  # 😬 - Grimacing
    "\U0001F971": "5447445388183222331",  # 🥱 - Yawning
    "\U0001F634": "5341363621572128687",  # 😴 - Sleeping
    "\U0001F635": "5422649047334794716",  # 😵 - Dizzy
    "\U0001F635\u200D\U0001F4AB": "5296424506875722458",  # 😵‍💫 - Spiral eyes
    "\U0001F92E": "5384083969048325091",  # 🤮 - Vomiting
    "\U0001F911": "5436386989857320953",  # 🤑 - Money mouth
    "\U0001F608": "5197645099495862838",  # 😈 - Devil smile
    "\U0001F921": "5197188419918246648",  # 🤡 - Clown
    "\U0001F4A9": "5199763841222721243",  # 💩 - Pile of poo
    "\U0001F480": "5375407413555900550",  # 💀 - Skull
    "\U0001F44D": "5323547156630483403",  # 👍 - Thumbs up
    "\U0001F44E": "5197396124536682206",  # 👎 - Thumbs down
    "\U0001F44C": "5422446685655676792",  # 👌 - OK hand
    "\U0001F44B": "5199885118214255386",  # 👋 - Waving hand
    "\U0001F64F": "5458774648621643551",  # 🙏 - Folded hands
    "\U0001F645\u200D\u2642\uFE0F": "5422858869372104873",  # 🙅‍♂️ - Man gesturing no
    "\u2795": "5433805508353996553",      # ➕ - Plus
    "\U0001F4AF": "5447508713181034519",  # 💯 - Hundred points
}

# Fallback mapping for emojis NOT in Emoji.json (using existing EMOJI_IDS)
# These are manually mapped to suitable premium custom emojis from EMOJI_IDS.
_EMOJI_FALLBACK = {}

def _build_fallback():
    """Build fallback mapping from EMOJI_IDS for emojis not in Emoji.json."""
    global _EMOJI_FALLBACK
    _EMOJI_FALLBACK = {
        "\u23f9\ufe0f": EMOJI_IDS.get("tools", ""),       # ⏹️ stop -> tools
        "\u23f9": EMOJI_IDS.get("tools", ""),              # ⏹ stop -> tools
        "\U0001F194": EMOJI_IDS.get("user", ""),           # 🆔 ID -> ID card
        "\U0001F4CB": EMOJI_IDS.get("clipboard", ""),      # 📋 clipboard -> memo
        "\U0001F4DB": EMOJI_IDS.get("user", ""),           # 📛 name badge -> ID card
        "\U0001F535": EMOJI_IDS.get("link", ""),           # 🔵 blue circle -> blue link
    }

# Preference order for premium / colorful / animated categories
_EMOJI_CATEGORY_PREFERENCE = [
    "NeonEmoji", "SparklesEmoji", "GlowingFont", "EffectEmoji",
    "RestrictedEmoji", "TopicIcons", "TONEmoji", "FinanceEmoji",
    "CuteEmoji", "UnicornEmoji", "HandEmoji", "StarEmoji",
    "HeartEmoji", "FaceEmoji", "GameEmoji", "NewsEmoji",
    "ApplicationEmoji", "CrayonsEmoji", "KawaiiEmoji",
    "MadEmoji2", "MadEmoji", "ColorfulFontEmoji", "LedScreenEmoji",
    "PencilEmoji", "HandDrawnEmoji", "OutlineEmoji",
]

def _load_emoji_map():
    """Load Emoji.json once and build base-emoji -> custom_emoji_id mapping.
    The LUXURY emoji overrides take HIGHEST priority."""
    global _EMOJI_MAP_CACHE, _EMOJI_MAP_LOADED
    if _EMOJI_MAP_LOADED:
        return _EMOJI_MAP_CACHE
    _build_fallback()
    try:
        if not _EMOJI_JSON_PATH or not os.path.exists(_EMOJI_JSON_PATH):
            logging.warning("Emoji.json not found - using fallback emojis only")
            _EMOJI_MAP_LOADED = True
            return _EMOJI_MAP_CACHE
        with open(_EMOJI_JSON_PATH, "r", encoding="utf-8") as _f:
            _data = _json_module.load(_f)
        _candidates = {}
        for _cat, _cat_data in _data.items():
            for _entry in _cat_data.get("emoji", []):
                _emoji = _entry.get("emoji")
                _cid = _entry.get("custom_emoji_id")
                if _emoji and _cid:
                    _candidates.setdefault(_emoji, []).append((_cat, _cid))
        for _emoji, _opts in _candidates.items():
            _chosen = None
            for _pref in _EMOJI_CATEGORY_PREFERENCE:
                for _cat, _cid in _opts:
                    if _cat == _pref:
                        _chosen = _cid
                        break
                if _chosen:
                    break
            if not _chosen:
                _chosen = _opts[0][1]
            _EMOJI_MAP_CACHE[_emoji] = _chosen
        # Add fallback entries for emojis not in Emoji.json
        for _fb_emoji, _fb_cid in _EMOJI_FALLBACK.items():
            if _fb_emoji not in _EMOJI_MAP_CACHE and _fb_cid:
                _EMOJI_MAP_CACHE[_fb_emoji] = _fb_cid
        # ★ Apply LUXURY overrides LAST so they take HIGHEST priority ★
        _EMOJI_MAP_CACHE.update(_LUXURY_EMOJI_OVERRIDES)
        _EMOJI_MAP_LOADED = True
        logging.info(f"Loaded {len(_EMOJI_MAP_CACHE)} premium emojis from Emoji.json (incl. {len(_LUXURY_EMOJI_OVERRIDES)} luxury overrides)")
    except Exception as _e:
        logging.warning(f"Failed to load Emoji.json: {_e}")
        # Still apply luxury overrides even if Emoji.json fails
        _EMOJI_MAP_CACHE.update(_LUXURY_EMOJI_OVERRIDES)
        _EMOJI_MAP_LOADED = True
    return _EMOJI_MAP_CACHE

def e(base_emoji):
    """Wrap ANY plain emoji with a premium custom Telegram emoji.
    LUXURY emojis (40 hand-picked premium IDs) take highest priority.
    Falls back to the plain emoji if no mapping exists.
    Usage in f-strings: f"{e('\\U0001F44D')} text"
    """
    if not _EMOJI_MAP_LOADED:
        _load_emoji_map()
    _cid = _EMOJI_MAP_CACHE.get(base_emoji)
    if _cid:
        return f'<tg-emoji emoji-id="{_cid}">{base_emoji}</tg-emoji>'
    return base_emoji

def lux(name):
    """Directly use a LUXURY emoji by short name. Returns the wrapped HTML tag.
    Available luxury names: laugh, sweat_smile, smile_eyes, wink, heart_eyes,
    kiss, tongue, eyebrow, star_struck, party, pleading, cry, sob, angry,
    mind_blown, cold, scream, fear, hand_mouth, salute, melt, grimace,
    yawn, sleep, dizzy, spiral, vomit, money_mouth, devil, clown, poo,
    skull, thumbs_up, thumbs_down, ok_hand, wave, pray, no_man, plus, hundred.
    """
    _luxury_names = {
        "laugh":        ("\U0001F606", "5323523560080158541"),
        "sweat_smile":  ("\U0001F605", "5199468807034253648"),
        "smile_eyes":   ("\U0001F60A", "5352899869369446268"),
        "wink":         ("\U0001F609", "5339267587337370029"),
        "heart_eyes":   ("\U0001F60D", "5217824874487101321"),
        "kiss":         ("\U0001F618", "5307736407056331791"),
        "tongue":       ("\U0001F61D", "5460631951394225073"),
        "eyebrow":      ("\U0001F928", "5352640560718949874"),
        "star_struck":  ("\U0001F929", "5353025608832004653"),
        "party":        ("\U0001F973", "5197630131534836123"),
        "pleading":     ("\U0001F97A", "5458378137240877666"),
        "cry":          ("\U0001F622", "5323329096845897690"),
        "sob":          ("\U0001F62D", "5339124569221377480"),
        "angry":        ("\U0001F621", "5217467090826441505"),
        "mind_blown":   ("\U0001F92F", "5197564405650307134"),
        "cold":         ("\U0001F976", "5197581306346617713"),
        "scream":       ("\U0001F631", "5197706972794731241"),
        "fear":         ("\U0001F628", "5460958179930158488"),
        "hand_mouth":   ("\U0001FAE2", "5197404349399054490"),
        "salute":       ("\U0001FAE1", "5323772371830588991"),
        "melt":         ("\U0001FAE0", "5197170531379459422"),
        "grimace":      ("\U0001F62C", "5352609143033180462"),
        "yawn":         ("\U0001F971", "5447445388183222331"),
        "sleep":        ("\U0001F634", "5341363621572128687"),
        "dizzy":        ("\U0001F635", "5422649047334794716"),
        "spiral":       ("\U0001F635\u200D\U0001F4AB", "5296424506875722458"),
        "vomit":        ("\U0001F92E", "5384083969048325091"),
        "money_mouth":  ("\U0001F911", "5436386989857320953"),
        "devil":        ("\U0001F608", "5197645099495862838"),
        "clown":        ("\U0001F921", "5197188419918246648"),
        "poo":          ("\U0001F4A9", "5199763841222721243"),
        "skull":        ("\U0001F480", "5375407413555900550"),
        "thumbs_up":    ("\U0001F44D", "5323547156630483403"),
        "thumbs_down":  ("\U0001F44E", "5197396124536682206"),
        "ok_hand":      ("\U0001F44C", "5422446685655676792"),
        "wave":         ("\U0001F44B", "5199885118214255386"),
        "pray":         ("\U0001F64F", "5458774648621643551"),
        "no_man":       ("\U0001F645\u200D\u2642\uFE0F", "5422858869372104873"),
        "plus":         ("\u2795",     "5433805508353996553"),
        "hundred":      ("\U0001F4AF", "5447508713181034519"),
    }
    if name not in _luxury_names:
        return ""
    _emoji, _cid = _luxury_names[name]
    return f'<tg-emoji emoji-id="{_cid}">{_emoji}</tg-emoji>'

def lux_id(name):
    """Return ONLY the custom_emoji_id (string) for a luxury emoji by short name.
    Use this for InlineKeyboardButton(icon_custom_emoji_id=...).
    Available names: see lux() function docstring.
    """
    _luxury_names = {
        "laugh":        "5323523560080158541",
        "sweat_smile":  "5199468807034253648",
        "smile_eyes":   "5352899869369446268",
        "wink":         "5339267587337370029",
        "heart_eyes":   "5217824874487101321",
        "kiss":         "5307736407056331791",
        "tongue":       "5460631951394225073",
        "eyebrow":      "5352640560718949874",
        "star_struck":  "5353025608832004653",
        "party":        "5197630131534836123",
        "pleading":     "5458378137240877666",
        "cry":          "5323329096845897690",
        "sob":          "5339124569221377480",
        "angry":        "5217467090826441505",
        "mind_blown":   "5197564405650307134",
        "cold":         "5197581306346617713",
        "scream":       "5197706972794731241",
        "fear":         "5460958179930158488",
        "hand_mouth":   "5197404349399054490",
        "salute":       "5323772371830588991",
        "melt":         "5197170531379459422",
        "grimace":      "5352609143033180462",
        "yawn":         "5447445388183222331",
        "sleep":        "5341363621572128687",
        "dizzy":        "5422649047334794716",
        "spiral":       "5296424506875722458",
        "vomit":        "5384083969048325091",
        "money_mouth":  "5436386989857320953",
        "devil":        "5197645099495862838",
        "clown":        "5197188419918246648",
        "poo":          "5199763841222721243",
        "skull":        "5375407413555900550",
        "thumbs_up":    "5323547156630483403",
        "thumbs_down":  "5197396124536682206",
        "ok_hand":      "5422446685655676792",
        "wave":         "5199885118214255386",
        "pray":         "5458774648621643551",
        "no_man":       "5422858869372104873",
        "plus":         "5433805508353996553",
        "hundred":      "5447508713181034519",
    }
    return _luxury_names.get(name, "")



# Style aliases for native colored button backgrounds
STYLE_BLUE = KeyboardButtonStyle.PRIMARY
STYLE_GREEN = KeyboardButtonStyle.SUCCESS
STYLE_RED = KeyboardButtonStyle.DANGER

PLANS = [
    {"name": "Free Plan", "price": "$0", "duration": "7 days", "features": ["Limited signals (3 signals per day)", "Access to basic time list", "Bot-only support"]},
    {"name": "Weekly Plan", "price": "$15", "duration": "7 days", "features": ["Unlimited signals", "Full access to time list", "Instant alerts", "VIP support"]},
    {"name": "Monthly Plan", "price": "$45", "duration": "30 days", "features": ["All weekly plan features", "Top payout currencies analysis", "Exclusive future signals", "Weekly training sessions"]},
    {"name": "Gold Plan", "price": "$120", "duration": "90 days", "features": ["All monthly plan features", "Personal account manager", "Custom VIP signals", "Exclusive training workshops"]},
]

def validate_config():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN is not set!")
        return False
    return True

# ============================================================
# 2) DATABASE (SQLite)
# ============================================================
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, join_date TEXT, referrer_id INTEGER DEFAULT NULL, referral_count INTEGER DEFAULT 0, is_premium INTEGER DEFAULT 0, plan TEXT DEFAULT 'free')""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS referrals (id INTEGER PRIMARY KEY AUTOINCREMENT, referrer_id INTEGER, referred_id INTEGER, date TEXT, joined_channel INTEGER DEFAULT 0)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS signals (id INTEGER PRIMARY KEY AUTOINCREMENT, currency TEXT, direction TEXT, entry_price REAL, expiry TEXT, time TEXT, status TEXT DEFAULT 'pending')""")
    conn.commit()
    conn.close()

def add_user(user_id, username=None, first_name=None, referrer_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute("INSERT INTO users (user_id, username, first_name, join_date, referrer_id, referral_count, is_premium, plan) VALUES (?, ?, ?, ?, ?, 0, 0, 'free')", (user_id, username, first_name, datetime.now().isoformat(), referrer_id))
    if referrer_id and referrer_id != user_id:
        cursor.execute("SELECT id FROM referrals WHERE referrer_id = ? AND referred_id = ?", (referrer_id, user_id))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO referrals (referrer_id, referred_id, date, joined_channel) VALUES (?, ?, ?, 0)", (referrer_id, user_id, datetime.now().isoformat()))
            cursor.execute("UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?", (referrer_id,))
    conn.commit()
    conn.close()
    return True

def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_referral_count(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT referral_count FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def get_referrals_list(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT u.username, u.first_name, r.date, r.joined_channel FROM referrals r JOIN users u ON r.referred_id = u.user_id WHERE r.referrer_id = ? ORDER BY r.date DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_channel_join(user_id, joined=True):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE referrals SET joined_channel = ? WHERE referred_id = ?", (1 if joined else 0, user_id))
    conn.commit()
    conn.close()

def is_admin(user_id):
    return user_id in ADMIN_IDS

def add_signal(currency, direction, entry_price, expiry):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO signals (currency, direction, entry_price, expiry, time, status) VALUES (?, ?, ?, ?, ?, 'pending')", (currency, direction, entry_price, expiry, datetime.now().isoformat()))
    signal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return signal_id

def get_signals_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM signals GROUP BY status")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def get_all_users_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, first_name, join_date, referral_count, plan FROM users ORDER BY join_date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ============================================================
# 3) KEYBOARDS (Using icon_custom_emoji_id for buttons)
# ============================================================

def get_main_menu_keyboard():
    keyboard = [
        # === Quick Actions ===
        [
            InlineKeyboardButton("Join Channel", url=JOIN_CHANNEL_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["speaker"]),
            InlineKeyboardButton("Live Chart", url=WEBAPP_CHARTS_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["chart"]),
        ],
        # === Signals ===
        [
            InlineKeyboardButton("Current Signals", callback_data="current_signals", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
            InlineKeyboardButton("Live Future", callback_data="live_future", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["target_check"]),
        ],
        [
            InlineKeyboardButton("Live Signal", callback_data="live_signal", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["lightning_premium"]),
            InlineKeyboardButton("Bug Signal", callback_data="bug_signal", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["bug"]),
        ],
        # === Checkers ===
        [
            InlineKeyboardButton("Live Checker", callback_data="live_checker", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["magnifier"]),
            InlineKeyboardButton("OTC Checker", callback_data="otc_checker", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["magnifier"]),
        ],
        [
            InlineKeyboardButton("Blackout Checker", callback_data="blackout_checker", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["magnifier"]),
            InlineKeyboardButton("Whiteout Checker", callback_data="whiteout_checker", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["magnifier"]),
        ],
        # === Market Future Signals (FS) ===
        [
            InlineKeyboardButton("OTC Market FS", callback_data="otc_market_fs", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["chart_market"]),
            InlineKeyboardButton("Live Market FS", callback_data="live_market_fs", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["globe"]),
        ],
        [
            InlineKeyboardButton("Blackout FS", callback_data="blackout_fs", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["cross_premium"]),
            InlineKeyboardButton("Whiteout FS", callback_data="whiteout_fs", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["sparkle_premium"]),
        ],
        # === Payouts ===
        [
            InlineKeyboardButton("Top Payout", callback_data="top_payout", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["money"]),
            InlineKeyboardButton("News Signal", callback_data="news_signal", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["sparkle_premium"]),
        ],
        # === News & Filters ===
        [
            InlineKeyboardButton("Market Filters", callback_data="market_filters", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats_premium"]),
            InlineKeyboardButton("Time Session", callback_data="time_session", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["clock_premium"]),
        ],
        # === Schedule & Time ===
        [
            InlineKeyboardButton("TZ Converter", callback_data="tz_converter", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["alarm"]),
        ],
        [
            InlineKeyboardButton("Swap C/P", callback_data="swap_cp", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["swap"]),
            InlineKeyboardButton("Plans", url=WEBAPP_PLANS_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["diamond"]),
        ],
        # === Plans & Upgrade ===
        [
            InlineKeyboardButton("Upgrade", callback_data="upgrade", style=STYLE_BLUE, icon_custom_emoji_id="5217880283860194582"),
            InlineKeyboardButton("Free Bots", callback_data="free_bots", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["gift"]),
        ],
        # === Misc ===
        [
            InlineKeyboardButton("Referral Link", callback_data="referral_link", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["balloon_premium"]),
        ],
        # === Account ===
        [
            InlineKeyboardButton("Settings", callback_data="settings", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["gear"]),
            InlineKeyboardButton("Rate Us", callback_data="ratings", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["star"]),
        ],
        # === Support ===
        [
            InlineKeyboardButton("Support", url=SUPPORT_URL, style=STYLE_BLUE, icon_custom_emoji_id="5215334566549540768"),
            InlineKeyboardButton("Support Web", url=WEBAPP_SUPPORT_URL, style=STYLE_BLUE, icon_custom_emoji_id="5463090760041634232"),
        ],
        # === Admin ===
        [InlineKeyboardButton("Bot Control", url=WEBAPP_BOTS_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["tools"])],
        # === Final: 2 GREEN then 1 GREEN ===
        [
            InlineKeyboardButton("My Profile", callback_data="my_account", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["user"]),
            InlineKeyboardButton("Live Payouts", callback_data="live_payouts", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["diamond_premium"]),
        ],
        [InlineKeyboardButton("Start Signal Session", callback_data="signal_session_start", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["clock_premium"])],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])]])

def get_plans_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Free Plan - $0", callback_data="plan_free", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["free"])],
        [InlineKeyboardButton("Weekly Plan - $15", callback_data="plan_weekly", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["calendar"])],
        [InlineKeyboardButton("Monthly Plan - $45", callback_data="plan_monthly", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["calendar"])],
        [InlineKeyboardButton("Gold Plan - $120", callback_data="plan_gold", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["crown"])],
        [InlineKeyboardButton("Back", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])

def get_control_keyboard(is_admin):
    if not is_admin:
        return get_back_keyboard()
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("New Signal", callback_data="admin_new_signal", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("Broadcast", callback_data="admin_broadcast", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["speaker"]),
        ],
        [InlineKeyboardButton("Bot Statistics", callback_data="admin_stats", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])

def get_admin_confirm_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Yes, Send", callback_data="admin_confirm_send", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("Cancel", callback_data="control_bot", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"]),
        ]
    ])

def get_free_bots_list_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Signals Bot", url=FREE_BOTS_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
            InlineKeyboardButton("Price Alerts", url=FREE_BOTS_URL, style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["bell"]),
        ],
        [
            InlineKeyboardButton("Market News", url=FREE_BOTS_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["newspaper"]),
            InlineKeyboardButton("Profit Calc", url=FREE_BOTS_URL, style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["abacus"]),
        ],
        [
            InlineKeyboardButton("Crypto Scanner", url=FREE_BOTS_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["gem"]),
            InlineKeyboardButton("Economic Calendar", url=FREE_BOTS_URL, style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["calendar"]),
        ],
        [
            InlineKeyboardButton("Pattern Detector", url=FREE_BOTS_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["target"]),
            InlineKeyboardButton("Currency Converter", url=FREE_BOTS_URL, style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["currency"]),
        ],
        [InlineKeyboardButton("Back", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])

def get_back_to_signal_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Refresh", callback_data="request_signals", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["sparkles"]),
            InlineKeyboardButton("Back", callback_data="request_signals", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"]),
        ],
        [InlineKeyboardButton("Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])

def get_platform_keyboard(return_to):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data=f"platform_quotex_{return_to}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data=f"platform_binolla_{return_to}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])

def get_ratings_keyboard():
    """Rating keyboard with 1-5 stars and back button."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1 ⭐", callback_data="rate_1", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["star"]),
            InlineKeyboardButton("2 ⭐⭐", callback_data="rate_2", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["star"]),
            InlineKeyboardButton("3 ⭐⭐⭐", callback_data="rate_3", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["star"]),
        ],
        [
            InlineKeyboardButton("4 ⭐⭐⭐⭐", callback_data="rate_4", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["star"]),
            InlineKeyboardButton("5 ⭐⭐⭐⭐⭐", callback_data="rate_5", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["star"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])

def get_upgrade_keyboard():
    """Upgrade keyboard with plans 50, 75, 100 and back button."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Upgrade $50", callback_data="upgrade_50", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["calendar"])],
        [InlineKeyboardButton("Upgrade $75", callback_data="upgrade_75", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["diamond"])],
        [InlineKeyboardButton("Upgrade $100", callback_data="upgrade_100", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["crown"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])

# ============================================================
# 4) HANDLERS
# ============================================================
WAITING_SIGNAL_INPUT, WAITING_BROADCAST, WAITING_SESSION_START, WAITING_SESSION_END = range(4)

async def safe_edit_message(query, text, reply_markup=None, parse_mode=None):
    """Edit message safely - handle 'Message is not modified' error."""
    try:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except Exception as e:
        err_str = str(e)
        if "Message is not modified" in err_str or "exactly the same" in err_str:
            # Content is the same - this is OK, just skip
            pass
        else:
            logging.warning(f"edit_message_text error: {e}")
            try:
                await query.answer("Loading...", show_alert=False)
            except Exception:
                pass

def get_welcome_message(first_name=None):
    """Premium welcome message with fancy Unicode text and custom emojis."""
    name_part = f" {first_name}" if first_name else ""
    return f"""{lux('wave')} 𝑾𝑬𝑳𝑪𝑶𝑴𝑬{name_part} 𝑻𝑶 𝑸𝑼𝑨𝑵𝑻𝑽𝑬𝑿𝑨 𝑩𝑶𝑻

{e('🛠')} 𝒀𝑶𝑼𝑹 𝑺𝑴𝑨𝑹𝑻 𝑻𝑹𝑨𝑫𝑰𝑵𝑮 𝑨𝑺𝑺𝑰𝑺𝑻𝑨𝑵𝑻

{e('🚀')} 𝙔𝙤𝙪𝙧 𝙖𝙡𝙡-𝙞𝙣-𝙤𝙣𝙚 𝙏𝙧𝙖𝙙𝙞𝙣𝙜 𝙏𝙤𝙤𝙡𝙨 𝘽𝙤𝙩 — 𝙙𝙚𝙨𝙞𝙜𝙣𝙚𝙙 𝙩𝙤 𝙝𝙚𝙡𝙥 𝙮𝙤𝙪 𝙖𝙣𝙖𝙡𝙮𝙯𝙚 𝙢𝙖𝙧𝙠𝙚𝙩𝙨, 𝙖𝙘𝙘𝙚𝙨𝙨 𝙨𝙞𝙜𝙣𝙖𝙡𝙨, 𝙖𝙣𝙙 𝙪𝙨𝙚 𝙥𝙤𝙬𝙚𝙧𝙛𝙪𝙡 𝙩𝙧𝙖𝙙𝙞𝙣𝙜 𝙩𝙤𝙤𝙡𝙨.

{e('📈')} 𝑬𝙭𝙥𝙡𝙤𝙧𝙚 𝙨𝙞𝙜𝙣𝙖𝙡𝙨, 𝙢𝙖𝙧𝙠𝙚𝙩 𝙞𝙣𝙨𝙞𝙜𝙝𝙩𝙨, 𝙘𝙝𝙚𝙘𝙠𝙚𝙧𝙨, 𝙖𝙣𝙙 𝙤𝙩𝙝𝙚𝙧 𝙖𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚 𝙛𝙚𝙖𝙩𝙪𝙧𝙚𝙨 𝙛𝙧𝙤𝙢 𝙤𝙣𝙚 𝙥𝙡𝙖𝙘𝙚.

{e('⚡')} 𝑻𝑨𝑷 𝑩𝑬𝑳𝑶𝑾 𝑻𝑶 𝑮𝑬𝑻 𝑺𝑻𝑨𝑹𝑻𝑬𝑫

{e('💎')} 𝑬𝑿𝑷𝑳𝑶𝑹𝑬 𝑻𝑯𝑬 𝑭𝑬𝑨𝑻𝑼𝑹𝑬𝑺 & 𝑻𝑶𝑶𝑳𝑺 {e('✨')}"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    referrer_id = None
    if context.args and len(context.args) > 0:
        arg = context.args[0]
        if arg.startswith("ref_"):
            try:
                referrer_id = int(arg.replace("ref_", ""))
            except ValueError:
                referrer_id = None

    is_new = add_user(user_id=user_id, username=user.username, first_name=user.first_name, referrer_id=referrer_id)
    if is_new:
        logging.info(f"New user: {user_id} - @{user.username}")

    context.user_data["user_id"] = user_id
    welcome_text = get_welcome_message(user.first_name)
    if referrer_id:
        welcome_text += f"\n{emj('gift', '🎁')} You were referred by a friend!"

    await update.message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode=ParseMode.HTML)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # Handle timeout error gracefully (silent - don't log warnings)
    try:
        await query.answer()
    except Exception:
        pass  # Query too old or invalid - silently ignore
    
    data = query.data
    user_id = query.from_user.id
    context.user_data["user_id"] = user_id

    if data == "main_menu":
        await show_main_menu(query)
    elif data == "plans":
        await show_plans(query)
    elif data.startswith("plan_"):
        await show_plan_details(query, data.replace("plan_", ""))
    elif data == "request_signals":
        await show_request_signals(query)
    elif data.startswith("platform_quotex_request_signals"):
        await show_bot_signals(query, "quotex")
    elif data.startswith("platform_binolla_request_signals"):
        await show_bot_signals(query, "binolla")
    elif data == "current_signals":
        await show_current_signals(query)
    elif data == "time_list":
        await show_time_list(query)
    elif data == "time_session":
        await show_time_session(query)
    elif data == "signal_session_start":
        await show_signal_session_broker(query)
    elif data == "signal_session_quotex":
        await show_signal_session_quotex(query)
    elif data == "signal_session_binolla":
        await show_signal_session_binolla(query)
    elif data.startswith("signal_session_page_"):
        # Format: signal_session_page_<broker>_<page>
        parts = data.replace("signal_session_page_", "").split("_")
        if len(parts) == 2:
            await show_signal_session_pairs(query, parts[0], int(parts[1]))
    elif data.startswith("signal_session_toggle_"):
        # Format: signal_session_toggle_<broker>_<page>_<pair_index>
        parts = data.replace("signal_session_toggle_", "").split("_")
        if len(parts) == 3:
            broker = parts[0]
            page = int(parts[1])
            pair_idx = int(parts[2])
            await toggle_signal_session_pair(query, user_id, broker, page, pair_idx)
    elif data == "signal_session_select_all":
        await signal_session_select_all(query, user_id)
    elif data.startswith("signal_session_select_page_"):
        # Format: signal_session_select_page_<broker>_<page>
        parts = data.replace("signal_session_select_page_", "").split("_")
        if len(parts) == 2:
            await signal_session_select_page(query, user_id, parts[0], int(parts[1]))
    elif data == "signal_session_start_analysis":
        await show_signal_session_mtg(query, user_id)
    elif data == "signal_session_mtg1":
        await show_signal_session_duration(query, user_id, 1)
    elif data == "signal_session_mtg2":
        await show_signal_session_duration(query, user_id, 2)
    elif data.startswith("signal_session_duration_"):
        # Format: signal_session_duration_<duration>_<mtg_level>
        parts = data.replace("signal_session_duration_", "").split("_")
        if len(parts) == 2:
            duration = parts[0]
            mtg_level = int(parts[1])
            await start_signal_session_analysis(query, user_id, mtg_level, duration)
    elif data == "save_session":
        await save_session(query, context)
    elif data == "live_future":
        await show_live_future(query)
    elif data.startswith("set_schedule_"):
        # Format: set_schedule_HH:MM_HH:MM
        parts = data.replace("set_schedule_", "").split("_")
        if len(parts) == 2:
            await set_user_schedule(query, user_id, parts[0], parts[1])
    elif data == "pause_schedule":
        await pause_user_schedule(query, user_id)
    elif data == "delete_schedule":
        await delete_user_schedule(query, user_id)
    elif data == "free_bots":
        await show_free_bots(query)
    elif data.startswith("free_bot_"):
        bot_idx = int(data.replace("free_bot_", ""))
        await show_free_bot_details(query, user_id, bot_idx)
    elif data == "control_bot":
        await show_control_bot(query, user_id)
    elif data == "top_payout":
        await show_top_payout(query)
    elif data == "future_signals":
        await show_future_signals(query)
    elif data == "future_results":
        await show_future_results(query)
    elif data.startswith("platform_quotex_future_signals"):
        await show_future_signals_platform(query, "quotex")
    elif data.startswith("platform_binolla_future_signals"):
        await show_future_signals_platform(query, "binolla")
    elif data.startswith("platform_quotex_future_results"):
        await show_future_results_platform(query, "quotex")
    elif data.startswith("platform_binolla_future_results"):
        await show_future_results_platform(query, "binolla")
    elif data == "referral_link":
        await show_referral_link(query, user_id)
    elif data == "my_account":
        await show_my_account(query, user_id)
    elif data == "support":
        await show_support(query)
    elif data == "ratings":
        await show_ratings(query)
    elif data.startswith("rate_"):
        await submit_rating(query, data.replace("rate_", ""))
    elif data == "upgrade":
        await show_upgrade(query)
    elif data.startswith("upgrade_"):
        await show_upgrade_details(query, data.replace("upgrade_", ""))
    elif data == "schedule_session":
        await show_schedule_session(query)
    elif data == "settings":
        await show_settings(query)
    elif data == "settings_platform":
        await settings_change_platform(query, user_id)
    elif data == "settings_expiry":
        await settings_change_expiry(query, user_id)
    elif data == "settings_risk":
        await settings_change_risk(query, user_id)
    elif data == "settings_notifications":
        await settings_change_notifications(query, user_id)
    elif data.startswith("settings_set_"):
        # Format: settings_set_<key>_<value>
        parts = data.replace("settings_set_", "").split("_", 1)
        if len(parts) == 2:
            key = parts[0]
            value = parts[1]
            _save_user_setting(user_id, key.lower(), value)
            await show_settings(query)
    elif data == "live_checker":
        await show_checker(query, "Live Checker")
    elif data == "otc_checker":
        await show_checker(query, "OTC Checker")
    elif data == "blackout_checker":
        await show_checker(query, "Blackout Checker")
    elif data == "whiteout_checker":
        await show_checker(query, "Whiteout Checker")
    elif data == "otc_market_fs":
        await show_market_fs(query, "OTC Market")
    elif data == "live_market_fs":
        await show_market_fs(query, "Live Market")
    elif data == "blackout_fs":
        await show_market_fs(query, "Blackout")
    elif data == "whiteout_fs":
        await show_market_fs(query, "Whiteout")
    elif data == "future_live":
        await show_future_live(query)
    elif data == "live_signal":
        await show_live_signal(query)
    elif data == "live_signal_quotex":
        await show_live_signal_market(query, "quotex")
    elif data == "live_signal_binolla":
        await show_live_signal_market(query, "binolla")
    elif data.startswith("live_signal_broker_"):
        broker = data.replace("live_signal_broker_", "")
        await show_live_signal_market(query, broker)
    elif data.startswith("live_signal_market_"):
        parts = data.replace("live_signal_market_", "").split("_")
        if len(parts) == 2:
            market, broker = parts[0], parts[1]
            await show_live_signal_duration(query, broker, market)
    elif data.startswith("live_signal_dur_"):
        parts = data.replace("live_signal_dur_", "").split("_")
        if len(parts) == 3:
            duration, broker, market = parts[0], parts[1], parts[2]
            await show_live_signal_bot_type(query, broker, market, duration)
    elif data.startswith("live_signal_bot_"):
        parts = data.replace("live_signal_bot_", "").split("_")
        if len(parts) == 4:
            bot_type, broker, market, duration = parts[0], parts[1], parts[2], parts[3]
            await show_live_signal_final(query, broker, market, duration, bot_type)
    elif data == "bug_signal":
        await show_bug_signal(query)
    elif data == "live_payouts":
        await show_live_payouts(query)
    elif data == "live_payouts_quotex":
        await show_live_payouts_pairs(query, "quotex")
    elif data == "live_payouts_binolla":
        await show_live_payouts_pairs(query, "binolla")
    elif data == "live_payouts_refresh":
        await query.answer("Refreshed!", show_alert=False)
    elif data == "news_signal":
        await show_news_signal(query)
    elif data == "ai_filter":
        await show_ai_filter(query)
    elif data == "ai_assistant":
        await show_ai_assistant(query)
    elif data == "formatter":
        await show_formatter(query)
    elif data == "market_filters":
        await show_market_filters(query)
    elif data == "swap_cp":
        await show_swap_cp(query)
    elif data == "tz_converter":
        await show_tz_converter(query)
    elif data.startswith("set_tz_"):
        utc_offset = data.replace("set_tz_", "")
        await set_user_timezone(query, user_id, utc_offset)
    elif data == "admin_new_signal":
        await admin_new_signal(query, context)
    elif data == "admin_broadcast":
        await admin_broadcast(query, context)
    elif data == "admin_stats":
        await admin_stats(query)
    elif data == "admin_confirm_send":
        await admin_confirm_send(query, context)

async def show_main_menu(query):
    first_name = query.from_user.first_name if query.from_user else None
    await safe_edit_message(query, get_welcome_message(first_name), reply_markup=get_main_menu_keyboard(), parse_mode=ParseMode.HTML)

async def show_plans(query):
    text = f"""
{emj('diamond', '💎')} Subscription Plans {emj('diamond', '💎')}

Choose the plan that suits you from the list below:

{emj('free', '🆓')} Free Plan - $0
Duration: 7 days trial
Limited basic features

{emj('calendar', '📅')} Weekly Plan - $15
Duration: 7 full days
Unlimited signals + instant alerts

{emj('calendar', '📆')} Monthly Plan - $45
Duration: 30 days
All features + advanced analytics

{emj('crown', '👑')} Gold Plan - $120
Duration: 90 days
VIP features + personal account manager

Select a plan to view full details:
"""
    await safe_edit_message(query, text, reply_markup=get_plans_keyboard(), parse_mode=ParseMode.HTML)

async def show_plan_details(query, plan_key):
    plans_map = {"free": PLANS[0], "weekly": PLANS[1], "monthly": PLANS[2], "gold": PLANS[3]}
    plan = plans_map.get(plan_key, PLANS[0])
    features_text = "\n".join([f"{emj('check', '✅')} {f}" for f in plan["features"]])
    text = f"""
📋 Plan Details

Name: {plan['name']}
Price: {plan['price']}
Duration: {plan['duration']}

{emj('star', '⭐')} Included Features:
{features_text}

💳 To subscribe to this plan:
Contact technical support via the Support button in the main menu
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_request_signals(query):
    text = f"""
{emj('lightning', '⚡')} Request Signals Now

{emj('robot', '🤖')} Select the platform you want signals from:

🟢 QUOTEX
  Best for binary options (OTC available)

🔵 BINOLLA
  Fast execution + high payout rates

👇 Choose a platform below:
"""
    await safe_edit_message(query, text, reply_markup=get_platform_keyboard("request_signals"), parse_mode=ParseMode.HTML)

async def show_bot_signals(query, platform):
    now = datetime.now()
    platforms_info = {
        "quotex": {"name": "QUOTEX Signals", "emoji_id": EMOJI_IDS["robot"], "pairs": [("EUR/USD OTC", "CALL", "1.0856", "M1", "94%"), ("GBP/JPY OTC", "PUT", "189.42", "M5", "89%"), ("USD/JPY OTC", "CALL", "149.78", "M1", "91%")]},
        "binolla": {"name": "BINOLLA Signals", "emoji_id": EMOJI_IDS["chart"], "pairs": [("AUD/CAD", "PUT", "0.9124", "M5", "88%"), ("EUR/GBP", "CALL", "0.8541", "M1", "92%"), ("USD/CHF", "PUT", "0.8923", "M5", "90%")]},
    }
    platform_info = platforms_info.get(platform, platforms_info["quotex"])
    signals_text = "\n\n".join([f"📊 {p[0]}\nDirection: {p[1]}\nEntry: {p[2]}\nExpiry: {p[3]}\nConfidence: {p[4]}" for p in platform_info["pairs"]])
    text = f"""
{emj('robot', '🤖')} {platform_info['name']}

{emj('calendar', '📅')} Request Time: {now.strftime('%Y-%m-%d %H:%M:%S')}
{emj('check', '✅')} Status: Active signals below

{signals_text}

📈 Platform Summary:
• Active pairs: {len(platform_info['pairs'])}
• Avg confidence: 90%
• Sentiment: Bullish {emj('chart', '📈')}

{emj('warning', '⚠️')} Trade responsibly - Not financial advice
"""
    await safe_edit_message(query, text, reply_markup=get_back_to_signal_keyboard(), parse_mode=ParseMode.HTML)

async def show_current_signals(query):
    signals = [("EUR/USD", "CALL", "1.0856", "M1", "92%"), ("GBP/JPY", "PUT", "189.42", "M5", "88%"), ("USD/JPY", "CALL", "149.78", "M1", "95%")]
    signals_text = "\n\n".join([f"📊 {s[0]}\nDirection: {s[1]}\nEntry: {s[2]}\nExpiry: {s[3]}\nExpected Rate: {s[4]}" for s in signals])
    text = f"""
{emj('chart', '📈')} Live Current Signals

{signals_text}

{emj('clock', '⏰')} Last Update: {datetime.now().strftime('%H:%M:%S')}
{emj('warning', '⚠️')} Trade responsibly - Signals are not a profit guarantee

📌 To subscribe to premium instant signals, use the "Subscription Plans" button
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_time_list(query):
    """Personal signal scheduling - user sets when bot sends signals."""
    user_id = query.from_user.id
    user_data = get_user(user_id)
    # Get user's scheduled time (stored in DB or default None)
    scheduled_time = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_schedule (user_id INTEGER PRIMARY KEY, start_time TEXT, end_time TEXT, enabled INTEGER DEFAULT 0)")
        cursor.execute("SELECT start_time, end_time, enabled FROM user_schedule WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            scheduled_time = dict(row)
        conn.close()
    except Exception:
        pass

    if scheduled_time and scheduled_time.get("start_time"):
        status = "✅ Active" if scheduled_time.get("enabled") else "⏸️ Paused"
        schedule_text = f"""{emj('check', '✅')} 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆 𝑺𝒕𝒂𝒕𝒖𝒔: {status}

{emj('clock', '⏰')} 𝑺𝒕𝒂𝒓𝒕 𝑻𝒊𝒎𝒆: {scheduled_time['start_time']}
{emj('clock', '⏰')} 𝑬𝒏𝒅 𝑻𝒊𝒎𝒆: {scheduled_time.get('end_time', 'Not set')}

💡 The bot will automatically send you signals during this time period."""
    else:
        schedule_text = f"""{emj('warning', '⚠️')} 𝑵𝒐 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆 𝑺𝒆𝒕

You haven't set a signal schedule yet.

👇 Choose a time slot below to start receiving signals automatically:"""

    text = f"""{emj('clock', '⏰')} 𝑺𝑰𝑮𝑵𝑨𝑳 𝑺𝑪𝑯𝑬𝑫𝑼𝑳𝑬

{schedule_text}

━━━━━━━━━━━━━━━━━━━━

💡 𝑯𝒐𝒘 𝒊𝒕 𝒘𝒐𝒓𝒌𝒔:
Set a time period and the bot will
automatically send you trading signals
during that time every day."""

    # Build keyboard rows as a list
    keyboard_rows = [
        [
            InlineKeyboardButton("🌅 Morning 09:00-12:00", callback_data="set_schedule_09:00_12:00", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["clock_premium"]),
            InlineKeyboardButton("☀️ Afternoon 14:00-17:00", callback_data="set_schedule_14:00_17:00", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["clock_premium"]),
        ],
        [
            InlineKeyboardButton("🌆 Evening 19:00-22:00", callback_data="set_schedule_19:00_22:00", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["clock_premium"]),
            InlineKeyboardButton("🌙 Night 22:00-01:00", callback_data="set_schedule_22:00_01:00", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["clock_premium"]),
        ],
        [
            InlineKeyboardButton("🕐 Full Day 00:00-23:59", callback_data="set_schedule_00:00_23:59", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["clock_premium"]),
        ],
    ]
    if scheduled_time and scheduled_time.get("start_time"):
        keyboard_rows.append([
            InlineKeyboardButton("⏸️ Pause Schedule", callback_data="pause_schedule", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"]),
            InlineKeyboardButton("🗑️ Delete Schedule", callback_data="delete_schedule", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"]),
        ])
    keyboard_rows.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# ============================================================
# SIGNAL SESSION - Broker selection, pairs selection, MTG
# ============================================================

# Currency pairs list with payout percentages (simulated data)
# 40 pairs sorted by payout (highest first)
SIGNAL_SESSION_PAIRS = [
    ("EUR/USD OTC", 95), ("GBP/JPY OTC", 93), ("USD/JPY OTC", 92),
    ("AUD/CAD OTC", 91), ("EUR/GBP OTC", 90), ("USD/CHF OTC", 89),
    ("EUR/JPY OTC", 88), ("GBP/USD OTC", 87), ("USD/CAD OTC", 86),
    ("AUD/USD OTC", 85), ("NZD/USD OTC", 84), ("EUR/AUD OTC", 83),
    ("GBP/AUD OTC", 82), ("EUR/CAD OTC", 81), ("AUD/JPY OTC", 80),
    ("CAD/JPY OTC", 79), ("NZD/JPY OTC", 78), ("CHF/JPY OTC", 77),
    ("EUR/CHF OTC", 76), ("USD/SEK OTC", 75), ("EUR/SEK OTC", 74),
    ("GBP/CHF OTC", 73), ("AUD/NZD OTC", 72), ("CAD/CHF OTC", 71),
    ("EUR/NZD OTC", 70), ("GBP/CAD OTC", 69), ("NZD/CAD OTC", 68),
    ("AUD/CHF OTC", 67), ("EUR/NOK OTC", 66), ("USD/NOK OTC", 65),
    ("GBP/NOK OTC", 64), ("AUD/SEK OTC", 63), ("CAD/SEK OTC", 62),
    ("EUR/TRY OTC", 61), ("USD/TRY OTC", 60), ("GBP/TRY OTC", 59),
    ("USD/ZAR OTC", 58), ("EUR/ZAR OTC", 57), ("USD/MXN OTC", 56),
    ("USD/SGD OTC", 55),
]
PAIRS_PER_PAGE = 30  # 2 columns x 15 rows = 30 per page


def _get_pair_color_style(payout: int):
    """Return button style based on payout: blue (85%+), green (70-84%), red (<70%)."""
    if payout >= 85:
        return STYLE_BLUE  # High payout 85%+ - blue
    elif payout >= 70:
        return STYLE_GREEN  # Medium payout 70-84% - green
    else:
        return STYLE_RED  # Low payout <70% - red


async def show_signal_session_quotex(query):
    """Clear old selections and show QUOTEX pairs."""
    user_id = query.from_user.id
    _clear_user_selections(user_id, "quotex")
    await show_signal_session_pairs(query, "quotex", 0)

async def show_signal_session_binolla(query):
    """Clear old selections and show BINOLLA pairs."""
    user_id = query.from_user.id
    _clear_user_selections(user_id, "binolla")
    await show_signal_session_pairs(query, "binolla", 0)


def _clear_user_selections(user_id: int, broker: str):
    """Clear all selections for a user/broker."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS signal_session_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("DELETE FROM signal_session_selections WHERE user_id = ? AND broker = ?", (user_id, broker))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to clear selections: {e}")


async def show_signal_session_broker(query):
    """Show broker selection page."""
    text = f"""{emj('clock', '⏰')} 𝚂𝙸𝙶𝙽𝙰𝙻 𝚂𝙴𝚂𝚂𝙸𝙾𝙽

👇 𝙲𝙷𝙾𝙾𝚂𝙴 𝙱𝚁𝙾𝙺𝙴𝚁

Select your broker to start the signal session."""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="signal_session_quotex", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="signal_session_binolla", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_signal_session_pairs(query, broker: str, page: int):
    """Show currency pairs page with 2 columns + navigation + selection buttons."""
    # Get selected pairs from DB
    user_id = query.from_user.id
    selected_pairs = _get_selected_pairs(user_id, broker)

    total_pairs = len(SIGNAL_SESSION_PAIRS)
    total_pages = (total_pairs + PAIRS_PER_PAGE - 1) // PAIRS_PER_PAGE
    start_idx = page * PAIRS_PER_PAGE
    end_idx = min(start_idx + PAIRS_PER_PAGE, total_pairs)
    page_pairs = SIGNAL_SESSION_PAIRS[start_idx:end_idx]

    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    text = f"""{emj('clock', '⏰')} 𝚂𝙸𝙶𝙽𝙰𝙻 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 - {broker_name}

👇 𝚂𝙴𝙻𝙴𝙲𝚃 𝙲𝚄𝚁𝚁𝙴𝙽𝙲𝚈 𝙿𝙰𝙸𝚁𝚂

Page {page + 1}/{total_pages} · Selected: {len(selected_pairs)} pairs

🟦 Blue = High payout (85%+)
🟩 Green = Medium payout (70-84%)
🟥 Red = Low payout (&lt;70%)"""
    keyboard_rows = []
    # 2 buttons per row
    row = []
    for i, (pair_name, payout) in enumerate(page_pairs):
        global_idx = start_idx + i
        is_selected = str(global_idx) in selected_pairs
        # Only ONE checkmark in text, no icon emoji when selected
        if is_selected:
            label = f"✅{pair_name} {payout}%"
            style = STYLE_GREEN
            icon_id = None  # No icon - only text checkmark
        else:
            label = f"{pair_name} {payout}%"
            style = _get_pair_color_style(payout)
            icon_id = None  # No icon for unselected either
        row.append(InlineKeyboardButton(label, callback_data=f"signal_session_toggle_{broker}_{page}_{global_idx}", style=style))
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    if row:  # Last odd button
        keyboard_rows.append(row)

    # Navigation buttons
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"signal_session_page_{broker}_{page-1}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"]))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("➡️ Next", callback_data=f"signal_session_page_{broker}_{page+1}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"]))
    if nav_row:
        keyboard_rows.append(nav_row)

    # Selection button - only selectAll
    keyboard_rows.append([
        InlineKeyboardButton("selectAll", callback_data="signal_session_select_all", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["check"]),
    ])

    # Start analysis button (shows count)
    count = len(selected_pairs)
    keyboard_rows.append([
        InlineKeyboardButton(f"Start ({count})", callback_data="signal_session_start_analysis", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["lightning"]),
    ])

    # Back button
    keyboard_rows.append([InlineKeyboardButton("Back to Broker", callback_data="signal_session_start", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


def _get_selected_pairs(user_id: int, broker: str) -> set:
    """Get user's selected pairs for a broker from DB."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS signal_session_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("SELECT pair_index FROM signal_session_selections WHERE user_id = ? AND broker = ?", (user_id, broker))
        rows = cursor.fetchall()
        conn.close()
        return set(str(r[0]) for r in rows)
    except Exception:
        return set()


async def toggle_signal_session_pair(query, user_id, broker, page, pair_idx):
    """Toggle selection of a currency pair."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS signal_session_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        # Check if already selected
        cursor.execute("SELECT 1 FROM signal_session_selections WHERE user_id = ? AND broker = ? AND pair_index = ?", (user_id, broker, pair_idx))
        if cursor.fetchone():
            cursor.execute("DELETE FROM signal_session_selections WHERE user_id = ? AND broker = ? AND pair_index = ?", (user_id, broker, pair_idx))
        else:
            cursor.execute("INSERT INTO signal_session_selections (user_id, broker, pair_index) VALUES (?, ?, ?)", (user_id, broker, pair_idx))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to toggle pair: {e}")
    # Refresh the page
    await show_signal_session_pairs(query, broker, page)


async def signal_session_select_page(query, user_id, broker, page):
    """Select all pairs on current page then go directly to MTG selection."""
    start_idx = page * PAIRS_PER_PAGE
    end_idx = min(start_idx + PAIRS_PER_PAGE, len(SIGNAL_SESSION_PAIRS))
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS signal_session_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        for i in range(start_idx, end_idx):
            cursor.execute("INSERT OR IGNORE INTO signal_session_selections (user_id, broker, pair_index) VALUES (?, ?, ?)", (user_id, broker, i))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to select page: {e}")
    # Go directly to MTG selection (not back to pairs page)
    await show_signal_session_mtg(query, user_id)


async def signal_session_select_all(query, user_id):
    """Select all pairs for the current broker then go directly to MTG selection."""
    # Detect broker from the current message (we stored it in text)
    # For simplicity, try to detect from the message text
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS signal_session_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        for i in range(len(SIGNAL_SESSION_PAIRS)):
            cursor.execute("INSERT OR IGNORE INTO signal_session_selections (user_id, broker, pair_index) VALUES (?, ?, ?)", (user_id, broker, i))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to select all: {e}")
    # Go directly to MTG selection (not back to pairs page)
    await show_signal_session_mtg(query, user_id)


async def show_signal_session_mtg(query, user_id):
    """Show MTG selection page after user clicks Start."""
    # Detect broker from message text
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"
    selected_count = len(_get_selected_pairs(user_id, broker))

    if selected_count == 0:
        await query.answer("Please select at least one pair first!", show_alert=True)
        return

    text = f"""{emj('lightning', '⚡')} 𝚂𝚃𝙰𝚁𝚃 𝙰𝙽𝙰𝙻𝚈𝚂𝙸𝚂

Selected pairs: {selected_count}

👇 𝙲𝙷𝙾𝙾𝚂𝙴 𝙼𝚃𝙶 𝙻𝙴𝚅𝙴𝙻"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MTG1", callback_data="signal_session_mtg1", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("MTG2", callback_data="signal_session_mtg2", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_signal_session_duration(query, user_id, mtg_level):
    """Show trade duration selection page (1M, 2M, 3M, 4M, 5M)."""
    # Detect broker
    # We need to store mtg_level in user_data or pass it
    text = f"""{emj('clock', '⏰')} 𝚃𝚁𝙰𝙳𝙴 𝙳𝚄𝚁𝙰𝚃𝙸𝙾𝙽

MTG Level: MTG{mtg_level}

👇 𝙲𝙷𝙾𝙾𝚂𝙴 𝙳𝚄𝚁𝙰𝚃𝙸𝙾𝙽"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1M", callback_data=f"signal_session_duration_1M_{mtg_level}", style=STYLE_BLUE),
            InlineKeyboardButton("2M", callback_data=f"signal_session_duration_2M_{mtg_level}", style=STYLE_BLUE),
            InlineKeyboardButton("3M", callback_data=f"signal_session_duration_3M_{mtg_level}", style=STYLE_BLUE),
        ],
        [
            InlineKeyboardButton("4M", callback_data=f"signal_session_duration_4M_{mtg_level}", style=STYLE_BLUE),
            InlineKeyboardButton("5M", callback_data=f"signal_session_duration_5M_{mtg_level}", style=STYLE_BLUE),
        ],
        [InlineKeyboardButton("Back to MTG", callback_data="signal_session_start_analysis", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def start_signal_session_analysis(query, user_id, mtg_level, duration="1M"):
    """Start the signal session analysis with selected pairs, MTG level, and duration."""
    # Detect broker from message
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"

    # Get selected pairs for this broker only
    pair_indices = _get_selected_pairs(user_id, broker)
    selected_pairs = []
    for idx_str in pair_indices:
        idx = int(idx_str)
        if 0 <= idx < len(SIGNAL_SESSION_PAIRS):
            selected_pairs.append((broker, SIGNAL_SESSION_PAIRS[idx][0], SIGNAL_SESSION_PAIRS[idx][1]))

    if not selected_pairs:
        await query.answer("No pairs selected!", show_alert=True)
        return

    # Save session to DB
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS active_signal_sessions (user_id INTEGER PRIMARY KEY, broker TEXT, pairs TEXT, mtg_level INTEGER, duration TEXT, started_at TEXT, active INTEGER DEFAULT 1)")
        import json as _json
        pairs_json = _json.dumps(selected_pairs)
        cursor.execute("INSERT OR REPLACE INTO active_signal_sessions (user_id, broker, pairs, mtg_level, duration, started_at, active) VALUES (?, ?, ?, ?, ?, ?, 1)",
                       (user_id, broker, pairs_json, mtg_level, duration, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to save session: {e}")

    pairs_count = len(selected_pairs)
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    text = f"""{emj('check', '✅')} 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝚂𝚃𝙰𝚁𝚃𝙴𝙳!

{emj('lightning', '⚡')} MTG Level: MTG{mtg_level}
{emj('clock', '⏰')} Duration: {duration}
{emj('stats', '📊')} Broker: {broker_name}
{emj('chart', '📈')} Selected Pairs: {pairs_count}

💡 The bot will now start sending
trading signals for your selected pairs.

{emj('clock', '⏰')} Session started at: {datetime.now().strftime('%H:%M:%S')}"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_time_session(query):
    """Show the Time Session page - user can add a session with start/end time."""
    user_id = query.from_user.id
    # Get user's saved sessions
    sessions = []
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS time_sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, start_time TEXT, end_time TEXT, enabled INTEGER DEFAULT 1)")
        cursor.execute("SELECT id, start_time, end_time, enabled FROM time_sessions WHERE user_id = ? ORDER BY id", (user_id,))
        rows = cursor.fetchall()
        sessions = [dict(r) for r in rows]
        conn.close()
    except Exception:
        pass

    if sessions:
        sessions_text = ""
        for i, s in enumerate(sessions, 1):
            status = "✅" if s["enabled"] else "⏸️"
            sessions_text += f"\n{i}. {status} {s['start_time']} - {s['end_time']}"
        schedule_text = f"""{emj('check', '✅')} 𝒀𝒐𝒖𝒓 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆𝒅 𝑺𝒆𝒔𝒔𝒊𝒐𝒏𝒔:
{sessions_text}"""
    else:
        schedule_text = f"""{emj('warning', '⚠️')} 𝙽𝙾 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴𝙳 𝚂𝙴𝚂𝚂𝙸𝙾𝙽𝚂 𝚈𝙴𝚃

𝚈𝚘𝚞 𝚍𝚘𝚗'𝚝 𝚑𝚊𝚟𝚎 𝚊𝚗𝚢 𝚜𝚌𝚑𝚎𝚍𝚞𝚕𝚎𝚍 𝚜𝚎𝚜𝚜𝚒𝚘𝚗𝚜 𝚊𝚝 𝚝𝚑𝚎 𝚖𝚘𝚖𝚎𝚗𝚝.

➕ 𝙽𝙴𝚆 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴

👇 𝚃𝙰𝙿 𝙱𝙴𝙻𝙾𝚆 𝚃𝙾 𝙲𝚁𝙴𝙰𝚃𝙴 𝙰 𝙽𝙴𝚆 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴."""

    text = f"""{emj('clock', '⏰')} 𝚃𝙸𝙼𝙴 𝚂𝙴𝚂𝚂𝙸𝙾𝙽

{schedule_text}

━━━━━━━━━━━━━━━━━━━━

💡 𝑯𝒐𝒘 𝒊𝒕 𝒘𝒐𝒓𝒌𝒔:
Set a time period and the bot will
automatically send you trading signals
during that time every day."""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ New Schedule", callback_data="new_session", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["clock_premium"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def start_new_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the new session conversation - ask for start time."""
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    text = f"""{emj('clock', '⏰')} 𝙽𝙴𝚆 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴

👇 𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙴𝙽𝙳 𝚃𝙷𝙴 𝚂𝚃𝙰𝚁𝚃 𝚃𝙸𝙼𝙴

𝙵𝚘𝚛𝚖𝚊𝚝: 𝙷𝙷:𝙼𝙼 (𝚎.𝚐. 09:00)

{emj('warning', '⚠️')} 𝚂𝚎𝚗𝚍 /cancel 𝚝𝚘 𝚌𝚊𝚗𝚌𝚎𝚕"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="time_session", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return WAITING_SESSION_START


async def receive_session_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive the start time and ask for end time."""
    text = update.message.text.strip()
    # Validate HH:MM format
    try:
        parts = text.split(":")
        if len(parts) != 2:
            raise ValueError
        h, m = int(parts[0]), int(parts[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
    except (ValueError, IndexError):
        await update.message.reply_text(f"{emj('warning', '⚠️')} Invalid format! Please send time as HH:MM (e.g. 09:00)\n\nSend /cancel to cancel")
        return WAITING_SESSION_START

    context.user_data["session_start"] = text
    await update.message.reply_text(
        f"{emj('check', '✅')} Start time received: {text}\n\n"
        f"{emj('clock', '⏰')} Now please send the END time\n\n"
        f"Format: HH:MM (e.g. 17:00)\n\n"
        f"{emj('warning', '⚠️')} Send /cancel to cancel",
        parse_mode=ParseMode.HTML
    )
    return WAITING_SESSION_END


async def receive_session_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive the end time and show confirmation with Save/Back buttons."""
    text = update.message.text.strip()
    try:
        parts = text.split(":")
        if len(parts) != 2:
            raise ValueError
        h, m = int(parts[0]), int(parts[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
    except (ValueError, IndexError):
        await update.message.reply_text(f"{emj('warning', '⚠️')} Invalid format! Please send time as HH:MM (e.g. 17:00)\n\nSend /cancel to cancel")
        return WAITING_SESSION_END

    context.user_data["session_end"] = text
    start_time = context.user_data.get("session_start")
    end_time = text

    text_msg = f"""{emj('check', '✅')} 𝙲𝙾𝙽𝙵𝙸𝚁𝙼 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴

{emj('clock', '⏰')} 𝚂𝚃𝙰𝚁𝚃: {start_time}
{emj('clock', '⏰')} 𝙴𝙽𝙳:   {end_time}

👇 𝙿𝚁𝙴𝚂𝚂 𝙱𝙴𝙻𝙾𝚆 𝚃𝙾 𝙲𝙾𝙽𝙵𝙸𝚁𝙼"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💾 Save Schedule", callback_data="save_session", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"])],
        [InlineKeyboardButton("Back to Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await update.message.reply_text(text_msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return ConversationHandler.END


async def save_session(query, context):
    """Save the session to database and return to main menu."""
    user_id = query.from_user.id
    start_time = context.user_data.get("session_start")
    end_time = context.user_data.get("session_end")

    if not start_time or not end_time:
        await safe_edit_message(query, f"{emj('warning', '⚠️')} Session data missing. Please try again.", reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS time_sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, start_time TEXT, end_time TEXT, enabled INTEGER DEFAULT 1)")
        cursor.execute("INSERT INTO time_sessions (user_id, start_time, end_time, enabled) VALUES (?, ?, ?, 1)", (user_id, start_time, end_time))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to save session: {e}")

    # Clear user data
    context.user_data.pop("session_start", None)
    context.user_data.pop("session_end", None)

    text = f"""{emj('check', '✅')} 𝚂𝙲𝚑𝚎𝚍𝚞𝚕𝚎 𝚂𝚊𝚟𝚎𝚍!

{emj('clock', '⏰')} Start: {start_time}
{emj('clock', '⏰')} End: {end_time}

💡 The bot will send you trading signals
during this time period every day."""
    await safe_edit_message(query, text, reply_markup=get_main_menu_keyboard(), parse_mode=ParseMode.HTML)


async def show_live_future(query):
    """Show the Live Future page - user requests to verify results."""
    text = f"""{emj('crystal_ball', '🔮')} 𝙻𝙸𝚅𝙴 𝙵𝚄𝚃𝚄𝚁𝙴

𝚁𝚎𝚚𝚞𝚎𝚜𝚝 𝚝𝚘 𝚟𝚎𝚛𝚒𝚏𝚢 𝚏𝚞𝚝𝚞𝚛𝚎 𝚜𝚒𝚐𝚗𝚊𝚕𝚜 𝚛𝚎𝚜𝚞𝚕𝚝𝚜.

👇 𝚃𝙰𝙿 𝙱𝙴𝙻𝙾𝚆 𝚃𝙾 𝙲𝙷𝙴𝙲𝙺:"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Check Results", callback_data="future_results", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_free_bots(query):
    """Show 10 free bots - ALL locked, 2 columns x 5 rows, blue color."""
    bots = [
        "Signals Bot",
        "Price Alerts Bot",
        "Market News Bot",
        "Profit Calc Bot",
        "Pattern Detector Bot",
        "Crypto Scanner Bot",
        "Economic Calendar Bot",
        "Currency Converter Bot",
        "Risk Manager Bot",
        "Trade Journal Bot",
    ]

    text = f"""{emj('gift', '🎁')} <b>FREE BOTS</b>"""
    keyboard_rows = []
    # 2 columns x 5 rows: first 5 in left column, next 5 in right column
    for i in range(5):
        left_bot = bots[i]
        right_bot = bots[i + 5]
        row = [
            InlineKeyboardButton(left_bot, callback_data=f"free_bot_{i}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["lock"]),
            InlineKeyboardButton(right_bot, callback_data=f"free_bot_{i+5}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["lock"]),
        ]
        keyboard_rows.append(row)

    keyboard_rows.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])])
    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_free_bot_details(query, user_id, bot_idx):
    """Show details for a specific free bot - all locked, need upgrade."""
    bots = [
        ("Signals Bot", "Basic analysis for major currencies. Get simple trading signals."),
        ("Price Alerts Bot", "Alerts when price reaches a specific level you set."),
        ("Market News Bot", "Latest economic news as soon as published."),
        ("Profit Calc Bot", "Easily calculate your trading profits and losses."),
        ("Pattern Detector Bot", "Detect chart patterns automatically."),
        ("Crypto Scanner Bot", "Scan crypto pairs for trading opportunities."),
        ("Economic Calendar Bot", "Track upcoming economic events and news."),
        ("Currency Converter Bot", "Convert between 150+ currencies instantly."),
        ("Risk Manager Bot", "Manage your risk with position sizing tools."),
        ("Trade Journal Bot", "Keep a journal of all your trades and results."),
    ]

    if bot_idx < 0 or bot_idx >= len(bots):
        await query.answer("Bot not found!", show_alert=True)
        return

    bot_name, bot_desc = bots[bot_idx]

    # ALL bots are locked - show upgrade message
    text = f"""{emj('lock', '🔒')} <b>{bot_name}</b>

{emj('warning', '⚠️')} <b>UPGRADE REQUIRED</b>

This bot is locked. You need to upgrade your plan
to access this bot.

Upgrade to: Weekly / Monthly / Gold
to unlock all bots.

👇 <b>TAP BELOW TO UPGRADE</b>"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Upgrade Now", callback_data="upgrade", style=STYLE_GREEN, icon_custom_emoji_id="5217880283860194582")],
        [InlineKeyboardButton("Back to Bots", callback_data="free_bots", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_control_bot(query, user_id):
    if not is_admin(user_id):
        text = f"""
{emj('cross', '❌')} Access Denied

This feature is restricted to admins only.
If you believe this is an error, please contact support.
"""
        await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
        return
    text = f"""
{emj('tools', '🛠')} Admin Control Panel

Welcome Admin {emj('crown', '👑')}

Quick Statistics:
👥 Users: {get_all_users_count()}
{emj('stats', '📊')} Today's Signals: {len(get_signals_stats())}

Select the desired action:
"""
    await safe_edit_message(query, text, reply_markup=get_control_keyboard(is_admin=True), parse_mode=ParseMode.HTML)

# ============================================
# Fancy Unicode text helpers (Bold / Bold Italic)
# ============================================
def to_bold_italic(text: str) -> str:
    """Convert text to Mathematical Bold Italic Unicode characters."""
    result = []
    for c in text:
        if 'A' <= c <= 'Z':
            result.append(chr(0x1D468 + (ord(c) - ord('A'))))
        elif 'a' <= c <= 'z':
            result.append(chr(0x1D482 + (ord(c) - ord('a'))))
        else:
            result.append(c)
    return ''.join(result)


def to_bold(text: str) -> str:
    """Convert text to Mathematical Bold Unicode characters."""
    result = []
    for c in text:
        if 'A' <= c <= 'Z':
            result.append(chr(0x1D400 + (ord(c) - ord('A'))))
        elif 'a' <= c <= 'z':
            result.append(chr(0x1D41A + (ord(c) - ord('a'))))
        elif '0' <= c <= '9':
            result.append(chr(0x1D7CE + (ord(c) - ord('0'))))
        else:
            result.append(c)
    return ''.join(result)


async def show_top_payout(query):
    """Show top payout pairs (88%+) with bold text."""
    # Filter pairs with payout 88%+
    top_pairs = [(name, payout) for name, payout in SIGNAL_SESSION_PAIRS if payout >= 88]
    
    # Build text with bold Unicode for pair names and payouts
    lines = []
    for i, (pair_name, payout) in enumerate(top_pairs, 1):
        bold_name = to_bold(pair_name)
        bold_payout = to_bold(f"{payout}%")
        lines.append(f"{bold_name}  {bold_payout}")
    pairs_text = "\n".join(lines)

    text = f"""{emj('money', '💲')} <b>TOP PAYOUT</b>

Pairs with 88%+ payout:

{pairs_text}

{emj('stats', '📊')} <b>Updated:</b> {datetime.now().strftime('%H:%M')}
{emj('warning', '⚠️')} <b>Rates change continuously</b>"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_future_signals(query):
    text = f"""
{emj('crystal', '💎')} Choose Platform

Select the platform you want future signals for:
"""
    await safe_edit_message(query, text, reply_markup=get_platform_keyboard("future_signals"), parse_mode=ParseMode.HTML)

async def show_future_signals_platform(query, platform):
    now = datetime.now()
    if platform == "quotex":
        future_signals = [("EUR/USD OTC", now + timedelta(minutes=15), "CALL", "M1"), ("GBP/JPY OTC", now + timedelta(minutes=30), "PUT", "M5"), ("USD/JPY OTC", now + timedelta(hours=1), "CALL", "M1")]
    else:
        future_signals = [("BTC/USD", now + timedelta(minutes=15), "PUT", "M5"), ("ETH/USD", now + timedelta(minutes=30), "CALL", "M1"), ("Gold/XAU", now + timedelta(hours=1), "CALL", "M5")]
    signals_text = "\n\n".join([f"📊 {s[0]}\n{emj('clock', '⏰')} {s[1].strftime('%H:%M')}\nDirection: {s[2]}\nDuration: {s[3]}" for s in future_signals])
    platform_name = "QUOTEX" if platform == "quotex" else "BINOLLA"
    text = f"""
{emj('crystal', '💎')} {platform_name} - Upcoming Future Signals

{signals_text}

{emj('warning', '⚠️')} Future signals are a premium feature (Monthly Plan or higher)
"""
    await safe_edit_message(query, text, reply_markup=get_platform_keyboard("future_signals"), parse_mode=ParseMode.HTML)

async def show_future_results(query):
    text = f"""
📋 Choose Platform

Select the platform to view results for:
"""
    await safe_edit_message(query, text, reply_markup=get_platform_keyboard("future_results"), parse_mode=ParseMode.HTML)

async def show_future_results_platform(query, platform):
    if platform == "quotex":
        results = [("EUR/USD OTC", "CALL", "WIN", "✅", "1.0856 → 1.0862"), ("GBP/JPY OTC", "PUT", "WIN", "✅", "189.42 → 189.18"), ("USD/CAD OTC", "CALL", "LOSS", "❌", "1.3642 → 1.3639"), ("AUD/USD OTC", "PUT", "WIN", "✅", "0.6582 → 0.6571"), ("EUR/GBP OTC", "CALL", "WIN", "✅", "0.8541 → 0.8553")]
    else:
        results = [("BTC/USD", "CALL", "WIN", "✅", "67250 → 67800"), ("ETH/USD", "PUT", "WIN", "✅", "3450 → 3420"), ("Gold/XAU", "CALL", "LOSS", "❌", "2034 → 2031"), ("Oil/WTI", "PUT", "WIN", "✅", "78.5 → 77.9"), ("Silver/XAG", "CALL", "WIN", "✅", "24.1 → 24.5")]
    results_text = "\n\n".join([f"📊 {r[0]} | {r[1]}\n{r[3]} Result: {r[2]}\n📈 Movement: {r[4]}" for r in results])
    wins = sum(1 for r in results if r[2] == "WIN")
    total = len(results)
    win_rate = (wins / total * 100) if total > 0 else 0
    platform_name = "QUOTEX" if platform == "quotex" else "BINOLLA"
    text = f"""
{emj('stats', '📊')} {platform_name} - Future Signals Results

{results_text}

📈 Performance Statistics:
{emj('check', '✅')} Winning signals: {wins}
{emj('cross', '❌')} Losing signals: {total - wins}
{emj('stats', '📊')} Win rate: {win_rate:.0f}%

🎯 To follow real-time results:
"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Results Channel", url=RESULTS_CHANNEL_URL, style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back", callback_data="future_results", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
        [InlineKeyboardButton("Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_referral_link(query, user_id):
    global BOT_USERNAME
    bot_username = BOT_USERNAME
    if bot_username in ["your_bot_username", "", None]:
        try:
            me = await query.bot.get_me()
            bot_username = me.username
        except Exception:
            bot_username = "your_bot_username"

    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    ref_count = get_referral_count(user_id)
    referrals = get_referrals_list(user_id)
    text = f"""
{emj('gift', '🎁')} Referral System

Your referral link:
{ref_link}

{emj('stats', '📊')} Your Statistics:
👥 Referrals count: {ref_count}
💎 Earned rewards: {ref_count * 5} points

🎁 How does the referral system work?
1️⃣ Share your link with friends
2️⃣ When they join the bot, you get credited
3️⃣ Every 10 referrals = 1 free VIP month

📋 Recent Referrals List:
"""
    if referrals:
        for ref in referrals[:5]:
            name = ref.get("first_name") or ref.get("username") or "User"
            joined = f"{emj('check', '✅')} Joined" if ref.get("joined_channel") else "⏳ Pending"
            text += f"\n• {name} - {joined}"
    else:
        text += f"\nNo referrals yet. Share your link to get started!"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Share Link", url=f"https://t.me/share/url?url={ref_link}&text=Join%20the%20Advanced%20Trading%20Signals%20Bot!", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["link"])],
        [InlineKeyboardButton("Back", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_my_account(query, user_id):
    user_data = get_user(user_id)
    if not user_data:
        await safe_edit_message(query, f"{emj('warning', '⚠️')} Your account was not found. Start over with /start", reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
        return

    join_date = user_data.get("join_date", "Unknown")[:10] if user_data.get("join_date") else "Unknown"
    plan = user_data.get("plan", "free")
    ref_count = user_data.get("referral_count", 0)
    is_premium = user_data.get("is_premium", 0)
    plan_name = "Gold" if plan == "gold" else "Monthly" if plan == "monthly" else "Weekly" if plan == "weekly" else "Free"
    status = "VIP" if is_premium else "Regular User"
    status_emoji = "👑" if is_premium else "🟢"

    name = user_data.get('first_name', 'Unknown')
    # Convert name to bold italic
    name_fancy = ""
    for c in name:
        if 'A' <= c <= 'Z':
            name_fancy += chr(0x1D468 + (ord(c) - ord('A')))
        elif 'a' <= c <= 'z':
            name_fancy += chr(0x1D482 + (ord(c) - ord('a')))
        else:
            name_fancy += c

    text = f"""{emj('user', '🪪')} <b>MY PROFILE</b>

🆔 <b>ID:</b> <code>{user_id}</code>  👤 <b>Name:</b> <b>{name_fancy}</b>
📅 <b>Joined:</b> <b>{join_date}</b>

{emj('diamond', '💎')} <b>PLAN:</b> 👑 <b>{plan_name}</b>  {status_emoji} <b>Status:</b> <b>{status}</b>

{emj('stats', '📊')} <b>STATS:</b>  👥 <b>Referrals:</b> {ref_count}  💰 <b>Rewards:</b> {ref_count * 5} pts

🏆 <b>ACHIEVEMENTS:</b>
✅ <b>Bot Member</b>
{'⏳ <b>Not Subscribed</b>' if not is_premium else '✅ <b>VIP Subscriber</b>'}  {'⏳ <b>No Referrals</b>' if ref_count == 0 else '✅ <b>Has Referrals</b>'}"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_support(query):
    text = f"""
{emj('headset', '📞')} Technical Support

We are here to help you anytime!

📞 Contact Methods:
• Direct Support: via "Contact Support" button
• Support Group: via official channel
• FAQ: below

❓ Frequently Asked Questions:

Q: How do I get signals?
A: Click the "Current Signals" button in the main menu

Q: How do I subscribe to a paid plan?
A: Click "Subscription Plans" then choose a plan

Q: How do I earn from referrals?
A: Share your referral link, every 10 referrals = 1 free VIP month

{emj('warning', '⚠️')} For urgent incidents only:
Contact support via the button below
"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact Support", url=SUPPORT_URL, style=STYLE_GREEN, icon_custom_emoji_id="5215334566549540768")],
        [InlineKeyboardButton("Official Channel", url=JOIN_CHANNEL_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["speaker"])],
        [InlineKeyboardButton("Back", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# ============================================================
# RATINGS & UPGRADE FUNCTIONS
# ============================================================
async def show_ratings(query):
    """Show the ratings page with 1-5 star buttons."""
    # Calculate average rating from database
    avg_rating = 4.5
    total_ratings = 0
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(stars), COUNT(*) FROM ratings")
        row = cursor.fetchone()
        if row and row[1] and row[1] > 0:
            avg_rating = round(row[0], 1)
            total_ratings = row[1]
        conn.close()
    except Exception:
        pass

    # Build separator line with fancy Unicode
    separator = "━━━━━━━━━━━━━━━━━━━"
    # Build stars display based on avg rating
    full_stars = int(avg_rating)
    stars_display = "⭐" * full_stars + "✨" if (avg_rating - full_stars) >= 0.5 else "⭐" * full_stars

    text = f"""{emj('star', '⭐')} 𝑹𝑨𝑻𝑬 𝑶𝑼𝑹 𝑩𝑶𝑻 {emj('star', '⭐')}

𝑾𝒆 𝒗𝒂𝒍𝒖𝒆 𝒚𝒐𝒖𝒓 𝒇𝒆𝒆𝒅𝒃𝒂𝒄𝒌! {e('😍')}

{separator}

{emj('stats', '📊')} 𝑪𝑼𝑹𝑹𝑬𝑵𝑻 𝑹𝑨𝑻𝑰𝑵𝑮:
{stars_display} {avg_rating}/5
𝑻𝒐𝒕𝒂𝒍 𝑹𝒂𝒕𝒊𝒏𝒈𝒔: {total_ratings}

{separator}

👇 𝑻𝑨𝑷 𝑻𝑯𝑬 𝑵𝑼𝑴𝑩𝑬𝑹 𝑶𝑭 𝑺𝑻𝑨𝑹𝑺:

⭐ - 𝑷𝒐𝒐𝒓
⭐⭐ - 𝑭𝒂𝒊𝒓
⭐⭐⭐ - 𝑮𝒐𝒐𝒅
⭐⭐⭐⭐ - 𝑽𝒆𝒓𝒚 𝑮𝒐𝒐𝒅
⭐⭐⭐⭐⭐ - 𝑬𝒙𝒄𝒆𝒍𝒍𝒆𝒏𝒕 {e('🎉')}

{separator}

{emj('heart', '❤️')} 𝑻𝑯𝑨𝑵𝑲 𝒀𝑶𝑼 𝑭𝑶𝑹 𝑯𝑬𝑳𝑷𝑰𝑵𝑮 𝑼𝑺 𝑰𝑴𝑷𝑹𝑶𝑽𝑬! {e('🙏')}"""
    await safe_edit_message(query, text, reply_markup=get_ratings_keyboard(), parse_mode=ParseMode.HTML)

async def submit_rating(query, stars):
    """Handle the user's rating submission."""
    stars_int = int(stars)
    # Build star display
    star_display = "⭐" * stars_int
    # Log the rating
    user_id = query.from_user.id
    user_name = query.from_user.first_name or "User"
    logging.info(f"User {user_id} ({user_name}) rated the bot: {stars_int}/5 stars")
    # Save rating to database (optional - store in users table)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Create ratings table if not exists
        cursor.execute("""CREATE TABLE IF NOT EXISTS ratings (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, stars INTEGER, date TEXT)""")
        cursor.execute("INSERT INTO ratings (user_id, stars, date) VALUES (?, ?, ?)", (user_id, stars_int, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to save rating: {e}")

    # Thank you message
    thanks_messages = {
        1: "We're sorry to hear that. Please let us know how we can improve!",
        2: "Thank you for your feedback. We'll work hard to improve!",
        3: "Thanks for your rating! We're glad you're satisfied.",
        4: "Thank you! We're happy you had a great experience!",
        5: "Wow, thank you so much for the 5-star rating! We're thrilled! 🎉",
    }
    msg = thanks_messages.get(stars_int, "Thank you for your rating!")

    text = f"""
{emj('check', '✅')} Rating Submitted!

You rated us: {star_display} ({stars_int}/5)

{msg}

{emj('heart', '❤️')} Thank you for taking the time to rate QuantVexa Bot!
"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_upgrade(query):
    """Show the upgrade page with plans 50, 75, 100."""
    # Calculate average rating from database
    avg_rating = 4.5
    total_ratings = 0
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(stars), COUNT(*) FROM ratings")
        row = cursor.fetchone()
        if row and row[1] and row[1] > 0:
            avg_rating = round(row[0], 1)
            total_ratings = row[1]
        conn.close()
    except Exception:
        pass

    # Build separator line with fancy Unicode
    separator = "━━━━━━━━━━━━━━━━━━━"
    text = f"""{e('🚀')} 𝑼𝑷𝑮𝑹𝑨𝑫𝑬 𝒀𝑶𝑼𝑹 𝑷𝑳𝑨𝑵 {e('🚀')}

𝑻𝒂𝒌𝒆 𝒚𝒐𝒖𝒓 𝒕𝒓𝒂𝒅𝒊𝒏𝒈 𝒕𝒐 𝒕𝒉𝒆 𝒏𝒆𝒙𝒕 𝒍𝒆𝒗𝒆𝒍!

{separator}

{emj('calendar', '📅')} 𝑼𝑷𝑮𝑹𝑨𝑫𝑬 $50
𝑫𝒖𝒓𝒂𝒕𝒊𝒐𝒏: 30 𝒅𝒂𝒚𝒔
• 𝑼𝒏𝒍𝒊𝒎𝒊𝒕𝒆𝒅 𝒔𝒊𝒈𝒏𝒂𝒍𝒔
• 𝑭𝒖𝒍𝒍 𝒂𝒄𝒄𝒆𝒔𝒔 𝒕𝒐 𝒕𝒊𝒎𝒆 𝒍𝒊𝒔𝒕
• 𝑰𝒏𝒔𝒕𝒂𝒏𝒕 𝒂𝒍𝒆𝒓𝒕𝒔
• 𝑽𝑰𝑷 𝒔𝒖𝒑𝒑𝒐𝒓𝒕

{separator}

{emj('diamond', '💎')} 𝑼𝑷𝑮𝑹𝑨𝑫𝑬 $75
𝑫𝒖𝒓𝒂𝒕𝒊𝒐𝒏: 60 𝒅𝒂𝒚𝒔
• 𝑨𝒍𝒍 $50 𝒇𝒆𝒂𝒕𝒖𝒓𝒆𝒔
• 𝑻𝒐𝒑 𝒑𝒂𝒚𝒐𝒖𝒕 𝒄𝒖𝒓𝒓𝒆𝒏𝒄𝒊𝒆𝒔 𝒂𝒏𝒂𝒍𝒚𝒔𝒊𝒔
• 𝑬𝒙𝒄𝒍𝒖𝒔𝒊𝒗𝒆 𝒇𝒖𝒕𝒖𝒓𝒆 𝒔𝒊𝒈𝒏𝒂𝒍𝒔
• 𝑾𝒆𝒆𝒌𝒍𝒚 𝒕𝒓𝒂𝒊𝒏𝒊𝒏𝒈 𝒔𝒆𝒔𝒔𝒊𝒐𝒏𝒔

{separator}

{emj('crown', '👑')} 𝑼𝑷𝑮𝑹𝑨𝑫𝑬 $100
𝑫𝒖𝒓𝒂𝒕𝒊𝒐𝒏: 90 𝒅𝒂𝒚𝒔
• 𝑨𝒍𝒍 $75 𝒇𝒆𝒂𝒕𝒖𝒓𝒆𝒔
• 𝑷𝒆𝒓𝒔𝒐𝒏𝒂𝒍 𝒂𝒄𝒄𝒐𝒖𝒏𝒕 𝒎𝒂𝒏𝒂𝒈𝒆𝒓
• 𝑪𝒖𝒔𝒕𝒐𝒎 𝑽𝑰𝑷 𝒔𝒊𝒈𝒏𝒂𝒍𝒔
• 𝑬𝒙𝒄𝒍𝒖𝒔𝒊𝒗𝒆 𝒕𝒓𝒂𝒊𝒏𝒊𝒏𝒈 𝒘𝒐𝒓𝒌𝒔𝒉𝒐𝒑𝒔

{separator}

{emj('lightning', '⚡')} 𝑺𝑬𝑳𝑬𝑪𝑻 𝑨 𝑷𝑳𝑨𝑵 𝑩𝑬𝑳𝑶𝑾 𝑻𝑶 𝑼𝑷𝑮𝑹𝑨𝑫𝑬:

{emj('warning', '⚠️')} 𝑻𝒐 𝒔𝒖𝒃𝒔𝒄𝒓𝒊𝒃𝒆, 𝒄𝒐𝒏𝒕𝒂𝒄𝒕 𝒕𝒆𝒄𝒉𝒏𝒊𝒄𝒂𝒍 𝒔𝒖𝒑𝒑𝒐𝒓𝒕"""
    await safe_edit_message(query, text, reply_markup=get_upgrade_keyboard(), parse_mode=ParseMode.HTML)

async def show_upgrade_details(query, price):
    """Show details for a specific upgrade plan."""
    plans = {
        "50": {"name": "Standard Upgrade", "price": "$50", "duration": "30 days", "features": ["Unlimited signals", "Full access to time list", "Instant alerts", "VIP support"]},
        "75": {"name": "Premium Upgrade", "price": "$75", "duration": "60 days", "features": ["All Standard features", "Top payout currencies analysis", "Exclusive future signals", "Weekly training sessions"]},
        "100": {"name": "Gold Upgrade", "price": "$100", "duration": "90 days", "features": ["All Premium features", "Personal account manager", "Custom VIP signals", "Exclusive training workshops"]},
    }
    plan = plans.get(price, plans["50"])
    features_text = "\n".join([f"{emj('check', '✅')} {f}" for f in plan["features"]])

    text = f"""
{emj('crown', '👑')} {plan['name']} - {plan['price']}

📋 Plan Details:

💰 Price: {plan['price']}
⏰ Duration: {plan['duration']}

{emj('star', '⭐')} Included Features:
{features_text}

💳 To subscribe to this plan:
Contact technical support via the Support button in the main menu

{emj('lightning', '⚡')} Upgrade now and unlock premium features!
"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Upgrades", callback_data="upgrade", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["crown"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# ============================================================
# NEW BUTTON HANDLERS (from screenshot)
# ============================================================
async def show_schedule_session(query):
    text = f"""
{emj('calendar', '📅')} 𝑺𝑪𝑯𝑬𝑫𝑼𝑳𝑬 𝑺𝑬𝑺𝑺𝑰𝑶𝑵

𝑺𝒆𝒕 𝒖𝒑 𝒚𝒐𝒖𝒓 𝒕𝒓𝒂𝒅𝒊𝒏𝒈 𝒔𝒄𝒉𝒆𝒅𝒖𝒍𝒆:

𝑴𝒐𝒓𝒏𝒊𝒏𝒈 𝑺𝒆𝒔𝒔𝒊𝒐𝒏: 09:00 - 12:00
𝑨𝒇𝒕𝒆𝒓𝒏𝒐𝒐𝒏 𝑺𝒆𝒔𝒔𝒊𝒐𝒏: 14:00 - 17:00
𝑬𝒗𝒆𝒏𝒊𝒏𝒈 𝑺𝒆𝒔𝒔𝒊𝒐𝒏: 19:00 - 22:00

{emj('warning', '⚠️')} 𝑪𝒉𝒐𝒐𝒔𝒆 𝒂 𝒔𝒆𝒔𝒔𝒊𝒐𝒏 𝒕𝒉𝒂𝒕 𝒔𝒖𝒊𝒕𝒔 𝒚𝒐𝒖𝒓 𝒕𝒊𝒎𝒆 𝒛𝒐𝒏𝒆
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_settings(query):
    """Show settings page with interactive buttons."""
    user_id = query.from_user.id
    # Get current settings from DB
    settings = _get_user_settings(user_id)
    platform = settings.get("platform", "QUOTEX")
    expiry = settings.get("expiry", "M1")
    risk = settings.get("risk", "Medium")
    notifications = settings.get("notifications", "ON")

    text = f"""{emj('gear', '⚙️')} <b>SETTINGS</b>

<b>Trading Settings:</b>
📊 <b>Platform:</b> {platform}
⏱️ <b>Expiry:</b> {expiry}
⚠️ <b>Risk Level:</b> {risk}

<b>Notifications:</b>
🔔 <b>Signal Alerts:</b> {notifications}

👇 <b>TAP TO CHANGE</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"Platform: {platform}", callback_data="settings_platform", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
            InlineKeyboardButton(f"Expiry: {expiry}", callback_data="settings_expiry", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["clock_premium"]),
        ],
        [
            InlineKeyboardButton(f"Risk: {risk}", callback_data="settings_risk", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["warning"]),
            InlineKeyboardButton(f"Alerts: {notifications}", callback_data="settings_notifications", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["bell"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


def _get_user_settings(user_id: int) -> dict:
    """Get user settings from DB."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_settings (user_id INTEGER PRIMARY KEY, platform TEXT, expiry TEXT, risk TEXT, notifications TEXT)")
        cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return {"platform": "QUOTEX", "expiry": "M1", "risk": "Medium", "notifications": "ON"}
    except Exception:
        return {"platform": "QUOTEX", "expiry": "M1", "risk": "Medium", "notifications": "ON"}


def _save_user_setting(user_id: int, key: str, value: str):
    """Save a single user setting."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_settings (user_id INTEGER PRIMARY KEY, platform TEXT, expiry TEXT, risk TEXT, notifications TEXT)")
        # Get existing or create
        cursor.execute("SELECT user_id FROM user_settings WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            cursor.execute(f"UPDATE user_settings SET {key} = ? WHERE user_id = ?", (value, user_id))
        else:
            cursor.execute(f"INSERT INTO user_settings (user_id, {key}) VALUES (?, ?)", (user_id, value))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to save setting: {e}")


async def settings_change_platform(query, user_id):
    """Show platform selection."""
    text = f"""{emj('gear', '⚙️')} <b>SELECT PLATFORM</b>

👇 Choose your default platform:"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="settings_set_platform_QUOTEX", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="settings_set_platform_BINOLLA", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Settings", callback_data="settings", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def settings_change_expiry(query, user_id):
    """Show expiry selection."""
    text = f"""{emj('gear', '⚙️')} <b>SELECT EXPIRY</b>

👇 Choose default expiry time:"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("M1", callback_data="settings_set_expiry_M1", style=STYLE_BLUE),
            InlineKeyboardButton("M5", callback_data="settings_set_expiry_M5", style=STYLE_BLUE),
            InlineKeyboardButton("M15", callback_data="settings_set_expiry_M15", style=STYLE_BLUE),
        ],
        [
            InlineKeyboardButton("M30", callback_data="settings_set_expiry_M30", style=STYLE_BLUE),
        ],
        [InlineKeyboardButton("Back to Settings", callback_data="settings", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def settings_change_risk(query, user_id):
    """Show risk level selection."""
    text = f"""{emj('gear', '⚙️')} <b>SELECT RISK LEVEL</b>

👇 Choose your risk level:"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Low", callback_data="settings_set_risk_Low", style=STYLE_GREEN),
            InlineKeyboardButton("Medium", callback_data="settings_set_risk_Medium", style=STYLE_BLUE),
            InlineKeyboardButton("High", callback_data="settings_set_risk_High", style=STYLE_RED),
        ],
        [InlineKeyboardButton("Back to Settings", callback_data="settings", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def settings_change_notifications(query, user_id):
    """Show notifications selection."""
    text = f"""{emj('gear', '⚙️')} <b>NOTIFICATIONS</b>

👇 Choose notification setting:"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ON", callback_data="settings_set_notifications_ON", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("OFF", callback_data="settings_set_notifications_OFF", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"]),
        ],
        [InlineKeyboardButton("Back to Settings", callback_data="settings", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_checker(query, checker_name):
    text = f"""
{emj('magnifier', '🔍')} {checker_name.upper()}

𝑪𝒉𝒆𝒄𝒌𝒊𝒏𝒈 𝒎𝒂𝒓𝒌𝒆𝒕 𝒔𝒕𝒂𝒕𝒖𝒔...

𝑺𝒕𝒂𝒕𝒖𝒔: 𝑨𝒄𝒕𝒊𝒗𝒆 ✅
𝑳𝒂𝒔𝒕 𝑼𝒑𝒅𝒂𝒕𝒆: {datetime.now().strftime('%H:%M:%S')}

𝑨𝒗𝒂𝒊𝒍𝒂𝒃𝒍𝒆 𝑷𝒂𝒊𝒓𝒔:
• 𝑬𝑼𝑹/𝑼𝑺𝑫
• 𝑮𝑩𝑷/𝑱𝑷𝒀
• 𝑼𝑺𝑫/𝑱𝑷𝒀
• 𝑨𝑼𝑫/𝑪𝑨𝑫

{emj('warning', '⚠️')} 𝑹𝒆𝒇𝒓𝒆𝒔𝒉 𝒕𝒐 𝒄𝒉𝒆𝒄𝒌 𝒂𝒈𝒂𝒊𝒏
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_market_fs(query, market_name):
    text = f"""
{emj('chart', '📈')} {market_name.upper()} 𝑭𝑺

𝑴𝒂𝒓𝒌𝒆𝒕 𝑭𝒖𝒕𝒖𝒓𝒆 𝑺𝒊𝒈𝒏𝒂𝒍𝒔:

𝑨𝒄𝒕𝒊𝒗𝒆 𝑷𝒂𝒊𝒓𝒔:
• 𝑬𝑼𝑹/𝑼𝑺𝑫 - 𝑪𝑨𝑳𝑳 - 92%
• 𝑮𝑩𝑷/𝑱𝑷𝒀 - 𝑷𝑼𝑻 - 88%
• 𝑼𝑺𝑫/𝑪𝑨𝑫 - 𝑪𝑨𝑳𝑳 - 90%

𝑼𝒑𝒅𝒂𝒕𝒆𝒅: {datetime.now().strftime('%H:%M')}

{emj('warning', '⚠️')} 𝑭𝒖𝒕𝒖𝒓𝒆 𝒔𝒊𝒈𝒏𝒂𝒍𝒔 𝒂𝒓𝒆 𝒑𝒓𝒆𝒎𝒊𝒖𝒎 𝒇𝒆𝒂𝒕𝒖𝒓𝒆
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_future_live(query):
    text = f"""
{emj('crystal_ball', '🔮')} 𝑭𝑼𝑻𝑼𝑹𝑬 𝑳𝑰𝑽𝑬

𝑼𝒑𝒄𝒐𝒎𝒊𝒏𝒈 𝑳𝒊𝒗𝒆 𝑺𝒊𝒈𝒏𝒂𝒍𝒔:

𝑵𝒆𝒙𝒕 𝑺𝒊𝒈𝒏𝒂𝒍:
• 𝑷𝒂𝒊𝒓: 𝑬𝑼𝑹/𝑼𝑺𝑫
• 𝑻𝒊𝒎𝒆: {(datetime.now() + timedelta(minutes=15)).strftime('%H:%M')}
• 𝑫𝒊𝒓𝒆𝒄𝒕𝒊𝒐𝒏: 𝑪𝑨𝑳𝑳
• 𝑬𝒙𝒑𝒊𝒓𝒚: 𝑴1

{emj('lightning', '⚡')} 𝑺𝒕𝒂𝒚 𝒕𝒖𝒏𝒆𝒅!
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_live_signal(query):
    """Show broker selection for live signal."""
    text = f"""{emj('lightning_premium', '⚡')} <b>LIVE SIGNAL</b>

👇 <b>CHOOSE BROKER</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="live_signal_quotex", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="live_signal_binolla", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_live_signal_market(query, broker):
    """Show market type selection (OTC / Global)."""
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    text = f"""{emj('lightning_premium', '⚡')} <b>LIVE SIGNAL - {broker_name}</b>

👇 <b>CHOOSE MARKET TYPE</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("OTC Market", callback_data=f"live_signal_market_otc_{broker}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["chart"]),
            InlineKeyboardButton("Global Market", callback_data=f"live_signal_market_global_{broker}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["globe"]),
        ],
        [InlineKeyboardButton("Back to Broker", callback_data="live_signal", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_live_signal_duration(query, broker, market):
    """Show trade duration selection."""
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    market_name = "OTC" if market == "otc" else "Global"
    text = f"""{emj('lightning_premium', '⚡')} <b>LIVE SIGNAL - {broker_name} {market_name}</b>

👇 <b>CHOOSE DURATION</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1M", callback_data=f"live_signal_dur_1M_{broker}_{market}", style=STYLE_BLUE),
            InlineKeyboardButton("2M", callback_data=f"live_signal_dur_2M_{broker}_{market}", style=STYLE_BLUE),
            InlineKeyboardButton("3M", callback_data=f"live_signal_dur_3M_{broker}_{market}", style=STYLE_BLUE),
        ],
        [
            InlineKeyboardButton("4M", callback_data=f"live_signal_dur_4M_{broker}_{market}", style=STYLE_BLUE),
            InlineKeyboardButton("5M", callback_data=f"live_signal_dur_5M_{broker}_{market}", style=STYLE_BLUE),
        ],
        [InlineKeyboardButton("Back to Market", callback_data=f"live_signal_broker_{broker}", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_live_signal_bot_type(query, broker, market, duration):
    """Show bot type selection (Strong / Medium / Hybrid)."""
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    market_name = "OTC" if market == "otc" else "Global"
    text = f"""{emj('lightning_premium', '⚡')} <b>LIVE SIGNAL - {broker_name} {market_name}</b>

Duration: {duration}

👇 <b>CHOOSE BOT TYPE</b>"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Strong Bot", callback_data=f"live_signal_bot_strong_{broker}_{market}_{duration}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"])],
        [InlineKeyboardButton("Medium Bot", callback_data=f"live_signal_bot_medium_{broker}_{market}_{duration}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Hybrid Bot", callback_data=f"live_signal_bot_hybrid_{broker}_{market}_{duration}", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["fire"])],
        [InlineKeyboardButton("Back to Duration", callback_data=f"live_signal_market_{market}_{broker}", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_live_signal_final(query, broker, market, duration, bot_type):
    """Show final message - signals coming soon."""
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    market_name = "OTC" if market == "otc" else "Global"
    bot_names = {"strong": "Strong Bot", "medium": "Medium Bot", "hybrid": "Hybrid Bot"}
    bot_name = bot_names.get(bot_type, bot_type)

    text = f"""{emj('check', '✅')} <b>LIVE SIGNAL CONFIGURED</b>

Broker: {broker_name}
Market: {market_name}
Duration: {duration}
Bot Type: {bot_name}

The bot will select the best currency pairs
and send you live signals automatically.

{emj('lightning_premium', '⚡')} Signals are coming soon - under development"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_bug_signal(query):
    """Bug Signal is currently disabled."""
    text = f"""
{emj('bug', '🐛')} 𝑩𝑼𝑮 𝑺𝑰𝑮𝑵𝑨𝑳

{emj('warning', '⚠️')} 𝑪𝑶𝑴𝑰𝑵𝑮 𝑺𝑶𝑶𝑵

This feature is currently under development
and will be available soon.

{emj('lightning', '⚡')} Stay tuned for updates!
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_live_payouts(query):
    """Show broker selection for live payouts."""
    text = f"""{emj('diamond_premium', '💎')} 𝙻𝙸𝚅𝙴 𝙿𝙰𝚈𝙾𝚄𝚃𝚂

👇 𝙲𝙷𝙾𝙾𝚂𝙴 𝙱𝚁𝙾𝙺𝙴𝚁

Select broker to view live payouts."""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="live_payouts_quotex", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="live_payouts_binolla", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_live_payouts_pairs(query, broker: str):
    """Show live payouts for a broker with auto-updating payout percentages."""
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    import random as _random
    pairs_with_payouts = []
    for pair_name, base_payout in SIGNAL_SESSION_PAIRS[:20]:
        variation = _random.randint(-5, 5)
        actual_payout = max(50, min(99, base_payout + variation))
        pairs_with_payouts.append((pair_name, actual_payout))

    text = _build_live_payouts_text(broker_name, pairs_with_payouts)
    keyboard = _build_live_payouts_keyboard(broker, pairs_with_payouts)

    chat_id = query.message.chat_id
    message_id = query.message.message_id
    bot = query.message.get_bot()

    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    # Start auto-update loop using asyncio
    import asyncio
    asyncio.create_task(_auto_update_live_payouts_loop(bot, chat_id, message_id, broker))


def _build_live_payouts_text(broker_name: str, pairs_with_payouts: list) -> str:
    """Build the live payouts message text."""
    return f"""{emj('diamond_premium', '💎')} 𝙻𝙸𝚅𝙴 𝙿𝙰𝚈𝙾𝚄𝚃𝚂 - {broker_name}

👇 𝙻𝙸𝚅𝙴 𝙿𝙰𝚈𝙾𝚄𝚃 𝚁𝙰𝚃𝙴𝚂

Updated: {datetime.now().strftime('%H:%M:%S')}

🟦 Blue = High payout (85%+)
🟩 Green = Medium payout (70-84%)
🟥 Red = Low payout (&lt;70%)"""


def _build_live_payouts_keyboard(broker: str, pairs_with_payouts: list) -> InlineKeyboardMarkup:
    """Build the live payouts keyboard."""
    keyboard_rows = []
    row = []
    for pair_name, payout in pairs_with_payouts:
        label = f"{pair_name} {payout}%"
        style = _get_pair_color_style(payout)
        row.append(InlineKeyboardButton(label, callback_data="live_payouts_none", style=style))
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)

    keyboard_rows.append([
        InlineKeyboardButton("Back to Broker", callback_data="live_payouts", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"]),
        InlineKeyboardButton("Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"]),
    ])

    return InlineKeyboardMarkup(keyboard_rows)


async def _auto_update_live_payouts_loop(bot, chat_id, message_id, broker):
    """Auto-update live payouts message every 3 seconds using asyncio."""
    import asyncio
    import random as _random
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"

    for _ in range(100):  # Max 100 updates (~5 minutes)
        await asyncio.sleep(3)
        try:
            # Generate new random payouts
            pairs_with_payouts = []
            for pair_name, base_payout in SIGNAL_SESSION_PAIRS[:20]:
                variation = _random.randint(-5, 5)
                actual_payout = max(50, min(99, base_payout + variation))
                pairs_with_payouts.append((pair_name, actual_payout))

            text = _build_live_payouts_text(broker_name, pairs_with_payouts)
            keyboard = _build_live_payouts_keyboard(broker, pairs_with_payouts)

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:
            err_str = str(e)
            if "Message is not modified" in err_str or "message is not modified" in err_str.lower():
                continue
            elif "not found" in err_str.lower() or "deleted" in err_str.lower():
                break  # Message deleted or user navigated away
            else:
                logging.warning(f"Auto-update live payouts error: {e}")
                break

async def show_news_signal(query):
    text = f"""
{emj('sparkles', '✨')} 𝑵𝑬𝑾𝑺 𝑺𝑰𝑮𝑵𝑨𝑳

𝑳𝒂𝒕𝒆𝒔𝒕 𝑴𝒂𝒓𝒌𝒆𝒕 𝑵𝒆𝒘𝒔:

📰 𝑼𝑺 𝑭𝒆𝒅 𝑹𝒂𝒕𝒆 𝑫𝒆𝒄𝒊𝒔𝒊𝒐𝒏 - 𝑯𝒊𝒈𝒉 𝑰𝒎𝒑𝒂𝒄𝒕
📰 𝑵𝒐𝒏-𝑭𝒂𝒓𝒎 𝑷𝒂𝒚𝒓𝒐𝒍𝒍𝒔 - 𝑴𝒆𝒅𝒊𝒖𝒎 𝑰𝒎𝒑𝒂𝒄𝒕
📰 𝑬𝑼 𝑪𝑷𝑰 𝑫𝒂𝒕𝒂 - 𝑴𝒆𝒅𝒊𝒖𝒎 𝑰𝒎𝒑𝒂𝒄𝒕

𝑼𝒑𝒅𝒂𝒕𝒆𝒅: {datetime.now().strftime('%H:%M')}

{emj('warning', '⚠️')} 𝑵𝒆𝒘𝒔 𝒄𝒂𝒏 𝒂𝒇𝒇𝒆𝒄𝒕 𝒎𝒂𝒓𝒌𝒆𝒕 𝒗𝒐𝒍𝒂𝒕𝒊𝒍𝒊𝒕𝒚
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_ai_filter(query):
    text = f"""
{emj('person', '👤')} 𝑨𝑰 𝑭𝑰𝑳𝑻𝑬𝑹

𝑨𝑰-𝑷𝒐𝒘𝒆𝒓𝒆𝒅 𝑺𝒊𝒈𝒏𝒂𝒍 𝑭𝒊𝒍𝒕𝒆𝒓:

𝑭𝒊𝒍𝒕𝒆𝒓 𝑺𝒆𝒕𝒕𝒊𝒏𝒈𝒔:
• 𝑴𝒊𝒏𝒊𝒎𝒖𝒎 𝑪𝒐𝒏𝒇𝒊𝒅𝒆𝒏𝒄𝒆: 85%
• 𝑴𝒂𝒙𝒊𝒎𝒖𝒎 𝑹𝒊𝒔𝒌: 𝑴𝒆𝒅𝒊𝒖𝒎
• 𝑷𝒓𝒆𝒇𝒆𝒓𝒓𝒆𝒅 𝑷𝒂𝒊𝒓𝒔: 𝑴𝒂𝒋𝒐𝒓

𝑨𝑰 𝑺𝒕𝒂𝒕𝒖𝒔: 𝑨𝒄𝒕𝒊𝒗𝒆 ✅
𝑳𝒂𝒔𝒕 𝑨𝒏𝒂𝒍𝒚𝒔𝒊𝒔: {datetime.now().strftime('%H:%M:%S')}

{emj('lightning', '⚡')} 𝑨𝑰 𝒊𝒔 𝒂𝒏𝒂𝒍𝒚𝒛𝒊𝒏𝒈 𝒎𝒂𝒓𝒌𝒆𝒕𝒔 24/7
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_ai_assistant(query):
    text = f"""
{emj('robot', '🤖')} 𝑨𝑰 𝑨𝑺𝑺𝑰𝑺𝑻𝑨𝑵𝑻

𝒀𝒐𝒖𝒓 𝑨𝑰 𝑻𝒓𝒂𝒅𝒊𝒏𝒈 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕:

𝑰 𝒄𝒂𝒏 𝒉𝒆𝒍𝒑 𝒚𝒐𝒖 𝒘𝒊𝒕𝒉:
• 𝑴𝒂𝒓𝒌𝒆𝒕 𝒂𝒏𝒂𝒍𝒚𝒔𝒊𝒔
• 𝑺𝒊𝒈𝒏𝒂𝒍 𝒊𝒏𝒕𝒆𝒓𝒑𝒓𝒆𝒕𝒂𝒕𝒊𝒐𝒏
• 𝑹𝒊𝒔𝒌 𝒎𝒂𝒏𝒂𝒈𝒆𝒎𝒆𝒏𝒕
• 𝑺𝒕𝒓𝒂𝒕𝒆𝒈𝒚 𝒕𝒊𝒑𝒔

{emj('lightning', '⚡')} 𝑨𝒔𝒌 𝒎𝒆 𝒂𝒏𝒚𝒕𝒉𝒊𝒏𝒈 𝒂𝒃𝒐𝒖𝒕 𝒕𝒓𝒂𝒅𝒊𝒏𝒈!

{emj('warning', '⚠️')} 𝑵𝒐𝒕 𝒇𝒊𝒏𝒂𝒏𝒄𝒊𝒂𝒍 𝒂𝒅𝒗𝒊𝒄𝒆
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_formatter(query):
    text = f"""
{emj('swirl', '🌀')} 𝑭𝑶𝑹𝑴𝑨𝑻𝑻𝑬𝑹

𝑺𝒊𝒈𝒏𝒂𝒍 𝑭𝒐𝒓𝒎𝒂𝒕𝒕𝒆𝒓:

𝑭𝒐𝒓𝒎𝒂𝒕 𝒚𝒐𝒖𝒓 𝒔𝒊𝒈𝒏𝒂𝒍𝒔:
• 𝑺𝒕𝒂𝒏𝒅𝒂𝒓𝒅 𝒇𝒐𝒓𝒎𝒂𝒕
• 𝑪𝒖𝒔𝒕𝒐𝒎 𝒇𝒐𝒓𝒎𝒂𝒕
• 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝒇𝒐𝒓𝒎𝒂𝒕

𝑺𝒆𝒏𝒅 𝒚𝒐𝒖𝒓 𝒔𝒊𝒈𝒏𝒂𝒍 𝒕𝒐 𝒇𝒐𝒓𝒎𝒂𝒕 𝒊𝒕.

{emj('lightning', '⚡')} 𝑸𝒖𝒊𝒄𝒌 𝒂𝒏𝒅 𝒆𝒂𝒔𝒚 𝒇𝒐𝒓𝒎𝒂𝒕𝒕𝒊𝒏𝒈
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_market_filters(query):
    text = f"""
{emj('stats', '📊')} 𝑴𝑨𝑹𝑲𝑬𝑬𝑻 𝑭𝑰𝑳𝑻𝑬𝑹𝑺

𝑨𝒗𝒂𝒊𝒍𝒂𝒃𝒍𝒆 𝑭𝒊𝒍𝒕𝒆𝒓𝒔:

• 𝑷𝒂𝒚𝒐𝒖𝒕 𝑭𝒊𝒍𝒕𝒆𝒓: 90%+
• 𝑽𝒐𝒍𝒂𝒕𝒊𝒍𝒊𝒕𝒚 𝑭𝒊𝒍𝒕𝒆𝒓: 𝑴𝒆𝒅𝒊𝒖𝒎
• 𝑻𝒊𝒎𝒆 𝑭𝒊𝒍𝒕𝒆𝒓: 𝑴1-𝑴5
• 𝑪𝒖𝒓𝒓𝒆𝒏𝒄𝒚 𝑭𝒊𝒍𝒕𝒆𝒓: 𝑴𝒂𝒋𝒐𝒓

𝑨𝒄𝒕𝒊𝒗𝒆 𝑭𝒊𝒍𝒕𝒆𝒓𝒔: 4

{emj('lightning', '⚡')} 𝑭𝒊𝒍𝒕𝒆𝒓𝒔 𝒉𝒆𝒍𝒑 𝒇𝒊𝒏𝒅 𝒕𝒉𝒆 𝒃𝒆𝒔𝒕 𝒔𝒊𝒈𝒏𝒂𝒍𝒔
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_swap_cp(query):
    """Swap C/P is currently disabled."""
    text = f"""
{emj('swap', '🔄')} 𝑺𝑾𝑨𝑷 𝑪/𝑷

{emj('warning', '⚠️')} 𝑪𝑶𝑴𝑰𝑵𝑮 𝑺𝑶𝑶𝑵

This feature is currently under development
and will be available soon.

{emj('lightning', '⚡')} Stay tuned for updates!
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_tz_converter(query):
    """Show timezone selector with all UTC offsets as buttons."""
    user_id = query.from_user.id
    # Get user's current timezone
    user_tz = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_timezone (user_id INTEGER PRIMARY KEY, utc_offset TEXT)")
        cursor.execute("SELECT utc_offset FROM user_timezone WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            user_tz = row["utc_offset"]
        conn.close()
    except Exception:
        pass

    if user_tz:
        tz_text = f"""{emj('check', '✅')} 𝒀𝒐𝒖𝒓 𝑻𝒊𝒎𝒆𝒛𝒐𝒏𝒆: UTC{user_tz}

💡 All signal times will be displayed
in your selected timezone."""
    else:
        tz_text = f"""{emj('warning', '⚠️')} 𝑵𝒐 𝑻𝒊𝒎𝒆𝒛𝒐𝒏𝒆 𝑺𝒆𝒕

Select your timezone below to convert
signal times to your local time."""

    text = f"""{emj('alarm', '⏰')} 𝑻𝑰𝑴𝑬𝒁𝑶𝑵𝑬 𝑺𝑬𝑳𝑬𝑪𝑻𝑶𝑹

{tz_text}

━━━━━━━━━━━━━━━━━━━━

👇 𝑺𝒆𝒍𝒆𝒄𝒕 𝒚𝒐𝒖𝒓 𝒕𝒊𝒎𝒆𝒛𝒐𝒏𝒆:"""

    # All UTC offsets
    offsets = [
        "-11:00", "-10:00", "-09:30", "-09:00", "-08:00", "-07:00",
        "-06:00", "-05:00", "-04:00", "-03:30", "-03:00", "-02:00",
        "-01:00", "+00:00", "+01:00", "+02:00", "+03:00", "+03:30",
        "+04:00", "+04:30", "+05:00", "+05:30", "+05:45", "+06:00",
        "+06:30", "+07:00", "+08:00", "+08:45", "+09:00", "+09:30",
        "+10:00", "+10:30", "+11:00", "+12:00", "+13:00", "+13:45", "+14:00",
    ]

    # Build keyboard: 3 buttons per row
    keyboard_rows = []
    row = []
    for offset in offsets:
        sign = "➖" if offset.startswith("-") else "➕"
        label = f"UTC{offset}"
        # Highlight current selection
        if user_tz == offset:
            label = f"✅ UTC{offset}"
        row.append(InlineKeyboardButton(label, callback_data=f"set_tz_{offset}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["alarm"]))
        if len(row) == 3:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)

    keyboard_rows.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def set_user_timezone(query, user_id, utc_offset):
    """Save the user's selected timezone."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_timezone (user_id INTEGER PRIMARY KEY, utc_offset TEXT)")
        cursor.execute("INSERT OR REPLACE INTO user_timezone (user_id, utc_offset) VALUES (?, ?)", (user_id, utc_offset))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to save timezone: {e}")

    text = f"""{emj('check', '✅')} 𝑻𝒊𝒎𝒆𝒛𝒐𝒏𝒆 𝑼𝒑𝒅𝒂𝒕𝒆𝒅!

{emj('alarm', '⏰')} 𝒀𝒐𝒖𝒓 𝑻𝒊𝒎𝒆𝒛𝒐𝒏𝒆: UTC{utc_offset}

💡 All signal times will now be displayed
in your selected timezone (UTC{utc_offset}).

{emj('lightning', '⚡')} You can change your timezone
anytime from the TZ Converter menu."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Timezone", callback_data="tz_converter", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["alarm"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# ============================================================
# SIGNAL SCHEDULE FUNCTIONS (Personal scheduling)
# ============================================================
async def set_user_schedule(query, user_id, start_time, end_time):
    """Save the user's signal schedule."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_schedule (user_id INTEGER PRIMARY KEY, start_time TEXT, end_time TEXT, enabled INTEGER DEFAULT 1)")
        cursor.execute("INSERT OR REPLACE INTO user_schedule (user_id, start_time, end_time, enabled) VALUES (?, ?, ?, 1)", (user_id, start_time, end_time))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to save schedule: {e}")

    text = f"""{emj('check', '✅')} 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆 𝑺𝒆𝒕 𝑺𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚!

{emj('clock', '⏰')} 𝑺𝒕𝒂𝒓𝒕 𝑻𝒊𝒎𝒆: {start_time}
{emj('clock', '⏰')} 𝑬𝒏𝒅 𝑻𝒊𝒎𝒆: {end_time}

💡 The bot will automatically send you
trading signals during this time period
every day.

{emj('lightning', '⚡')} You can pause or delete the schedule
from the Time Schedule menu."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Schedule", callback_data="time_list", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["clock_premium"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def pause_user_schedule(query, user_id):
    """Pause the user's signal schedule."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE user_schedule SET enabled = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to pause schedule: {e}")
    await show_time_list(query)

async def delete_user_schedule(query, user_id):
    """Delete the user's signal schedule."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_schedule WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to delete schedule: {e}")

    text = f"""{emj('cross', '❌')} 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆 𝑫𝒆𝒍𝒆𝒕𝒆𝒅

Your signal schedule has been deleted.
You will no longer receive automatic signals.

💡 You can set a new schedule anytime
from the Time Schedule menu."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Schedule", callback_data="time_list", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["clock_premium"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# ============================================================
# 5) ADMIN FUNCTIONS
# ============================================================
async def admin_new_signal(query, context):
    if not is_admin(query.from_user.id):
        await safe_edit_message(query, f"{emj('cross', '❌')} Access Denied - Admins only", reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
        return ConversationHandler.END
    text = f"""
📝 Create New Signal

Send the signal in the following format:
Currency | Direction | Entry Price | Expiry

Example:
EUR/USD | CALL | 1.0856 | M1

{emj('warning', '⚠️')} Send /cancel to cancel
"""
    await safe_edit_message(query, text, parse_mode=ParseMode.HTML)
    return WAITING_SIGNAL_INPUT

async def receive_signal_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    text = update.message.text
    parts = [p.strip() for p in text.split("|")]
    if len(parts) != 4:
        await update.message.reply_text(f"{emj('warning', '⚠️')} Invalid format! Use:\nCurrency | Direction | Price | Expiry", parse_mode=ParseMode.HTML)
        return WAITING_SIGNAL_INPUT
    currency, direction, entry_price, expiry = parts
    try:
        price = float(entry_price)
    except ValueError:
        await update.message.reply_text(f"{emj('warning', '⚠️')} Price must be a number", parse_mode=ParseMode.HTML)
        return WAITING_SIGNAL_INPUT

    signal_id = add_signal(currency, direction, price, expiry)
    context.user_data["pending_signal"] = {"id": signal_id, "currency": currency, "direction": direction, "price": price, "expiry": expiry}
    text = f"""
{emj('check', '✅')} Signal Ready

📊 Currency: {currency}
📈 Direction: {direction}
💰 Entry: {price}
⏰ Expiry: {expiry}

Do you want to send it to the signals channel?
"""
    await update.message.reply_text(text, reply_markup=get_admin_confirm_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

async def admin_confirm_send(query, context):
    if not is_admin(query.from_user.id):
        return
    signal = context.user_data.get("pending_signal")
    if not signal:
        await safe_edit_message(query, f"{emj('warning', '⚠️')} No pending signal", reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
        return

    signal_text = f"""
📊 New Signal from the Bot

📈 Currency: {signal['currency']}
📉 Direction: {signal['direction']}
💰 Entry Price: {signal['price']}
⏰ Expiry: {signal['expiry']}

🕐 Signal Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{emj('warning', '⚠️')} Trade responsibly - Signals are advisory only
"""
    try:
        await context.bot.send_message(chat_id=SIGNALS_CHANNEL_ID, text=signal_text, parse_mode=ParseMode.HTML)
        success_msg = f"{emj('check', '✅')} Signal sent to channel successfully!"
    except Exception as e:
        success_msg = f"{emj('cross', '❌')} Send failed: {str(e)}"

    context.user_data.pop("pending_signal", None)
    await safe_edit_message(query, f"{success_msg}\n\nBack to control panel:", reply_markup=get_control_keyboard(is_admin=True), parse_mode=ParseMode.HTML)

async def admin_broadcast(query, context):
    if not is_admin(query.from_user.id):
        return
    text = f"""
{emj('speaker', '📣')} Broadcast Message to All Users

Send the message you want to broadcast:
{emj('warning', '⚠️')} Send /cancel to cancel

Total Users: {get_all_users_count()}
"""
    await safe_edit_message(query, text, parse_mode=ParseMode.HTML)
    return WAITING_BROADCAST

async def receive_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    message = update.message.text
    users = get_all_users()
    sent = 0
    failed = 0
    status_msg = await update.message.reply_text(f"{emj('rocket', '🚀')} Sending... (0/{len(users)})")
    for user in users:
        try:
            await context.bot.send_message(chat_id=user["user_id"], text=f"{emj('speaker', '📣')} Message from Admin:\n\n{message}", parse_mode=ParseMode.HTML)
            sent += 1
        except Exception:
            failed += 1

    await status_msg.edit_text(f"{emj('check', '✅')} Broadcast completed!\n\n📤 Sent: {sent}\n{emj('cross', '❌')} Failed: {failed}", reply_markup=get_control_keyboard(is_admin=True), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

async def admin_stats(query):
    if not is_admin(query.from_user.id):
        return
    users_count = get_all_users_count()
    signals_stats = get_signals_stats()
    users = get_all_users()
    premium_count = sum(1 for u in users if u.get("plan") != "free")
    total_referrals = sum(u.get("referral_count", 0) for u in users)
    wins = signals_stats.get("win", 0)
    losses = signals_stats.get("loss", 0)
    total_signals = wins + losses
    win_rate = (wins / total_signals * 100) if total_signals > 0 else 0

    text = f"""
{emj('stats', '📊')} Bot Statistics

👥 Users:
• Total Users: {users_count}
• VIP Subscribers: {premium_count}
• Total Referrals: {total_referrals}

{emj('chart', '📈')} Signals:
• Winning signals: {wins}
• Losing signals: {losses}
• Win rate: {win_rate:.1f}%

📅 Last Updates:
• Last update date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    await safe_edit_message(query, text, reply_markup=get_control_keyboard(is_admin=True), parse_mode=ParseMode.HTML)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("admin_creating_signal", None)
    context.user_data.pop("admin_broadcasting", None)
    context.user_data.pop("pending_signal", None)
    await update.message.reply_text(f"{emj('cross', '❌')} Operation cancelled", reply_markup=get_main_menu_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

async def track_channel_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if result.new_chat_member.status in ['member', 'administrator']:
        user_id = result.from_user.id
        update_channel_join(user_id, joined=True)
        logging.info(f"User {user_id} joined the channel")

# ============================================================
# 6) MAIN ENTRY POINT
# ============================================================
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, handlers=[logging.FileHandler('bot.log', encoding='utf-8'), logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

async def post_init(application):
    me = await application.bot.get_me()
    logger.info("=" * 50)
    logger.info(f"{emj('robot', '🤖')} Bot Info:\n   📛 Name: {me.first_name}\n   🔗 Username: @{me.username}\n   🆔 ID: {me.id}")
    global BOT_USERNAME
    if BOT_USERNAME in ["your_bot_username", "", None]:
        BOT_USERNAME = me.username
    logger.info("=" * 50)

def main():
    if not validate_config():
        logger.error("❌ Configuration incomplete! Edit BOT_TOKEN in this file.")
        sys.exit(1)

    logger.info(f"{emj('stats', '📊')} Initializing database...")
    init_db()
    logger.info(f"{emj('check', '✅')} Database initialized successfully")

    logger.info(f"{emj('robot', '🤖')} Starting the bot...")
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("cancel", cancel))

    signal_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_new_signal, pattern="^admin_new_signal$")],
        states={WAITING_SIGNAL_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_signal_input)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(signal_conversation)

    broadcast_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_broadcast, pattern="^admin_broadcast$")],
        states={WAITING_BROADCAST: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_broadcast)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(broadcast_conversation)

    session_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_new_session, pattern="^new_session$")],
        states={
            WAITING_SESSION_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_session_start)],
            WAITING_SESSION_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_session_end)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(session_conversation)

    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(ChatMemberHandler(track_channel_join, ChatMemberHandler.CHAT_MEMBER))

    logger.info("=" * 50)
    logger.info(f"{emj('rocket', '🚀')} Advanced Trading Signals Bot is running!")
    logger.info(f"{emj('sparkles', '✨')} All emojis are premium custom emojis!")
    logger.info("=" * 50)
    logger.info("⏹️  Press Ctrl+C to stop the bot")
    logger.info("=" * 50)

    application.run_polling(allowed_updates=["message", "callback_query", "chat_member"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        sys.exit(1)
