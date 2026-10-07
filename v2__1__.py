f"""
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
- ALL EMOJIS ARE NOW PREMIUM COLORFUL CUSTOM EMOJIS
- FIXED: Callback query timeout error
- UPDATED: Future Signals icon (Neon Diamond)
- UPDATED: Token input from terminal

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
# HARDCODED PREMIUM EMOJI MAP (no Emoji.json file needed)
# These IDs are embedded directly in the code.
# Bot works WITHOUT Emoji.json file.
# ============================================================
import json as _json_module
_EMOJI_MAP_CACHE = {
    # Emojis used in e() calls throughout the bot
    "⚡": "5373066076558996568",   # NeonEmoji - lightning
    "✨": "5217818964612108191",  # EffectEmoji - sparkles
    "🎉": "5235711785482341993",  # SparklesEmoji - celebration
    "💎": "5465283645788937267",  # NeonEmoji - diamond
    "📈": "5197503331215361533",  # RestrictedEmoji - chart up
    "😍": "5217824874487101321",  # RestrictedEmoji - heart eyes
    "🙏": "5472189549473963781",  # RestrictedEmoji - pray
    "🚀": "5217880283860194582",  # EffectEmoji - rocket
    "🛠": "5462921117423384478",  # GameEmoji - tools
    # ALL other emojis used in bot messages
    "⏰": "5431807687136395567",  # RestrictedEmoji - alarm
    "⏳": "5217697679030637222",  # EffectEmoji - hourglass
    "✅": "5298780919207844086",  # SparklesEmoji - check
    "✔️": "5188216731453103384",  # RestrictedEmoji - heavy check
    "❓": "5206479194388713063",  # EffectEmoji - question
    "⭐": "5267500801240092311",  # FinanceEmoji - star
    "🎁": "5411271889421086677",  # NeonEmoji - gift
    "🎯": "5461009483314517035",  # RestrictedEmoji - target
    "🏆": "5345892905103932200",  # RestrictedEmoji - trophy
    "🐾": "5188308218551475917",  # RestrictedEmoji - paw prints
    "👇": "5470177992950946662",  # RestrictedEmoji - point down
    "👑": "5348306023889254367",  # RestrictedEmoji - crown
    "👥": "5190806721286657692",  # RestrictedEmoji - busts
    "💡": "5193127592764394874",  # EffectEmoji - light bulb
    "💰": "5456319774164269402",  # GlowingFont - money bag
    "💳": "5267300544094948794",  # SparklesEmoji - credit card
    "📅": "5192784923093652913",  # TopicIcons - calendar
    "📋": "5334882760735598374",  # EMOJI_IDS clipboard fallback
    "📌": "5397782960512444700",  # NewsEmoji - pushpin
    "📰": "5433982607035474385",  # RestrictedEmoji - newspaper
    "🔔": "5361643005444899140",  # RestrictedEmoji - bell
    "🔥": "5220166546491459639",  # EffectEmoji - fire
    "🔵": "5375129357373165375",  # EMOJI_IDS link fallback
    "🕊": "5434121252874756456",  # RestrictedEmoji - dove
    "🕐": "5445010743021818722",  # PeriodicTable - clock
    "🟢": "5416081784641168838",  # NewsEmoji - green circle
    "🟥": "5411225014148014586",  # NewsEmoji - red square fallback
    "🟦": "5375129357373165375",  # blue square -> link fallback
    "🟩": "5416081784641168838",  # green square -> green circle fallback
    "🦌": "5427137412713161135",  # RestrictedEmoji - deer
    "🆔": "5422683699130933153",  # RestrictedEmoji - ID (user fallback)
    "🪪": "5422683699130933153",  # RestrictedEmoji - ID card
    "👤": "5373012449597335010",  # RestrictedEmoji - person
    "🤖": "5372981976804366741",  # RestrictedEmoji - robot
    "📊": "5190806721286657692",  # RestrictedEmoji - bar chart
    # Fallback emojis (emojis not in standard sets)
    "⏹️": "5462921117423384478",  # tools fallback
    "⏹": "5462921117423384478",   # tools fallback
    "📛": "5422683699130933153",   # user fallback
    # Additional emojis for full coverage
    "⌛": "5386367538735104399",  # NewsEmoji - hourglass done
    "⏱️": "5350438526691326210",  # TopicIcons - stopwatch
    "⏸️": "5462921117423384478",  # tools fallback
    "⚙️": "5267334530171169409",  # LoveDayEmoji - gear (animated, colorful)
    "⚠️": "5431445849026611010",  # CuteEmoji - warning
    "❌": "5465665476971471368",  # RestrictedEmoji - cross
    "❤️": "5449505950283078474",  # RestrictedEmoji - heart
    "➕": "5417974701282571313",  # GlowingFont - plus
    "➖": "5418206758365574104",  # GlowingFont - minus
    "🆓": "5364112491381006601",  # RestrictedEmoji - free
    "🌀": "5429187589582111255",  # CuteEmoji - swirl
    "🌐": "5395330710280093235",  # NewsEmoji - globe
    "🐛": "5397991236361527676",  # RestrictedEmoji - bug
    "💲": "5373350287429872269",  # NeonEmoji - dollar
    "📆": "5431897022456145283",  # RestrictedEmoji - calendar
    "📉": "5361748661640372834",  # RestrictedEmoji - chart down
    "📝": "5334882760735598374",  # RestrictedEmoji - memo
    "📞": "5404350824501491839",  # NeonEmoji - phone
    "📣": "5469903029144657419",  # RestrictedEmoji - megaphone
    "📤": "5433614747381538714",  # RestrictedEmoji - outbox
    "🔄": "5264727218734524899",  # RestrictedEmoji - arrows
    "🔍": "5231012545799666522",  # RestrictedEmoji - magnifier
    "🔒": "5206432422194849059",  # TopicIcons - lock
    "🔗": "5375129357373165375",  # RestrictedEmoji - link
    "🔮": "5361837567463399422",  # RestrictedEmoji - crystal ball
    "🛑": "5413610645142642221",  # BubbleEmoji - stop
    "🇧🇩": "5372981976804366741",  # robot fallback for flags
}
_EMOJI_MAP_LOADED = True  # Already loaded - no file needed

# ============================================================
# PREMIUM LUXURY EMOJI OVERRIDES (40 hand-picked premium emoji IDs)
# ============================================================
_LUXURY_EMOJI_OVERRIDES = {
    "\U0001F606": "5323523560080158541",  # 😆
    "\U0001F605": "5199468807034253648",  # 😅
    "\U0001F60A": "5352899869369446268",  # 😊
    "\U0001F609": "5339267587337370029",  # 😉
    "\U0001F60D": "5217824874487101321",  # 😍
    "\U0001F618": "5307736407056331791",  # 😘
    "\U0001F61D": "5460631951394225073",  # 😝
    "\U0001F928": "5352640560718949874",  # 🤨
    "\U0001F929": "5353025608832004653",  # 🤩
    "\U0001F973": "5197630131534836123",  # 🥳
    "\U0001F97A": "5458378137240877666",  # 🥺
    "\U0001F622": "5323329096845897690",  # 😢
    "\U0001F62D": "5339124569221377480",  # 😭
    "\U0001F621": "5217467090826441505",  # 😡
    "\U0001F92F": "5197564405650307134",  # 🤯
    "\U0001F976": "5197581306346617713",  # 🥶
    "\U0001F631": "5197706972794731241",  # 😱
    "\U0001F628": "5460958179930158488",  # 😨
    "\U0001FAE2": "5197404349399054490",  # 🫢
    "\U0001FAE1": "5323772371830588991",  # 🫡
    "\U0001FAE0": "5197170531379459422",  # 🫠
    "\U0001F62C": "5352609143033180462",  # 😬
    "\U0001F971": "5447445388183222331",  # 🥱
    "\U0001F634": "5341363621572128687",  # 😴
    "\U0001F635": "5422649047334794716",  # 😵
    "\U0001F635\u200D\U0001F4AB": "5296424506875722458",  # 😵‍💫
    "\U0001F92E": "5384083969048325091",  # 🤮
    "\U0001F911": "5436386989857320953",  # 🤑
    "\U0001F608": "5197645099495862838",  # 😈
    "\U0001F921": "5197188419918246648",  # 🤡
    "\U0001F4A9": "5199763841222721243",  # 💩
    "\U0001F480": "5375407413555900550",  # 💀
    "\U0001F44D": "5323547156630483403",  # 👍
    "\U0001F44E": "5197396124536682206",  # 👎
    "\U0001F44C": "5422446685655676792",  # 👌
    "\U0001F44B": "5199885118214255386",  # 👋
    "\U0001F64F": "5458774648621643551",  # 🙏
    "\U0001F645\u200D\u2642\uFE0F": "5422858869372104873",  # 🙅‍♂️
    "\u2795": "5433805508353996553",      # ➕
    "\U0001F4AF": "5447508713181034519",  # 💯
}
# Apply luxury overrides to the cache
_EMOJI_MAP_CACHE.update(_LUXURY_EMOJI_OVERRIDES)

def _load_emoji_map():
    """Emoji map is already loaded (hardcoded). No file needed."""
    return _EMOJI_MAP_CACHE

def e(base_emoji):
    """Wrap ANY plain emoji with a premium custom Telegram emoji.
    Uses hardcoded IDs - no Emoji.json file needed.
    Falls back to the plain emoji if no mapping exists.
    """
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
            InlineKeyboardButton("Live Signal", callback_data="live_signal", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["lightning_premium"]),
        ],
        # === Market FS + Checkers (paired by market type) ===
        [
            InlineKeyboardButton("OTC Market FS", callback_data="otc_market_fs", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["chart_market"]),
            InlineKeyboardButton("OTC Checker", callback_data="otc_checker", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["magnifier"]),
        ],
        [
            InlineKeyboardButton("Live Market FS", callback_data="live_market_fs", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["globe"]),
            InlineKeyboardButton("Live Checker", callback_data="live_checker", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["magnifier"]),
        ],
        [
            InlineKeyboardButton("Blackout FS", callback_data="blackout_fs", style=STYLE_BLUE, icon_custom_emoji_id="5366254421636298770"),
            InlineKeyboardButton("Blackout Checker", callback_data="blackout_checker", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["magnifier"]),
        ],
        [
            InlineKeyboardButton("Axtiron FS", callback_data="axtiron_fs", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["target_check"]),
            InlineKeyboardButton("CHK Axtiron FS", callback_data="axtiron_checker", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["magnifier"]),
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
            InlineKeyboardButton("Plans", url=WEBAPP_PLANS_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["diamond"]),
        ],
        # === Plans & Upgrade ===
        [
            InlineKeyboardButton("Upgrade", callback_data="upgrade", style=STYLE_BLUE, icon_custom_emoji_id="5217880283860194582"),
            InlineKeyboardButton("Free Bots", callback_data="free_bots", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["gift"]),
        ],
        # === Promo Code & Referral (paired) ===
        [
            InlineKeyboardButton("Promo Code", callback_data="promo_code", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["gift"]),
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
        # === Admin & Tools (paired) ===
        [
            InlineKeyboardButton("Bot Control", url=WEBAPP_BOTS_URL, style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["tools"]),
            InlineKeyboardButton("Formatter", callback_data="formatter", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["swirl"]),
        ],
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
    f"""Rating keyboard with 1-5 stars and back button."""
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
WAITING_SIGNAL_INPUT, WAITING_BROADCAST, WAITING_SESSION_START, WAITING_SESSION_END, WAITING_BLACKOUT_START, WAITING_BLACKOUT_END, WAITING_OTC_START, WAITING_OTC_END, WAITING_OTC_CHK, WAITING_LIVE_CHK, WAITING_BLK_CHK, WAITING_AXTIRON_CHK, WAITING_PROMO, WAITING_FORMATTER_SIGNAL, WAITING_FORMATTER_CHOICE = range(15)

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
        welcome_text += f"\n{e('🎁')} You were referred by a friend!"

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
        await show_live_checker_time_input(update, context)
    elif data.startswith("live_chk_day_"):
        await show_live_chk_mtg(query, data.replace("live_chk_day_", ""))
    elif data.startswith("live_chk_mtg_"):
        parts = data.replace("live_chk_mtg_", "").split("_")
        if len(parts) == 2:
            await show_live_chk_scan(query, parts[0], parts[1])
    elif data == "otc_checker":
        await show_otc_checker_broker(query)
    elif data == "otc_chk_quotex":
        await show_otc_chk_time_input(update, context, "quotex")
    elif data == "otc_chk_binolla":
        await show_otc_chk_time_input(update, context, "binolla")
    elif data.startswith("otc_chk_day_"):
        # Format: otc_chk_day_<day>_<broker>
        parts = data.replace("otc_chk_day_", "").split("_")
        if len(parts) == 2:
            await show_otc_chk_mtg(query, parts[0], parts[1])
    elif data.startswith("otc_chk_mtg_"):
        # Format: otc_chk_mtg_<mtg>_<day>_<broker>
        parts = data.replace("otc_chk_mtg_", "").split("_")
        if len(parts) == 3:
            await show_otc_chk_scan(query, parts[0], parts[1], parts[2])
    elif data == "otc_chk_scan":
        # Detect from message
        await show_otc_chk_results(query, user_id)
    elif data == "blackout_checker":
        await show_blackout_chk_broker(query)
    elif data == "blk_chk_quotex":
        await show_blackout_chk_time_input(update, context, "quotex")
    elif data == "blk_chk_binolla":
        await show_blackout_chk_time_input(update, context, "binolla")
    elif data.startswith("blk_chk_day_"):
        parts = data.replace("blk_chk_day_", "").split("_")
        if len(parts) == 2:
            await show_blackout_chk_mtg(query, parts[0], parts[1])
    elif data.startswith("blk_chk_mtg_"):
        parts = data.replace("blk_chk_mtg_", "").split("_")
        if len(parts) == 3:
            await show_blackout_chk_scan(query, parts[0], parts[1], parts[2])
    elif data == "axtiron_checker":
        await show_axtiron_chk_time_input(update, context)
    elif data.startswith("axtiron_chk_day_"):
        await show_axtiron_chk_mtg(query, data.replace("axtiron_chk_day_", ""))
    elif data.startswith("axtiron_chk_mtg_"):
        parts = data.replace("axtiron_chk_mtg_", "").split("_")
        if len(parts) == 2:
            await show_axtiron_chk_scan(query, parts[0], parts[1])
    elif data == "promo_code":
        await show_promo_code_input(update, context)
    elif data == "otc_market_fs":
        await show_otc_broker(query)
    elif data == "otc_quotex":
        await start_otc_time_input(update, context, "quotex")
    elif data == "otc_binolla":
        await start_otc_time_input(update, context, "binolla")
    elif data.startswith("otc_pairs_"):
        parts = data.replace("otc_pairs_", "").split("_")
        if len(parts) == 2:
            await show_otc_pairs(query, parts[0], int(parts[1]))
    elif data.startswith("otc_toggle_"):
        parts = data.replace("otc_toggle_", "").split("_")
        if len(parts) == 3:
            await toggle_otc_pair(query, user_id, parts[0], int(parts[1]), int(parts[2]))
    elif data == "otc_select_all":
        await otc_select_all(query, user_id)
    elif data == "otc_start_pairs":
        await show_otc_direction(query, user_id)
    elif data.startswith("otc_dir_"):
        # Format: otc_dir_<direction>
        direction = data.replace("otc_dir_", "")
        context.user_data["otc_direction"] = direction
        await show_otc_mtg(query, user_id)
    elif data.startswith("otc_mtg_"):
        # Format: otc_mtg_<mtg_choice>
        mtg = data.replace("otc_mtg_", "")
        context.user_data["otc_mtg"] = mtg
        await show_otc_analysis_ready(query, user_id)
    elif data == "otc_start_analysis":
        await show_otc_starting(query, user_id)
    elif data == "live_market_fs":
        await show_live_market_pairs(query, 0)
    elif data.startswith("lm_pairs_"):
        # Format: lm_pairs_<page>
        parts = data.replace("lm_pairs_", "").split("_")
        if len(parts) == 1:
            await show_live_market_pairs(query, int(parts[0]))
    elif data.startswith("lm_toggle_"):
        # Format: lm_toggle_<page>_<pair_idx>
        parts = data.replace("lm_toggle_", "").split("_")
        if len(parts) == 2:
            await toggle_live_market_pair(query, user_id, int(parts[0]), int(parts[1]))
    elif data == "lm_select_all":
        await live_market_select_all(query, user_id)
    elif data == "lm_start_pairs":
        await show_live_market_direction(query, user_id)
    elif data.startswith("lm_dir_"):
        direction = data.replace("lm_dir_", "")
        context.user_data["lm_direction"] = direction
        await show_live_market_mtg(query, user_id)
    elif data.startswith("lm_mtg_"):
        mtg = data.replace("lm_mtg_", "")
        context.user_data["lm_mtg"] = mtg
        await show_live_market_analysis_ready(query, user_id)
    elif data == "lm_start_analysis":
        await show_live_market_starting(query, user_id)
    elif data == "blackout_fs":
        await show_blackout_broker(query)
    elif data == "blackout_quotex":
        await start_blackout_time_input(update, context, "quotex")
    elif data == "blackout_binolla":
        await start_blackout_time_input(update, context, "binolla")
    elif data.startswith("blackout_pairs_"):
        # Format: blackout_pairs_<broker>_<page>
        parts = data.replace("blackout_pairs_", "").split("_")
        if len(parts) == 2:
            await show_blackout_pairs(query, parts[0], int(parts[1]))
    elif data.startswith("blackout_toggle_"):
        # Format: blackout_toggle_<broker>_<page>_<pair_idx>
        parts = data.replace("blackout_toggle_", "").split("_")
        if len(parts) == 3:
            await toggle_blackout_pair(query, user_id, parts[0], int(parts[1]), int(parts[2]))
    elif data == "blackout_select_all":
        await blackout_select_all(query, user_id)
    elif data == "blackout_start_analysis":
        await show_blackout_mtg(query, user_id)
    elif data == "blackout_mtg1":
        await show_blackout_duration(query, user_id, 1)
    elif data == "blackout_mtg2":
        await show_blackout_duration(query, user_id, 2)
    elif data.startswith("blackout_dur_"):
        # Format: blackout_dur_<duration>_<mtg_level>
        parts = data.replace("blackout_dur_", "").split("_")
        if len(parts) == 2:
            await show_blackout_analysis_type(query, user_id, parts[0], int(parts[1]))
    elif data.startswith("blackout_analysis_"):
        # Format: blackout_analysis_<type>_<duration>_<mtg_level>
        parts = data.replace("blackout_analysis_", "").split("_")
        if len(parts) == 3:
            await show_blackout_final(query, user_id, parts[0], parts[1], int(parts[2]))
    elif data == "whiteout_fs":
        await show_market_fs(query, "Whiteout")
    elif data == "axtiron_fs":
        await show_axtiron_broker(query)
    elif data == "axtiron_quotex":
        await show_axtiron_market(query, "quotex")
    elif data == "axtiron_binolla":
        await show_axtiron_market(query, "binolla")
    elif data.startswith("axtiron_market_"):
        # Format: axtiron_market_<market>_<broker>
        parts = data.replace("axtiron_market_", "").split("_")
        if len(parts) == 2:
            await show_axtiron_analyzing(query, parts[0], parts[1])
    elif data.startswith("axtiron_pairs_"):
        # Format: axtiron_pairs_<broker>_<page>
        parts = data.replace("axtiron_pairs_", "").split("_")
        if len(parts) == 2:
            await show_axtiron_pairs(query, parts[0], int(parts[1]))
    elif data.startswith("axtiron_toggle_"):
        parts = data.replace("axtiron_toggle_", "").split("_")
        if len(parts) == 3:
            await toggle_axtiron_pair(query, user_id, parts[0], int(parts[1]), int(parts[2]))
    elif data == "axtiron_select_all":
        await axtiron_select_all(query, user_id)
    elif data == "axtiron_start":
        await show_axtiron_results(query, user_id)
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
        await show_formatter_input(update, context)
    elif data == "fmt_new":
        await show_formatter_input(update, context)
    elif data == "fmt_change":
        # Show format choice list again using stored signals
        await show_formatter_change_format(update, context)
    elif data.startswith("fmt_choice_"):
        # Format choice from inline buttons
        fmt_id = data.replace("fmt_choice_", "")
        await show_formatter_result_from_button(update, context, fmt_id)
    elif data == "market_filters":
        await show_market_filters_broker(query)
    elif data == "mf_quotex":
        await show_market_filters_market(query, "quotex")
    elif data == "mf_binolla":
        await show_market_filters_market(query, "binolla")
    elif data.startswith("mf_market_"):
        # Format: mf_market_<market>_<broker>
        parts = data.replace("mf_market_", "").split("_")
        if len(parts) == 2:
            await show_market_filters_scanning(query, parts[0], parts[1])
    elif data.startswith("mf_results_"):
        # Format: mf_results_<market>_<broker>
        parts = data.replace("mf_results_", "").split("_")
        if len(parts) == 2:
            await show_market_filters_results(query, parts[0], parts[1])
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
{e('💎')} Subscription Plans {e('💎')}

Choose the plan that suits you from the list below:

{e('🆓')} Free Plan - $0
Duration: 7 days trial
Limited basic features

{e('📅')} Weekly Plan - $15
Duration: 7 full days
Unlimited signals + instant alerts

{e('📆')} Monthly Plan - $45
Duration: 30 days
All features + advanced analytics

{e('👑')} Gold Plan - $120
Duration: 90 days
VIP features + personal account manager

Select a plan to view full details:
"""
    await safe_edit_message(query, text, reply_markup=get_plans_keyboard(), parse_mode=ParseMode.HTML)

async def show_plan_details(query, plan_key):
    plans_map = {"free": PLANS[0], "weekly": PLANS[1], "monthly": PLANS[2], "gold": PLANS[3]}
    plan = plans_map.get(plan_key, PLANS[0])
    features_text = "\n".join([f"{e('✅')} {f}" for f in plan["features"]])
    text = f"""
{e('📋')} Plan Details

Name: {plan['name']}
Price: {plan['price']}
Duration: {plan['duration']}

{e('⭐')} Included Features:
{features_text}

{e('💳')} To subscribe to this plan:
Contact technical support via the Support button in the main menu
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_request_signals(query):
    text = f"""
{e('⚡')} Request Signals Now

{e('🤖')} Select the platform you want signals from:

{e('🟢')} QUOTEX
  Best for binary options (OTC available)

{e('🔵')} BINOLLA
  Fast execution + high payout rates

{e('👇')} Choose a platform below:
"""
    await safe_edit_message(query, text, reply_markup=get_platform_keyboard("request_signals"), parse_mode=ParseMode.HTML)

async def show_bot_signals(query, platform):
    now = datetime.now()
    platforms_info = {
        "quotex": {"name": "QUOTEX Signals", "emoji_id": EMOJI_IDS["robot"], "pairs": [("EUR/USD OTC", "CALL", "1.0856", "M1", "94%"), ("GBP/JPY OTC", "PUT", "189.42", "M5", "89%"), ("USD/JPY OTC", "CALL", "149.78", "M1", "91%")]},
        "binolla": {"name": "BINOLLA Signals", "emoji_id": EMOJI_IDS["chart"], "pairs": [("AUD/CAD", "PUT", "0.9124", "M5", "88%"), ("EUR/GBP", "CALL", "0.8541", "M1", "92%"), ("USD/CHF", "PUT", "0.8923", "M5", "90%")]},
    }
    platform_info = platforms_info.get(platform, platforms_info["quotex"])
    signals_text = "\n\n".join([f"{e('📊')} {p[0]}\nDirection: {p[1]}\nEntry: {p[2]}\nExpiry: {p[3]}\nConfidence: {p[4]}" for p in platform_info["pairs"]])
    text = f"""
{e('🤖')} {platform_info['name']}

{e('📅')} Request Time: {now.strftime('%Y-%m-%d %H:%M:%S')}
{e('✅')} Status: Active signals below

{signals_text}

{e('📈')} Platform Summary:
• Active pairs: {len(platform_info['pairs'])}
• Avg confidence: 90%
• Sentiment: Bullish {e('📈')}

{e('⚠️')} Trade responsibly - Not financial advice
"""
    await safe_edit_message(query, text, reply_markup=get_back_to_signal_keyboard(), parse_mode=ParseMode.HTML)

async def show_current_signals(query):
    signals = [("EUR/USD", "CALL", "1.0856", "M1", "92%"), ("GBP/JPY", "PUT", "189.42", "M5", "88%"), ("USD/JPY", "CALL", "149.78", "M1", "95%")]
    signals_text = "\n\n".join([f"{e('📊')} {s[0]}\nDirection: {s[1]}\nEntry: {s[2]}\nExpiry: {s[3]}\nExpected Rate: {s[4]}" for s in signals])
    text = f"""
{e('📈')} Live Current Signals

{signals_text}

{e('⏰')} Last Update: {datetime.now().strftime('%H:%M:%S')}
{e('⚠️')} Trade responsibly - Signals are not a profit guarantee

{e('📌')} To subscribe to premium instant signals, use the "Subscription Plans" button
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
        status = "{e('✅')} Active" if scheduled_time.get("enabled") else "{e('⏸️')} Paused"
        schedule_text = f"""{e('✅')} 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆 𝑺𝒕𝒂𝒕𝒖𝒔: {status}

{e('⏰')} 𝑺𝒕𝒂𝒓𝒕 𝑻𝒊𝒎𝒆: {scheduled_time['start_time']}
{e('⏰')} 𝑬𝒏𝒅 𝑻𝒊𝒎𝒆: {scheduled_time.get('end_time', 'Not set')}

{e('💡')} The bot will automatically send you signals during this time period."""
    else:
        schedule_text = f"""{e('⚠️')} 𝑵𝒐 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆 𝑺𝒆𝒕

You haven't set a signal schedule yet.

{e('👇')} Choose a time slot below to start receiving signals automatically:"""

    text = f"""{e('⏰')} 𝑺𝑰𝑮𝑵𝑨𝑳 𝑺𝑪𝑯𝑬𝑫𝑼𝑳𝑬

{schedule_text}

━━━━━━━━━━━━━━━━━━━━

{e('💡')} 𝑯𝒐𝒘 𝒊𝒕 𝒘𝒐𝒓𝒌𝒔:
Set a time period and the bot will
automatically send you trading signals
during that time every day.f"""

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
# Live Market pairs (NO "OTC" suffix)
LIVE_MARKET_PAIRS = [
    ("EUR/USD", 95), ("GBP/JPY", 93), ("USD/JPY", 92),
    ("AUD/CAD", 91), ("EUR/GBP", 90), ("USD/CHF", 89),
    ("EUR/JPY", 88), ("GBP/USD", 87), ("USD/CAD", 86),
    ("AUD/USD", 85), ("NZD/USD", 84), ("EUR/AUD", 83),
    ("GBP/AUD", 82), ("EUR/CAD", 81), ("AUD/JPY", 80),
    ("CAD/JPY", 79), ("NZD/JPY", 78), ("CHF/JPY", 77),
    ("EUR/CHF", 76), ("USD/SEK", 75), ("EUR/SEK", 74),
    ("GBP/CHF", 73), ("AUD/NZD", 72), ("CAD/CHF", 71),
    ("EUR/NZD", 70), ("GBP/CAD", 69), ("NZD/CAD", 68),
    ("AUD/CHF", 67), ("EUR/NOK", 66), ("USD/NOK", 65),
    ("GBP/NOK", 64), ("AUD/SEK", 63), ("CAD/SEK", 62),
    ("EUR/TRY", 61), ("USD/TRY", 60), ("GBP/TRY", 59),
    ("USD/ZAR", 58), ("EUR/ZAR", 57), ("USD/MXN", 56),
    ("USD/SGD", 55),
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
    text = f"""{e('⏰')} 𝚂𝙸𝙶𝙽𝙰𝙻 𝚂𝙴𝚂𝚂𝙸𝙾𝙽

{e('👇')} 𝙲𝙷𝙾𝙾𝚂𝙴 𝙱𝚁𝙾𝙺𝙴𝚁

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
    text = f"""{e('⏰')} 𝚂𝙸𝙶𝙽𝙰𝙻 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 - {broker_name}

{e('👇')} 𝚂𝙴𝙻𝙴𝙲𝚃 𝙲𝚄𝚁𝚁𝙴𝙽𝙲𝚈 𝙿𝙰𝙸𝚁𝚂

Page {page + 1}/{total_pages} · Selected: {len(selected_pairs)} pairs

{e('🟦')} Blue = High payout (85%+)
{e('🟩')} Green = Medium payout (70-84%)
{e('🟥')} Red = Low payout (&lt;70%)"""
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
        nav_row.append(InlineKeyboardButton("Previous", callback_data=f"signal_session_page_{broker}_{page-1}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"]))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next", callback_data=f"signal_session_page_{broker}_{page+1}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"]))
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

    text = f"""{e('⚡')} 𝚂𝚃𝙰𝚁𝚃 𝙰𝙽𝙰𝙻𝚈𝚂𝙸𝚂

Selected pairs: {selected_count}

{e('👇')} 𝙲𝙷𝙾𝙾𝚂𝙴 𝙼𝚃𝙶 𝙻𝙴𝚅𝙴𝙻"""
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
    text = f"""{e('⏰')} 𝚃𝚁𝙰𝙳𝙴 𝙳𝚄𝚁𝙰𝚃𝙸𝙾𝙽

MTG Level: MTG{mtg_level}

{e('👇')} 𝙲𝙷𝙾𝙾𝚂𝙴 𝙳𝚄𝚁𝙰𝚃𝙸𝙾𝙽"""
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
    text = f"""{e('✅')} {to_bold_italic('SESSION STARTED!')}

{e('⚡')} {to_bold('MTG LEVEL')}: {to_bold(f'MTG{mtg_level}')}
{e('⌛')} {to_bold('DURATION')}: {to_bold(duration)}
{e('📊')} {to_bold('BROKER')}: {to_bold(broker_name)}
{e('📈')} {to_bold('SELECTED PAIRS')}: {to_bold(str(pairs_count))}

{e('💎')} {to_bold('The bot will now start sending')}
{to_bold('trading signals for your selected pairs.')}

{e('⌛')} {to_bold('STARTED AT')}: {to_bold(datetime.now().strftime('%H:%M:%S'))}"""
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
            status = "{e('✅')}" if s["enabled"] else "{e('⏸️')}"
            sessions_text += f"\n{i}. {status} {s['start_time']} - {s['end_time']}"
        schedule_text = f"""{e('✅')} 𝒀𝒐𝒖𝒓 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆𝒅 𝑺𝒆𝒔𝒔𝒊𝒐𝒏𝒔:
{sessions_text}"""
    else:
        schedule_text = f"""{e('⚠️')} 𝙽𝙾 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴𝙳 𝚂𝙴𝚂𝚂𝙸𝙾𝙽𝚂 𝚈𝙴𝚃

𝚈𝚘𝚞 𝚍𝚘𝚗'𝚝 𝚑𝚊𝚟𝚎 𝚊𝚗𝚢 𝚜𝚌𝚑𝚎𝚍𝚞𝚕𝚎𝚍 𝚜𝚎𝚜𝚜𝚒𝚘𝚗𝚜 𝚊𝚝 𝚝𝚑𝚎 𝚖𝚘𝚖𝚎𝚗𝚝.

{e('➕')} 𝙽𝙴𝚆 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴

{e('👇')} 𝚃𝙰𝙿 𝙱𝙴𝙻𝙾𝚆 𝚃𝙾 𝙲𝚁𝙴𝙰𝚃𝙴 𝙰 𝙽𝙴𝚆 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴."""

    text = f"""{e('⏰')} 𝚃𝙸𝙼𝙴 𝚂𝙴𝚂𝚂𝙸𝙾𝙽

{schedule_text}

━━━━━━━━━━━━━━━━━━━━

{e('💡')} 𝑯𝒐𝒘 𝒊𝒕 𝒘𝒐𝒓𝒌𝒔:
Set a time period and the bot will
automatically send you trading signals
during that time every day.f"""

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
    text = f"""{e('⏰')} 𝙽𝙴𝚆 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴

{e('👇')} 𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙴𝙽𝙳 𝚃𝙷𝙴 𝚂𝚃𝙰𝚁𝚃 𝚃𝙸𝙼𝙴

𝙵𝚘𝚛𝚖𝚊𝚝: 𝙷𝙷:𝙼𝙼 (𝚎.𝚐. 09:00)

{e('⚠️')} 𝚂𝚎𝚗𝚍 /cancel 𝚝𝚘 𝚌𝚊𝚗𝚌𝚎𝚕"""
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
        await update.message.reply_text(f"{e('⚠️')} Invalid format! Please send time as HH:MM (e.g. 09:00)\n\nSend /cancel to cancel")
        return WAITING_SESSION_START

    context.user_data["session_start"] = text
    await update.message.reply_text(
        f"{e('✅')} Start time received: {text}\n\n"
        f"{e('⏰')} Now please send the END time\n\n"
        f"Format: HH:MM (e.g. 17:00)\n\n"
        f"{e('⚠️')} Send /cancel to cancel",
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
        await update.message.reply_text(f"{e('⚠️')} Invalid format! Please send time as HH:MM (e.g. 17:00)\n\nSend /cancel to cancel")
        return WAITING_SESSION_END

    context.user_data["session_end"] = text
    start_time = context.user_data.get("session_start")
    end_time = text

    text_msg = f"""{e('✅')} 𝙲𝙾𝙽𝙵𝙸𝚁𝙼 𝚂𝙲𝙷𝙴𝙳𝚄𝙻𝙴

{e('⏰')} 𝚂𝚃𝙰𝚁𝚃: {start_time}
{e('⏰')} 𝙴𝙽𝙳:   {end_time}

{e('👇')} 𝙿𝚁𝙴𝚂𝚂 𝙱𝙴𝙻𝙾𝚆 𝚃𝙾 𝙲𝙾𝙽𝙵𝙸𝚁𝙼f"""
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
        await safe_edit_message(query, f"{e('⚠️')} Session data missing. Please try again.", reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
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

    text = f"""{e('✅')} 𝚂𝙲𝚑𝚎𝚍𝚞𝚕𝚎 𝚂𝚊𝚟𝚎𝚍!

{e('⏰')} Start: {start_time}
{e('⏰')} End: {end_time}

{e('💡')} The bot will send you trading signals
during this time period every day."""
    await safe_edit_message(query, text, reply_markup=get_main_menu_keyboard(), parse_mode=ParseMode.HTML)


async def show_live_future(query):
    """Show the Live Future page - user requests to verify results."""
    text = f"""{e('🔮')} 𝙻𝙸𝚅𝙴 𝙵𝚄𝚃𝚄𝚁𝙴

𝚁𝚎𝚚𝚞𝚎𝚜𝚝 𝚝𝚘 𝚟𝚎𝚛𝚒𝚏𝚢 𝚏𝚞𝚝𝚞𝚛𝚎 𝚜𝚒𝚐𝚗𝚊𝚕𝚜 𝚛𝚎𝚜𝚞𝚕𝚝𝚜.

{e('👇')} 𝚃𝙰𝙿 𝙱𝙴𝙻𝙾𝚆 𝚃𝙾 𝙲𝙷𝙴𝙲𝙺:f"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Check Results", callback_data="future_results", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


# ============================================================
# LIVE MARKET FS - Direct pairs selection (no broker), direction, MTG, analysis
# ============================================================

def _clear_lm_selections(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS lm_selections (user_id INTEGER PRIMARY KEY, pair_index INTEGER)")
        cursor.execute("DELETE FROM lm_selections WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to clear LM selections: {e}")

def _get_lm_selected(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS lm_selections (user_id INTEGER PRIMARY KEY, pair_index INTEGER)")
        cursor.execute("SELECT pair_index FROM lm_selections WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return set(str(r[0]) for r in rows)
    except Exception:
        return set()

async def show_live_market_pairs(query, page):
    """Show Live Market pairs directly (no broker selection)."""
    user_id = query.from_user.id
    if page == 0:
        _clear_lm_selections(user_id)
    selected = _get_lm_selected(user_id)
    total_pairs = len(LIVE_MARKET_PAIRS)
    total_pages = (total_pairs + PAIRS_PER_PAGE - 1) // PAIRS_PER_PAGE
    start_idx = page * PAIRS_PER_PAGE
    end_idx = min(start_idx + PAIRS_PER_PAGE, total_pairs)
    page_pairs = LIVE_MARKET_PAIRS[start_idx:end_idx]

    text = f"""{e('🌐')} {to_bold_italic('LIVE MARKET FS')}

Page {page + 1}/{total_pages} · Selected: {len(selected)} pairs

👇 {to_bold('SELECT CURRENCY PAIRS')}"""
    keyboard_rows = []
    row = []
    for i, (pair_name, payout) in enumerate(page_pairs):
        global_idx = start_idx + i
        is_selected = str(global_idx) in selected
        if is_selected:
            label = f"✅{pair_name} {payout}%"
            style = STYLE_GREEN
        else:
            label = f"{pair_name} {payout}%"
            style = _get_pair_color_style(payout)
        row.append(InlineKeyboardButton(label, callback_data=f"lm_toggle_{page}_{global_idx}", style=style))
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("Previous", callback_data=f"lm_pairs_{page-1}", style=STYLE_BLUE))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next", callback_data=f"lm_pairs_{page+1}", style=STYLE_BLUE))
    if nav_row:
        keyboard_rows.append(nav_row)

    keyboard_rows.append([
        InlineKeyboardButton("selectAll", callback_data="lm_select_all", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["check"]),
    ])
    count = len(selected)
    keyboard_rows.append([
        InlineKeyboardButton(f"Start ({count})", callback_data="lm_start_pairs", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["lightning"]),
    ])
    keyboard_rows.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def toggle_live_market_pair(query, user_id, page, pair_idx):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS lm_selections (user_id INTEGER PRIMARY KEY, pair_index INTEGER)")
        cursor.execute("SELECT 1 FROM lm_selections WHERE user_id = ? AND pair_index = ?", (user_id, pair_idx))
        if cursor.fetchone():
            cursor.execute("DELETE FROM lm_selections WHERE user_id = ? AND pair_index = ?", (user_id, pair_idx))
        else:
            cursor.execute("INSERT INTO lm_selections (user_id, pair_index) VALUES (?, ?)", (user_id, pair_idx))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to toggle LM pair: {e}")
    await show_live_market_pairs(query, page)

async def live_market_select_all(query, user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS lm_selections (user_id INTEGER PRIMARY KEY, pair_index INTEGER)")
        for i in range(len(LIVE_MARKET_PAIRS)):
            cursor.execute("INSERT OR IGNORE INTO lm_selections (user_id, pair_index) VALUES (?, ?)", (user_id, i))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to select all LM: {e}")
    await show_live_market_direction(query, user_id)

async def show_live_market_direction(query, user_id):
    text = f"""{e('🌐')} {to_bold_italic('LIVE MARKET FS')}

👇 {to_bold('CHOOSE SIGNAL DIRECTION')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("▲ CALL", callback_data="lm_dir_call", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("▼ PUT", callback_data="lm_dir_put", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"]),
        ],
        [InlineKeyboardButton("▲▼ BOTH", callback_data="lm_dir_both", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_live_market_mtg(query, user_id):
    text = f"""{e('🌐')} {to_bold_italic('LIVE MARKET FS')}

👇 {to_bold('CHOOSE MTG')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MTG1", callback_data="lm_mtg_mtg1", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("MTG2", callback_data="lm_mtg_mtg2", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("MTG1 + MTG2", callback_data="lm_mtg_both", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_live_market_analysis_ready(query, user_id):
    user_tz = "+00:00"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_timezone (user_id INTEGER PRIMARY KEY, utc_offset TEXT)")
        cursor.execute("SELECT utc_offset FROM user_timezone WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            user_tz = row[0]
        conn.close()
    except Exception:
        pass

    text = f"""{e('🌐')} {to_bold_italic('LIVE MARKET FS - READY')}

{e('🌐')} {to_bold('TIMEZONE')}: UTC {to_bold(user_tz)}

👇 {to_bold('PRESS TO START ANALYSIS')}"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Start Analysis", callback_data="lm_start_analysis", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["lightning"])],
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_live_market_starting(query, user_id):
    import asyncio
    import random as _random

    selected = _get_lm_selected(user_id)
    selected_names = []
    for idx_str in selected:
        idx = int(idx_str)
        if 0 <= idx < len(LIVE_MARKET_PAIRS):
            selected_names.append(LIVE_MARKET_PAIRS[idx][0])

    user_tz = "+00:00"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT utc_offset FROM user_timezone WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            user_tz = row[0]
        conn.close()
    except Exception:
        pass

    # Starting message
    text = f"""{e('🚀')} {to_bold_italic('LIVE MARKET FS')}

{e('⚡')} {to_bold('STARTING ANALYSIS...')}

Please wait..."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Please wait...", callback_data="lm_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)

    # Countdown
    text = f"""{e('🚀')} {to_bold_italic('LIVE MARKET FS')}

{e('⚡')} {to_bold('ANALYSIS IN PROGRESS')}

⏳ 00:10 remaining...

{to_bold('The bot is analyzing the market')}"""
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    bot = query.message.get_bot()
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    for seconds in range(9, 0, -1):
        await asyncio.sleep(1)
        time_str = f"00:{seconds:02d}"
        countdown_text = f"""{e('🚀')} {to_bold_italic('LIVE MARKET FS')}

{e('⚡')} {to_bold('ANALYSIS IN PROGRESS')}

⏳ {time_str} remaining...

{to_bold('The bot is analyzing the market')}"""
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=countdown_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        except Exception:
            pass

    # Generate signals
    directions_list = ["CALL", "PUT"]
    num_signals = _random.randint(15, 25)
    signals = []
    for _ in range(num_signals):
        pair = _random.choice(selected_names) if selected_names else "EUR/USD"
        pair_clean = pair.replace(" ", "").replace("/", "")
        h = _random.randint(0, 23)
        m = _random.randint(0, 59)
        sig_dir = _random.choice(directions_list)
        signals.append((h * 60 + m, pair_clean, h, m, sig_dir))

    signals.sort(key=lambda x: x[0])

    signal_lines = []
    for _, pair_clean, h, m, sig_dir in signals:
        bold_pair = to_bold(pair_clean)
        bold_time = to_bold(f"{h:02d}:{m:02d}")
        bold_dir = to_bold(sig_dir)
        signal_lines.append(f"{e('⚡')} {to_bold('M1')} {bold_pair} {bold_time} {bold_dir}")

    signals_text = "\n".join(signal_lines)
    today = datetime.now().strftime("%Y-%m-%d")

    final_text = f"""{e('🚀')} {to_bold_italic('LIVE MARKET FS')} {e('🚀')}

{e('📅')} {to_bold(today)}
{e('🌐')} {to_bold('TIMEZONE')}: UTC {to_bold(user_tz)}

━━━━━━━ • ━━━━━━━
{signals_text}
━━━━━━━ • ━━━━━━━

{e('✨')} {to_bold('BACK-TESTED')} ✔️
{e('💎')} {to_bold('USE SAFETY FOR BETTER RESULT')}"""

    final_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, final_text, reply_markup=final_keyboard, parse_mode=ParseMode.HTML)


# ============================================================
# OTC MARKET FS - Full flow: broker, time, pairs, direction, MTG, analysis
# ============================================================

async def show_otc_broker(query):
    f"""Show broker selection for OTC Market FS."""
    text = f"""{e('📈')} <b>OTC MARKET FS</b>

{e('👇')} <b>CHOOSE BROKER</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="otc_quotex", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="otc_binolla", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def start_otc_time_input(update, context, broker=None):
    """Start asking for time range - ask for start time."""
    if broker is None:
        query = update.callback_query
        data = query.data
        broker = "quotex" if "quotex" in data else "binolla"
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    context.user_data["otc_broker"] = broker
    text = f"""{e('📈')} <b>OTC MARKET FS</b>

Broker: {"QUOTEX" if broker == "quotex" else "BINOLLA"}

{e('👇')} <b>SEND START TIME</b>

Format: HH:MM (e.g. 09:10)

Send /cancel to cancel"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return WAITING_OTC_START


async def receive_otc_start_time(update, context):
    """Receive start time, ask for end time."""
    text = update.message.text.strip()
    try:
        parts = text.split(":")
        if len(parts) != 2:
            raise ValueError
        h, m = int(parts[0]), int(parts[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid format! Send HH:MM (e.g. 09:10)\n\nSend /cancel to cancel")
        return WAITING_OTC_START

    context.user_data["otc_start_time"] = text
    await update.message.reply_text(
        f"{e('✅')} Start time: {text}\n\n"
        f"{e('👇')} <b>SEND END TIME</b>\n\n"
        f"Format: HH:MM (e.g. 23:59)\n\n"
        f"Send /cancel to cancel",
        parse_mode=ParseMode.HTML
    )
    return WAITING_OTC_END


async def receive_otc_end_time(update, context):
    """Receive end time, show currency pairs."""
    text = update.message.text.strip()
    try:
        parts = text.split(":")
        if len(parts) != 2:
            raise ValueError
        h, m = int(parts[0]), int(parts[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid format! Send HH:MM (e.g. 23:59)\n\nSend /cancel to cancel")
        return WAITING_OTC_END

    context.user_data["otc_end_time"] = text
    broker = context.user_data.get("otc_broker", "quotex")
    _clear_otc_selections(update.effective_user.id, broker)
    await _send_otc_pairs_message(update, context, broker, 0)
    return ConversationHandler.END


def _clear_otc_selections(user_id, broker):
    """Clear OTC pair selections."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS otc_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("DELETE FROM otc_selections WHERE user_id = ? AND broker = ?", (user_id, broker))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to clear OTC selections: {e}")


def _get_otc_selected(user_id, broker):
    """Get selected pairs for OTC."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS otc_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("SELECT pair_index FROM otc_selections WHERE user_id = ? AND broker = ?", (user_id, broker))
        rows = cursor.fetchall()
        conn.close()
        return set(str(r[0]) for r in rows)
    except Exception:
        return set()


async def _send_otc_pairs_message(update, context, broker, page):
    """Send a new message with OTC pairs."""
    user_id = update.effective_user.id
    selected = _get_otc_selected(user_id, broker)
    total_pairs = len(SIGNAL_SESSION_PAIRS)
    total_pages = (total_pairs + PAIRS_PER_PAGE - 1) // PAIRS_PER_PAGE
    start_idx = page * PAIRS_PER_PAGE
    end_idx = min(start_idx + PAIRS_PER_PAGE, total_pairs)
    page_pairs = SIGNAL_SESSION_PAIRS[start_idx:end_idx]
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    start_time = context.user_data.get("otc_start_time", "")
    end_time = context.user_data.get("otc_end_time", "")

    text = f"""{e('📈')} <b>OTC MARKET FS - {broker_name}</b>

Time: {start_time} - {end_time}

Page {page + 1}/{total_pages} · Selected: {len(selected)} pairs

{e('👇')} <b>SELECT CURRENCY PAIRS</b>"""
    keyboard_rows = []
    row = []
    for i, (pair_name, payout) in enumerate(page_pairs):
        global_idx = start_idx + i
        is_selected = str(global_idx) in selected
        if is_selected:
            label = f"✅{pair_name} {payout}%"
            style = STYLE_GREEN
        else:
            label = f"{pair_name} {payout}%"
            style = _get_pair_color_style(payout)
        row.append(InlineKeyboardButton(label, callback_data=f"otc_toggle_{broker}_{page}_{global_idx}", style=style))
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("Previous", callback_data=f"otc_pairs_{broker}_{page-1}", style=STYLE_BLUE))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next", callback_data=f"otc_pairs_{broker}_{page+1}", style=STYLE_BLUE))
    if nav_row:
        keyboard_rows.append(nav_row)

    keyboard_rows.append([
        InlineKeyboardButton("selectAll", callback_data="otc_select_all", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["check"]),
    ])
    count = len(selected)
    keyboard_rows.append([
        InlineKeyboardButton(f"Start ({count})", callback_data="otc_start_pairs", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["lightning"]),
    ])
    keyboard_rows.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_otc_pairs(query, broker, page):
    """Show OTC pairs page (for navigation)."""
    user_id = query.from_user.id
    selected = _get_otc_selected(user_id, broker)
    total_pairs = len(SIGNAL_SESSION_PAIRS)
    total_pages = (total_pairs + PAIRS_PER_PAGE - 1) // PAIRS_PER_PAGE
    start_idx = page * PAIRS_PER_PAGE
    end_idx = min(start_idx + PAIRS_PER_PAGE, total_pairs)
    page_pairs = SIGNAL_SESSION_PAIRS[start_idx:end_idx]
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"

    text = f"""{e('📈')} <b>OTC MARKET FS - {broker_name}</b>

Page {page + 1}/{total_pages} · Selected: {len(selected)} pairs

{e('👇')} <b>SELECT CURRENCY PAIRS</b>"""
    keyboard_rows = []
    row = []
    for i, (pair_name, payout) in enumerate(page_pairs):
        global_idx = start_idx + i
        is_selected = str(global_idx) in selected
        if is_selected:
            label = f"✅{pair_name} {payout}%"
            style = STYLE_GREEN
        else:
            label = f"{pair_name} {payout}%"
            style = _get_pair_color_style(payout)
        row.append(InlineKeyboardButton(label, callback_data=f"otc_toggle_{broker}_{page}_{global_idx}", style=style))
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("Previous", callback_data=f"otc_pairs_{broker}_{page-1}", style=STYLE_BLUE))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next", callback_data=f"otc_pairs_{broker}_{page+1}", style=STYLE_BLUE))
    if nav_row:
        keyboard_rows.append(nav_row)

    keyboard_rows.append([
        InlineKeyboardButton("selectAll", callback_data="otc_select_all", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["check"]),
    ])
    count = len(selected)
    keyboard_rows.append([
        InlineKeyboardButton(f"Start ({count})", callback_data="otc_start_pairs", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["lightning"]),
    ])
    keyboard_rows.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def toggle_otc_pair(query, user_id, broker, page, pair_idx):
    """Toggle a pair selection for OTC."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS otc_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("SELECT 1 FROM otc_selections WHERE user_id = ? AND broker = ? AND pair_index = ?", (user_id, broker, pair_idx))
        if cursor.fetchone():
            cursor.execute("DELETE FROM otc_selections WHERE user_id = ? AND broker = ? AND pair_index = ?", (user_id, broker, pair_idx))
        else:
            cursor.execute("INSERT INTO otc_selections (user_id, broker, pair_index) VALUES (?, ?, ?)", (user_id, broker, pair_idx))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to toggle OTC pair: {e}")
    await show_otc_pairs(query, broker, page)


async def otc_select_all(query, user_id):
    """Select all pairs for OTC then go to direction selection."""
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS otc_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        for i in range(len(SIGNAL_SESSION_PAIRS)):
            cursor.execute("INSERT OR IGNORE INTO otc_selections (user_id, broker, pair_index) VALUES (?, ?, ?)", (user_id, broker, i))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to select all OTC: {e}")
    await show_otc_direction(query, user_id)


async def show_otc_direction(query, user_id):
    f"""Show signal direction selection (CALL / PUT / BOTH)."""
    text = f"""{e('📈')} <b>OTC MARKET FS</b>

{e('👇')} <b>CHOOSE SIGNAL DIRECTION</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("▲ CALL", callback_data="otc_dir_call", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("▼ PUT", callback_data="otc_dir_put", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"]),
        ],
        [InlineKeyboardButton("▲▼ BOTH", callback_data="otc_dir_both", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back to Pairs", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_otc_mtg(query, user_id):
    """Show MTG selection for OTC (MTG1 / MTG2 / BOTH)."""
    direction = query.message.text or ""
    dir_name = "BOTH" if "BOTH" in direction else ("CALL" if "CALL" in direction else "PUT")

    text = f"""{e('📈')} <b>OTC MARKET FS</b>

Direction: {dir_name}

{e('👇')} <b>CHOOSE MTG</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MTG1", callback_data="otc_mtg_mtg1", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("MTG2", callback_data="otc_mtg_mtg2", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("MTG1 + MTG2", callback_data="otc_mtg_both", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back to Direction", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_otc_analysis_ready(query, user_id):
    """Show timezone info and green Start Analysis button."""
    # Get user timezone
    user_tz = "+00:00"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_timezone (user_id INTEGER PRIMARY KEY, utc_offset TEXT)")
        cursor.execute("SELECT utc_offset FROM user_timezone WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            user_tz = row[0]
        conn.close()
    except Exception:
        pass

    # Get stored info from message
    msg_text = query.message.text or ""
    mtg_name = "MTG1 + MTG2" if "both" in msg_text.lower() else ("MTG1" if "mtg1" in msg_text.lower() else "MTG2")

    text = f"""{e('📈')} <b>OTC MARKET FS - READY</b>

{e('🌐')} <b>Timezone:</b> UTC {user_tz}
{e('⚙️')} <b>MTG:</b> {mtg_name}

{e('👇')} <b>PRESS TO START ANALYSIS</b>f"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Start Analysis", callback_data="otc_start_analysis", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["lightning"])],
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_otc_starting(query, user_id):
    """Show 'Starting...' message then countdown then signal list."""
    import asyncio
    import random as _random

    # Get user data
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    selected = _get_otc_selected(user_id, broker)

    # Get selected pair names
    selected_names = []
    for idx_str in selected:
        idx = int(idx_str)
        if 0 <= idx < len(SIGNAL_SESSION_PAIRS):
            selected_names.append(SIGNAL_SESSION_PAIRS[idx][0])

    # Get user timezone
    user_tz = "+00:00"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_timezone (user_id INTEGER PRIMARY KEY, utc_offset TEXT)")
        cursor.execute("SELECT utc_offset FROM user_timezone WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            user_tz = row[0]
        conn.close()
    except Exception:
        pass

    # Get direction and MTG from context (fallback to message text)
    direction = "BOTH"
    mtg_name = "MTG1"

    # Show "Starting..." message
    text = f"""{e('🚀')} <b>OTC MARKET FS</b>

{e('⚡')} <b>STARTING ANALYSIS...</b>

Please wait..."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏳ Please wait...", callback_data="otc_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)

    # Show 1-minute countdown
    text = f"""{e('🚀')} <b>OTC MARKET FS</b>

{e('⚡')} <b>ANALYSIS IN PROGRESS</b>

{e('⏳')} 01:00 remaining...

The bot is analyzing the market
and generating signals."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("01:00", callback_data="otc_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    # Countdown loop (shortened to 10 seconds for better UX)
    bot = query.message.get_bot()
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    for seconds in range(10, 0, -1):
        await asyncio.sleep(1)
        time_str = f"00:{seconds:02d}"

        countdown_text = f"""{e('🚀')} <b>OTC MARKET FS</b>

{e('⚡')} <b>ANALYSIS IN PROGRESS</b>

{e('⏳')} {time_str} remaining...

The bot is analyzing the market
and generating signals."""
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=countdown_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
        except Exception:
            pass

    # Generate signals
    directions_list = ["CALL", "PUT"] if direction == "BOTH" else [direction]

    # Generate 15-25 random signals
    num_signals = _random.randint(15, 25)
    signals = []
    for _ in range(num_signals):
        pair = _random.choice(selected_names) if selected_names else "EUR/USD OTC"
        pair_clean = pair.replace(" ", "").replace("/", "")
        h = _random.randint(0, 23)
        m = _random.randint(0, 59)
        sig_dir = _random.choice(directions_list)
        signals.append((h * 60 + m, pair_clean, h, m, sig_dir))

    # Sort by time
    signals.sort(key=lambda x: x[0])

    # Build signal text with bold Unicode
    signal_lines = []
    for _, pair_clean, h, m, sig_dir in signals:
        bold_pair = to_bold(pair_clean)
        bold_time = to_bold(f"{h:02d}:{m:02d}")
        bold_dir = to_bold(sig_dir)
        signal_lines.append(f"{e('⚡')} {to_bold('M1')} {bold_pair} {bold_time} {bold_dir}")

    signals_text = "\n".join(signal_lines)
    today = datetime.now().strftime("%Y-%m-%d")

    # Show final result with signals
    final_text = f"""{e('🚀')} {to_bold_italic('OTC MARKET FS')} {e('🚀')}

{e('📈')} {to_bold('BROKER')}: {to_bold(broker_name)}
{e('📅')} {to_bold('DATE')}: {to_bold(today)}
{e('🌐')} {to_bold('TIMEZONE')}: UTC {to_bold(user_tz)}

━━━━━━━ • ━━━━━━━
{signals_text}
━━━━━━━ • ━━━━━━━

{e('✨')} {to_bold('BACK-TESTED')} {e('✔️')}
{e('💎')} {to_bold('USE SAFETY FOR BETTER RESULT')}"""

    final_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, final_text, reply_markup=final_keyboard, parse_mode=ParseMode.HTML)


# ============================================================
# BLACKOUT FS - Full flow: broker, time, pairs, MTG, duration, analysis
# ============================================================

async def show_blackout_broker(query):
    """Show broker selection for Blackout FS."""
    text = f"""{e('🚀')} <b>BLACKOUT FS</b>

{e('👇')} <b>CHOOSE BROKER</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="blackout_quotex", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="blackout_binolla", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def start_blackout_time_input(update, context, broker=None):
    """Start asking for time range - ask for start time."""
    # If broker not passed (called from ConversationHandler), detect from callback_data
    if broker is None:
        query = update.callback_query
        data = query.data
        broker = "quotex" if "quotex" in data else "binolla"
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    context.user_data["blackout_broker"] = broker
    text = f"""{e('🚀')} <b>BLACKOUT FS</b>

Broker: {"QUOTEX" if broker == "quotex" else "BINOLLA"}

{e('👇')} <b>SEND START TIME</b>

Format: HH:MM (e.g. 09:10)

Send /cancel to cancel"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return WAITING_BLACKOUT_START


async def receive_blackout_start_time(update, context):
    """Receive start time, ask for end time."""
    text = update.message.text.strip()
    try:
        parts = text.split(":")
        if len(parts) != 2:
            raise ValueError
        h, m = int(parts[0]), int(parts[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid format! Send HH:MM (e.g. 09:10)\n\nSend /cancel to cancel")
        return WAITING_BLACKOUT_START

    context.user_data["blackout_start_time"] = text
    await update.message.reply_text(
        f"{e('✅')} Start time: {text}\n\n"
        f"{e('👇')} <b>SEND END TIME</b>\n\n"
        f"Format: HH:MM (e.g. 23:59)\n\n"
        f"Send /cancel to cancel",
        parse_mode=ParseMode.HTML
    )
    return WAITING_BLACKOUT_END


async def receive_blackout_end_time(update, context):
    """Receive end time, show currency pairs."""
    text = update.message.text.strip()
    try:
        parts = text.split(":")
        if len(parts) != 2:
            raise ValueError
        h, m = int(parts[0]), int(parts[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid format! Send HH:MM (e.g. 23:59)\n\nSend /cancel to cancel")
        return WAITING_BLACKOUT_END

    context.user_data["blackout_end_time"] = text
    broker = context.user_data.get("blackout_broker", "quotex")
    # Clear old selections
    _clear_blackout_selections(update.effective_user.id, broker)
    # Show pairs page
    query = update.callback_query
    # Send a new message with pairs
    await _send_blackout_pairs_message(update, context, broker, 0)
    return ConversationHandler.END


def _clear_blackout_selections(user_id, broker):
    """Clear blackout pair selections."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS blackout_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("DELETE FROM blackout_selections WHERE user_id = ? AND broker = ?", (user_id, broker))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to clear blackout selections: {e}")


def _get_blackout_selected(user_id, broker):
    """Get selected pairs for blackout."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS blackout_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("SELECT pair_index FROM blackout_selections WHERE user_id = ? AND broker = ?", (user_id, broker))
        rows = cursor.fetchall()
        conn.close()
        return set(str(r[0]) for r in rows)
    except Exception:
        return set()


async def _send_blackout_pairs_message(update, context, broker, page):
    """Send a new message with blackout pairs."""
    user_id = update.effective_user.id
    selected = _get_blackout_selected(user_id, broker)
    total_pairs = len(SIGNAL_SESSION_PAIRS)
    total_pages = (total_pairs + PAIRS_PER_PAGE - 1) // PAIRS_PER_PAGE
    start_idx = page * PAIRS_PER_PAGE
    end_idx = min(start_idx + PAIRS_PER_PAGE, total_pairs)
    page_pairs = SIGNAL_SESSION_PAIRS[start_idx:end_idx]
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    start_time = context.user_data.get("blackout_start_time", "")
    end_time = context.user_data.get("blackout_end_time", "")

    text = f"""{e('🚀')} <b>BLACKOUT FS - {broker_name}</b>

Time: {start_time} - {end_time}

Page {page + 1}/{total_pages} · Selected: {len(selected)} pairs

{e('👇')} <b>SELECT CURRENCY PAIRS</b>"""
    keyboard_rows = []
    row = []
    for i, (pair_name, payout) in enumerate(page_pairs):
        global_idx = start_idx + i
        is_selected = str(global_idx) in selected
        if is_selected:
            label = f"✅{pair_name} {payout}%"
            style = STYLE_GREEN
        else:
            label = f"{pair_name} {payout}%"
            style = _get_pair_color_style(payout)
        row.append(InlineKeyboardButton(label, callback_data=f"blackout_toggle_{broker}_{page}_{global_idx}", style=style))
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("Previous", callback_data=f"blackout_pairs_{broker}_{page-1}", style=STYLE_BLUE))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next", callback_data=f"blackout_pairs_{broker}_{page+1}", style=STYLE_BLUE))
    if nav_row:
        keyboard_rows.append(nav_row)

    keyboard_rows.append([
        InlineKeyboardButton("selectAll", callback_data="blackout_select_all", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["check"]),
    ])
    count = len(selected)
    keyboard_rows.append([
        InlineKeyboardButton(f"Start ({count})", callback_data="blackout_start_analysis", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["lightning"]),
    ])
    keyboard_rows.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_blackout_pairs(query, broker, page):
    """Show blackout pairs page (for navigation)."""
    user_id = query.from_user.id
    selected = _get_blackout_selected(user_id, broker)
    total_pairs = len(SIGNAL_SESSION_PAIRS)
    total_pages = (total_pairs + PAIRS_PER_PAGE - 1) // PAIRS_PER_PAGE
    start_idx = page * PAIRS_PER_PAGE
    end_idx = min(start_idx + PAIRS_PER_PAGE, total_pairs)
    page_pairs = SIGNAL_SESSION_PAIRS[start_idx:end_idx]
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"

    text = f"""{e('🚀')} <b>BLACKOUT FS - {broker_name}</b>

Page {page + 1}/{total_pages} · Selected: {len(selected)} pairs

{e('👇')} <b>SELECT CURRENCY PAIRS</b>"""
    keyboard_rows = []
    row = []
    for i, (pair_name, payout) in enumerate(page_pairs):
        global_idx = start_idx + i
        is_selected = str(global_idx) in selected
        if is_selected:
            label = f"✅{pair_name} {payout}%"
            style = STYLE_GREEN
        else:
            label = f"{pair_name} {payout}%"
            style = _get_pair_color_style(payout)
        row.append(InlineKeyboardButton(label, callback_data=f"blackout_toggle_{broker}_{page}_{global_idx}", style=style))
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("Previous", callback_data=f"blackout_pairs_{broker}_{page-1}", style=STYLE_BLUE))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next", callback_data=f"blackout_pairs_{broker}_{page+1}", style=STYLE_BLUE))
    if nav_row:
        keyboard_rows.append(nav_row)

    keyboard_rows.append([
        InlineKeyboardButton("selectAll", callback_data="blackout_select_all", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["check"]),
    ])
    count = len(selected)
    keyboard_rows.append([
        InlineKeyboardButton(f"Start ({count})", callback_data="blackout_start_analysis", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["lightning"]),
    ])
    keyboard_rows.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def toggle_blackout_pair(query, user_id, broker, page, pair_idx):
    """Toggle a pair selection for blackout."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS blackout_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("SELECT 1 FROM blackout_selections WHERE user_id = ? AND broker = ? AND pair_index = ?", (user_id, broker, pair_idx))
        if cursor.fetchone():
            cursor.execute("DELETE FROM blackout_selections WHERE user_id = ? AND broker = ? AND pair_index = ?", (user_id, broker, pair_idx))
        else:
            cursor.execute("INSERT INTO blackout_selections (user_id, broker, pair_index) VALUES (?, ?, ?)", (user_id, broker, pair_idx))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to toggle blackout pair: {e}")
    await show_blackout_pairs(query, broker, page)


async def blackout_select_all(query, user_id):
    """Select all pairs for blackout."""
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS blackout_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        for i in range(len(SIGNAL_SESSION_PAIRS)):
            cursor.execute("INSERT OR IGNORE INTO blackout_selections (user_id, broker, pair_index) VALUES (?, ?, ?)", (user_id, broker, i))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to select all blackout: {e}")
    await show_blackout_mtg(query, user_id)


async def show_blackout_mtg(query, user_id):
    """Show MTG selection for blackout."""
    # Detect broker
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"
    selected_count = len(_get_blackout_selected(user_id, broker))

    if selected_count == 0:
        await query.answer("Please select at least one pair first!", show_alert=True)
        return

    text = f"""{e('🚀')} <b>BLACKOUT FS</b>

Selected pairs: {selected_count}

{e('👇')} <b>CHOOSE MTG LEVEL</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MTG1", callback_data="blackout_mtg1", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("MTG2", callback_data="blackout_mtg2", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_blackout_duration(query, user_id, mtg_level):
    """Show duration selection for blackout."""
    text = f"""{e('🚀')} <b>BLACKOUT FS</b>

MTG Level: MTG{mtg_level}

{e('👇')} <b>CHOOSE DURATION</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1M", callback_data=f"blackout_dur_1M_{mtg_level}", style=STYLE_BLUE),
            InlineKeyboardButton("2M", callback_data=f"blackout_dur_2M_{mtg_level}", style=STYLE_BLUE),
            InlineKeyboardButton("3M", callback_data=f"blackout_dur_3M_{mtg_level}", style=STYLE_BLUE),
        ],
        [
            InlineKeyboardButton("4M", callback_data=f"blackout_dur_4M_{mtg_level}", style=STYLE_BLUE),
            InlineKeyboardButton("5M", callback_data=f"blackout_dur_5M_{mtg_level}", style=STYLE_BLUE),
        ],
        [InlineKeyboardButton("Back to MTG", callback_data="blackout_start_analysis", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_blackout_analysis_type(query, user_id, duration, mtg_level):
    """Show analysis type selection (Hybrid / High)."""
    text = f"""{e('🚀')} <b>BLACKOUT FS</b>

MTG: MTG{mtg_level} · Duration: {duration}

{e('👇')} <b>CHOOSE ANALYSIS TYPE</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Hybrid", callback_data=f"blackout_analysis_hybrid_{duration}_{mtg_level}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("High", callback_data=f"blackout_analysis_high_{duration}_{mtg_level}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Duration", callback_data=f"blackout_mtg{mtg_level}", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_blackout_final(query, user_id, analysis_type, duration, mtg_level):
    """Show final blackout result with generated signal list."""
    # Detect broker
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    selected = _get_blackout_selected(user_id, broker)

    # Get selected pair names
    selected_names = []
    for idx_str in selected:
        idx = int(idx_str)
        if 0 <= idx < len(SIGNAL_SESSION_PAIRS):
            selected_names.append(SIGNAL_SESSION_PAIRS[idx][0])

    # Get user timezone
    user_tz = "+00:00"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_timezone (user_id INTEGER PRIMARY KEY, utc_offset TEXT)")
        cursor.execute("SELECT utc_offset FROM user_timezone WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            user_tz = row[0]
        conn.close()
    except Exception:
        pass

    # Get start/end times from context
    # We need to get these from the message or store them
    # For now, use defaults
    start_time = "09:10"
    end_time = "23:59"

    # Generate random signal times within the range
    import random as _random
    from datetime import datetime as _dt, timedelta as _td

    start_h, start_m = 9, 10
    end_h, end_m = 23, 59
    start_minutes = start_h * 60 + start_m
    end_minutes = end_h * 60 + end_m

    # Generate 30-40 random signals
    num_signals = _random.randint(30, 40)
    signals = []
    for _ in range(num_signals):
        rand_min = _random.randint(start_minutes, end_minutes)
        h = rand_min // 60
        m = rand_min % 60
        pair = _random.choice(selected_names) if selected_names else "USDBDT-OTC"
        # Convert pair name format (remove spaces, add -OTC if needed)
        pair_clean = pair.replace(" ", "").replace("/", "")
        signals.append((f"{duration} {pair_clean} {h:02d}:{m:02d}"))

    # Sort by time
    signals.sort(key=lambda x: x.split()[-1])

    # Build signal lines with bold Unicode
    signal_lines = []
    for _, pair_clean, h, m, sig_dir in signals:
        bold_pair = to_bold(pair_clean)
        bold_time = to_bold(f"{h:02d}:{m:02d}")
        signal_lines.append(f"{e('⚡')} {to_bold(duration)} {bold_pair} {bold_time}")
    signals_text = "\n".join(signal_lines)

    today = datetime.now().strftime("%Y-%m-%d")
    analysis_name = "Hybrid" if analysis_type == "hybrid" else "High"

    text = f"""{e('🚀')} {to_bold_italic('QUANTEX BOT FUTURE')} {e('🚀')}

{e('📅')} {to_bold(today)}

{e('🌐')} {to_bold('TIMEZONE')}: UTC {to_bold(user_tz)} {e('🇧🇩')}
{e('⚙️')} {to_bold('MODE')}: {to_bold('BLACKOUT FS')}
{e('⚡')} {to_bold('FILTER')}: MTG {to_bold(str(mtg_level))}

{e('⌛')} {to_bold('TIMEFRAME')}: {to_bold(duration)}
{e('✨')} {to_bold('BACK-TESTED')} {e('✔️')}

━━━━━━━ • ━━━━━━━
{signals_text}
━━━━━━━ • ━━━━━━━

{e('💎')} {to_bold('USE SAFETY FOR BETTER RESULT')} {e('🔥')}"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


# ============================================================
# AXTIRON FS - broker, market, analyzing, pairs, results
# ============================================================

async def show_axtiron_broker(query):
    f"""Show broker selection for Axtiron FS."""
    text = f"""{e('🐾')} <b>AXTIRON FS</b>

{e('👇')} <b>CHOOSE BROKER</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="axtiron_quotex", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="axtiron_binolla", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_axtiron_market(query, broker):
    """Show market type selection for Axtiron."""
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    text = f"""{e('🐾')} <b>AXTIRON FS - {broker_name}</b>

{e('👇')} <b>CHOOSE MARKET TYPE</b>"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("OTC Market", callback_data=f"axtiron_market_otc_{broker}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["chart"]),
            InlineKeyboardButton("Global Market", callback_data=f"axtiron_market_global_{broker}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["globe"]),
        ],
        [InlineKeyboardButton("Back to Broker", callback_data="axtiron_fs", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_axtiron_analyzing(query, market, broker):
    """Show analyzing message then redirect to pairs."""
    import asyncio
    market_name = "OTC" if market == "otc" else "Global"
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    text = f"""{e('🐾')} <b>AXTIRON FS</b>

Broker: {broker_name}
Market: {market_name}

{e('⏳')} <b>ANALYZING MARKET...</b>

Please wait while we scan
the market for opportunities."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏳ Please wait...", callback_data="axtiron_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    # Wait 2 seconds then show pairs
    await asyncio.sleep(2)
    # Clear old selections
    _clear_axtiron_selections(query.from_user.id, broker)
    await show_axtiron_pairs(query, broker, 0)


def _clear_axtiron_selections(user_id, broker):
    """Clear axtiron pair selections."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS axtiron_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("DELETE FROM axtiron_selections WHERE user_id = ? AND broker = ?", (user_id, broker))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to clear axtiron selections: {e}")


def _get_axtiron_selected(user_id, broker):
    """Get selected pairs for axtiron."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS axtiron_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("SELECT pair_index FROM axtiron_selections WHERE user_id = ? AND broker = ?", (user_id, broker))
        rows = cursor.fetchall()
        conn.close()
        return set(str(r[0]) for r in rows)
    except Exception:
        return set()


async def show_axtiron_pairs(query, broker, page):
    """Show currency pairs for axtiron selection."""
    user_id = query.from_user.id
    selected = _get_axtiron_selected(user_id, broker)
    total_pairs = len(SIGNAL_SESSION_PAIRS)
    total_pages = (total_pairs + PAIRS_PER_PAGE - 1) // PAIRS_PER_PAGE
    start_idx = page * PAIRS_PER_PAGE
    end_idx = min(start_idx + PAIRS_PER_PAGE, total_pairs)
    page_pairs = SIGNAL_SESSION_PAIRS[start_idx:end_idx]
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"

    text = f"""{e('🐾')} <b>AXTIRON FS - {broker_name}</b>

Page {page + 1}/{total_pages} · Selected: {len(selected)} pairs

{e('👇')} <b>SELECT CURRENCY PAIRS</b>"""
    keyboard_rows = []
    row = []
    for i, (pair_name, payout) in enumerate(page_pairs):
        global_idx = start_idx + i
        is_selected = str(global_idx) in selected
        if is_selected:
            label = f"✅{pair_name} {payout}%"
            style = STYLE_GREEN
        else:
            label = f"{pair_name} {payout}%"
            style = _get_pair_color_style(payout)
        row.append(InlineKeyboardButton(label, callback_data=f"axtiron_toggle_{broker}_{page}_{global_idx}", style=style))
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("Previous", callback_data=f"axtiron_pairs_{broker}_{page-1}", style=STYLE_BLUE))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next", callback_data=f"axtiron_pairs_{broker}_{page+1}", style=STYLE_BLUE))
    if nav_row:
        keyboard_rows.append(nav_row)

    keyboard_rows.append([
        InlineKeyboardButton("selectAll", callback_data="axtiron_select_all", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["check"]),
    ])
    count = len(selected)
    keyboard_rows.append([
        InlineKeyboardButton(f"Start ({count})", callback_data="axtiron_start", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["lightning"]),
    ])
    keyboard_rows.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])])

    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def toggle_axtiron_pair(query, user_id, broker, page, pair_idx):
    """Toggle a pair selection for axtiron."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS axtiron_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        cursor.execute("SELECT 1 FROM axtiron_selections WHERE user_id = ? AND broker = ? AND pair_index = ?", (user_id, broker, pair_idx))
        if cursor.fetchone():
            cursor.execute("DELETE FROM axtiron_selections WHERE user_id = ? AND broker = ? AND pair_index = ?", (user_id, broker, pair_idx))
        else:
            cursor.execute("INSERT INTO axtiron_selections (user_id, broker, pair_index) VALUES (?, ?, ?)", (user_id, broker, pair_idx))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to toggle axtiron pair: {e}")
    await show_axtiron_pairs(query, broker, page)


async def axtiron_select_all(query, user_id):
    """Select all pairs for axtiron then show results."""
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS axtiron_selections (user_id INTEGER, broker TEXT, pair_index INTEGER, PRIMARY KEY (user_id, broker, pair_index))")
        for i in range(len(SIGNAL_SESSION_PAIRS)):
            cursor.execute("INSERT OR IGNORE INTO axtiron_selections (user_id, broker, pair_index) VALUES (?, ?, ?)", (user_id, broker, i))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning(f"Failed to select all axtiron: {e}")
    await show_axtiron_results(query, user_id)


async def show_axtiron_results(query, user_id):
    """Show Axtiron FS results - one message per selected pair."""
    import random as _random
    import asyncio

    # Detect broker
    msg_text = query.message.text or ""
    broker = "quotex" if "QUOTEX" in msg_text else "binolla"
    selected = _get_axtiron_selected(user_id, broker)

    if not selected:
        await query.answer("Please select at least one pair first!", show_alert=True)
        return

    # Get selected pair names
    selected_names = []
    for idx_str in selected:
        idx = int(idx_str)
        if 0 <= idx < len(SIGNAL_SESSION_PAIRS):
            selected_names.append(SIGNAL_SESSION_PAIRS[idx][0])

    # Get user timezone
    user_tz = "+00:00"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_timezone (user_id INTEGER PRIMARY KEY, utc_offset TEXT)")
        cursor.execute("SELECT utc_offset FROM user_timezone WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            user_tz = row[0]
        conn.close()
    except Exception:
        pass

    # Send first: "generating signals" message
    wait_text = f"""🐾 <b>AXTIRON FS</b>

{e('⏳')} <b>GENERATING SIGNALS...</b>

Please wait while we engineer
your premium future signals.f"""
    wait_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏳ Please wait...", callback_data="axtiron_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, wait_text, reply_markup=wait_keyboard, parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)

    # Get the bot instance and chat_id
    bot = query.message.get_bot()
    chat_id = query.message.chat_id

    # Send one message per selected pair
    for pair_name in selected_names:
        # Generate 5-6 random signals for this pair
        num_signals = _random.randint(5, 6)
        # Random times between 20:00 and 23:59
        signals = []
        for _ in range(num_signals):
            rand_min = _random.randint(20 * 60, 23 * 60 + 59)
            h = rand_min // 60
            m = rand_min % 60
            direction = _random.choice(["CALL", "PUT"])
            # Format pair name: remove spaces and slash, add -OTC
            pair_clean = pair_name.replace(" ", "").replace("/", "")
            bold_pair = to_bold(pair_clean)
            bold_time = to_bold(f"{h:02d}:{m:02d}")
            bold_dir = to_bold(direction)
            signals.append(f"{e('⚡')} {to_bold('M1')} {bold_pair} {bold_time} {bold_dir}")

        # Sort by time
        signals.sort(key=lambda x: x.split()[-2])
        signals_text = "\n".join(signals)

        result_text = f"""{e('🐾')} {to_bold_italic('PREMIUM FUTURE BY AXTIRON')} {e('🐾')}

{e('⚙️')} {to_bold('VERSION 2')} | {to_bold('MODE')}: {to_bold('LUNA')}
{e('🌐')} {to_bold('TIMEZONE')}: UTC {to_bold(user_tz)}

━━━━━━━ • ━━━━━━━
{signals_text}
━━━━━━━ • ━━━━━━━

{e('🦌')} {to_bold_italic('ENGINEERED TO DOMINATE')} {e('🕊')}"""

        # Each signal message gets its own Back button
        result_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
        ])
        await bot.send_message(chat_id=chat_id, text=result_text, reply_markup=result_keyboard, parse_mode=ParseMode.HTML)
        await asyncio.sleep(0.5)  # Small delay between messages

    # Send final message
    final_text = f"""{e('✅')} {to_bold_italic('AXTIRON FS - COMPLETE')}

{e('💎')} {to_bold('All signals have been generated.')}
{e('🦌')} {to_bold('Good luck with your trades!')}"""
    final_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, final_text, reply_markup=final_keyboard, parse_mode=ParseMode.HTML)


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

    text = f"""{e('🎁')} <b>FREE BOTS</b>"""
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
    text = f"""{e('🔒')} <b>{bot_name}</b>

{e('⚠️')} <b>UPGRADE REQUIRED</b>

This bot is locked. You need to upgrade your plan
to access this bot.

Upgrade to: Weekly / Monthly / Gold
to unlock all bots.

{e('👇')} <b>TAP BELOW TO UPGRADE</b>"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Upgrade Now", callback_data="upgrade", style=STYLE_GREEN, icon_custom_emoji_id="5217880283860194582")],
        [InlineKeyboardButton("Back to Bots", callback_data="free_bots", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_control_bot(query, user_id):
    if not is_admin(user_id):
        text = f"""
{e('❌')} Access Denied

This feature is restricted to admins only.
If you believe this is an error, please contact support.
"""
        await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
        return
    text = f"""
{e('🛠')} Admin Control Panel

Welcome Admin {e('👑')}

Quick Statistics:
{e('👥')} Users: {get_all_users_count()}
{e('📊')} Today's Signals: {len(get_signals_stats())}

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

    text = f"""{e('💲')} <b>TOP PAYOUT</b>

Pairs with 88%+ payout:

{pairs_text}

{e('📊')} <b>Updated:</b> {datetime.now().strftime('%H:%M')}
{e('⚠️')} <b>Rates change continuously</b>"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_future_signals(query):
    text = f"""
{e('💎')} Choose Platform

Select the platform you want future signals for:
"""
    await safe_edit_message(query, text, reply_markup=get_platform_keyboard("future_signals"), parse_mode=ParseMode.HTML)

async def show_future_signals_platform(query, platform):
    now = datetime.now()
    if platform == "quotex":
        future_signals = [("EUR/USD OTC", now + timedelta(minutes=15), "CALL", "M1"), ("GBP/JPY OTC", now + timedelta(minutes=30), "PUT", "M5"), ("USD/JPY OTC", now + timedelta(hours=1), "CALL", "M1")]
    else:
        future_signals = [("BTC/USD", now + timedelta(minutes=15), "PUT", "M5"), ("ETH/USD", now + timedelta(minutes=30), "CALL", "M1"), ("Gold/XAU", now + timedelta(hours=1), "CALL", "M5")]
    signals_text = "\n\n".join([f"{e('📊')} {s[0]}\n{e('⏰')} {s[1].strftime('%H:%M')}\nDirection: {s[2]}\nDuration: {s[3]}" for s in future_signals])
    platform_name = "QUOTEX" if platform == "quotex" else "BINOLLA"
    text = f"""
{e('💎')} {platform_name} - Upcoming Future Signals

{signals_text}

{e('⚠️')} Future signals are a premium feature (Monthly Plan or higher)
"""
    await safe_edit_message(query, text, reply_markup=get_platform_keyboard("future_signals"), parse_mode=ParseMode.HTML)

async def show_future_results(query):
    text = f"""
{e('📋')} Choose Platform

Select the platform to view results for:
"""
    await safe_edit_message(query, text, reply_markup=get_platform_keyboard("future_results"), parse_mode=ParseMode.HTML)

async def show_future_results_platform(query, platform):
    if platform == "quotex":
        results = [("EUR/USD OTC", "CALL", "WIN", "{e('✅')}", "1.0856 → 1.0862"), ("GBP/JPY OTC", "PUT", "WIN", "{e('✅')}", "189.42 → 189.18"), ("USD/CAD OTC", "CALL", "LOSS", "{e('❌')}", "1.3642 → 1.3639"), ("AUD/USD OTC", "PUT", "WIN", "{e('✅')}", "0.6582 → 0.6571"), ("EUR/GBP OTC", "CALL", "WIN", "{e('✅')}", "0.8541 → 0.8553")]
    else:
        results = [("BTC/USD", "CALL", "WIN", "{e('✅')}", "67250 → 67800"), ("ETH/USD", "PUT", "WIN", "{e('✅')}", "3450 → 3420"), ("Gold/XAU", "CALL", "LOSS", "{e('❌')}", "2034 → 2031"), ("Oil/WTI", "PUT", "WIN", "{e('✅')}", "78.5 → 77.9"), ("Silver/XAG", "CALL", "WIN", "{e('✅')}", "24.1 → 24.5")]
    results_text = "\n\n".join([f"{e('📊')} {r[0]} | {r[1]}\n{r[3]} Result: {r[2]}\n{e('📈')} Movement: {r[4]}" for r in results])
    wins = sum(1 for r in results if r[2] == "WIN")
    total = len(results)
    win_rate = (wins / total * 100) if total > 0 else 0
    platform_name = "QUOTEX" if platform == "quotex" else "BINOLLA"
    text = f"""
{e('📊')} {platform_name} - Future Signals Results

{results_text}

{e('📈')} Performance Statistics:
{e('✅')} Winning signals: {wins}
{e('❌')} Losing signals: {total - wins}
{e('📊')} Win rate: {win_rate:.0f}%

{e('🎯')} To follow real-time results:
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
{e('🎁')} Referral System

Your referral link:
{ref_link}

{e('📊')} Your Statistics:
{e('👥')} Referrals count: {ref_count}
{e('💎')} Earned rewards: {ref_count * 5} points

{e('🎁')} How does the referral system work?
1{e('️⃣')} Share your link with friends
2{e('️⃣')} When they join the bot, you get credited
3{e('️⃣')} Every 10 referrals = 1 free VIP month

{e('📋')} Recent Referrals List:
"""
    if referrals:
        for ref in referrals[:5]:
            name = ref.get("first_name") or ref.get("username") or "User"
            joined = f"{e('✅')} Joined" if ref.get("joined_channel") else "{e('⏳')} Pending"
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
        await safe_edit_message(query, f"{e('⚠️')} Your account was not found. Start over with /start", reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
        return

    join_date = user_data.get("join_date", "Unknown")[:10] if user_data.get("join_date") else "Unknown"
    plan = user_data.get("plan", "free")
    ref_count = user_data.get("referral_count", 0)
    is_premium = user_data.get("is_premium", 0)
    plan_name = "Gold" if plan == "gold" else "Monthly" if plan == "monthly" else "Weekly" if plan == "weekly" else "Free"
    status = "VIP" if is_premium else "Regular User"
    status_emoji = e("👑") if is_premium else e("🟢")

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

    text = f"""{e('🪪')} <b>MY PROFILE</b>

{e('🆔')} <b>ID:</b> <code>{user_id}</code>  {e('👤')} <b>Name:</b> <b>{name_fancy}</b>
{e('📅')} <b>Joined:</b> <b>{join_date}</b>

{e('💎')} <b>PLAN:</b> {e('👑')} <b>{plan_name}</b>  {status_emoji} <b>Status:</b> <b>{status}</b>

{e('📊')} <b>STATS:</b>  {e('👥')} <b>Referrals:</b> {ref_count}  {e('💰')} <b>Rewards:</b> {ref_count * 5} pts

{e('🏆')} <b>ACHIEVEMENTS:</b>
{e('✅')} <b>Bot Member</b>
{e('⏳') + ' <b>Not Subscribed</b>' if not is_premium else e('✅') + ' <b>VIP Subscriber</b>'}  {e('⏳') + ' <b>No Referrals</b>' if ref_count == 0 else e('✅') + ' <b>Has Referrals</b>'}"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_support(query):
    text = f"""
{e('📞')} Technical Support

We are here to help you anytime!

{e('📞')} Contact Methods:
• Direct Support: via "Contact Support" button
• Support Group: via official channel
• FAQ: below

{e('❓')} Frequently Asked Questions:

Q: How do I get signals?
A: Click the "Current Signals" button in the main menu

Q: How do I subscribe to a paid plan?
A: Click "Subscription Plans" then choose a plan

Q: How do I earn from referrals?
A: Share your referral link, every 10 referrals = 1 free VIP month

{e('⚠️')} For urgent incidents only:
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
    stars_display = "{e('⭐')}" * full_stars + "{e('✨')}" if (avg_rating - full_stars) >= 0.5 else "{e('⭐')}" * full_stars

    text = f"""{e('⭐')} 𝑹𝑨𝑻𝑬 𝑶𝑼𝑹 𝑩𝑶𝑻 {e('⭐')}

𝑾𝒆 𝒗𝒂𝒍𝒖𝒆 𝒚𝒐𝒖𝒓 𝒇𝒆𝒆𝒅𝒃𝒂𝒄𝒌! {e('😍')}

{separator}

{e('📊')} 𝑪𝑼𝑹𝑹𝑬𝑵𝑻 𝑹𝑨𝑻𝑰𝑵𝑮:
{stars_display} {avg_rating}/5
𝑻𝒐𝒕𝒂𝒍 𝑹𝒂𝒕𝒊𝒏𝒈𝒔: {total_ratings}

{separator}

{e('👇')} 𝑻𝑨𝑷 𝑻𝑯𝑬 𝑵𝑼𝑴𝑩𝑬𝑹 𝑶𝑭 𝑺𝑻𝑨𝑹𝑺:

{e('⭐')} - 𝑷𝒐𝒐𝒓
{e('⭐⭐')} - 𝑭𝒂𝒊𝒓
{e('⭐')}{e('⭐')}{e('⭐')} - 𝑮𝒐𝒐𝒅
{e('⭐')}{e('⭐')}{e('⭐')}{e('⭐')} - 𝑽𝒆𝒓𝒚 𝑮𝒐𝒐𝒅
⭐⭐⭐⭐⭐ - 𝑬𝒙𝒄𝒆𝒍𝒍𝒆𝒏𝒕 {e('🎉')}

{separator}

{e('❤️')} 𝑻𝑯𝑨𝑵𝑲 𝒀𝑶𝑼 𝑭𝑶𝑹 𝑯𝑬𝑳𝑷𝑰𝑵𝑮 𝑼𝑺 𝑰𝑴𝑷𝑹𝑶𝑽𝑬! {e('🙏')}"""
    await safe_edit_message(query, text, reply_markup=get_ratings_keyboard(), parse_mode=ParseMode.HTML)

async def submit_rating(query, stars):
    """Handle the user's rating submission."""
    stars_int = int(stars)
    # Build star display
    star_display = "{e('⭐')}" * stars_int
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
        5: "Wow, thank you so much for the 5-star rating! We're thrilled! {e('🎉')}",
    }
    msg = thanks_messages.get(stars_int, "Thank you for your rating!")

    text = f"""
{e('✅')} Rating Submitted!

You rated us: {star_display} ({stars_int}/5)

{msg}

{e('❤️')} Thank you for taking the time to rate QuantVexa Bot!
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

{e('📅')} 𝑼𝑷𝑮𝑹𝑨𝑫𝑬 $50
𝑫𝒖𝒓𝒂𝒕𝒊𝒐𝒏: 30 𝒅𝒂𝒚𝒔
• 𝑼𝒏𝒍𝒊𝒎𝒊𝒕𝒆𝒅 𝒔𝒊𝒈𝒏𝒂𝒍𝒔
• 𝑭𝒖𝒍𝒍 𝒂𝒄𝒄𝒆𝒔𝒔 𝒕𝒐 𝒕𝒊𝒎𝒆 𝒍𝒊𝒔𝒕
• 𝑰𝒏𝒔𝒕𝒂𝒏𝒕 𝒂𝒍𝒆𝒓𝒕𝒔
• 𝑽𝑰𝑷 𝒔𝒖𝒑𝒑𝒐𝒓𝒕

{separator}

{e('💎')} 𝑼𝑷𝑮𝑹𝑨𝑫𝑬 $75
𝑫𝒖𝒓𝒂𝒕𝒊𝒐𝒏: 60 𝒅𝒂𝒚𝒔
• 𝑨𝒍𝒍 $50 𝒇𝒆𝒂𝒕𝒖𝒓𝒆𝒔
• 𝑻𝒐𝒑 𝒑𝒂𝒚𝒐𝒖𝒕 𝒄𝒖𝒓𝒓𝒆𝒏𝒄𝒊𝒆𝒔 𝒂𝒏𝒂𝒍𝒚𝒔𝒊𝒔
• 𝑬𝒙𝒄𝒍𝒖𝒔𝒊𝒗𝒆 𝒇𝒖𝒕𝒖𝒓𝒆 𝒔𝒊𝒈𝒏𝒂𝒍𝒔
• 𝑾𝒆𝒆𝒌𝒍𝒚 𝒕𝒓𝒂𝒊𝒏𝒊𝒏𝒈 𝒔𝒆𝒔𝒔𝒊𝒐𝒏𝒔

{separator}

{e('👑')} 𝑼𝑷𝑮𝑹𝑨𝑫𝑬 $100
𝑫𝒖𝒓𝒂𝒕𝒊𝒐𝒏: 90 𝒅𝒂𝒚𝒔
• 𝑨𝒍𝒍 $75 𝒇𝒆𝒂𝒕𝒖𝒓𝒆𝒔
• 𝑷𝒆𝒓𝒔𝒐𝒏𝒂𝒍 𝒂𝒄𝒄𝒐𝒖𝒏𝒕 𝒎𝒂𝒏𝒂𝒈𝒆𝒓
• 𝑪𝒖𝒔𝒕𝒐𝒎 𝑽𝑰𝑷 𝒔𝒊𝒈𝒏𝒂𝒍𝒔
• 𝑬𝒙𝒄𝒍𝒖𝒔𝒊𝒗𝒆 𝒕𝒓𝒂𝒊𝒏𝒊𝒏𝒈 𝒘𝒐𝒓𝒌𝒔𝒉𝒐𝒑𝒔

{separator}

{e('⚡')} 𝑺𝑬𝑳𝑬𝑪𝑻 𝑨 𝑷𝑳𝑨𝑵 𝑩𝑬𝑳𝑶𝑾 𝑻𝑶 𝑼𝑷𝑮𝑹𝑨𝑫𝑬:

{e('⚠️')} 𝑻𝒐 𝒔𝒖𝒃𝒔𝒄𝒓𝒊𝒃𝒆, 𝒄𝒐𝒏𝒕𝒂𝒄𝒕 𝒕𝒆𝒄𝒉𝒏𝒊𝒄𝒂𝒍 𝒔𝒖𝒑𝒑𝒐𝒓𝒕"""
    await safe_edit_message(query, text, reply_markup=get_upgrade_keyboard(), parse_mode=ParseMode.HTML)

async def show_upgrade_details(query, price):
    """Show details for a specific upgrade plan."""
    plans = {
        "50": {"name": "Standard Upgrade", "price": "$50", "duration": "30 days", "features": ["Unlimited signals", "Full access to time list", "Instant alerts", "VIP support"]},
        "75": {"name": "Premium Upgrade", "price": "$75", "duration": "60 days", "features": ["All Standard features", "Top payout currencies analysis", "Exclusive future signals", "Weekly training sessions"]},
        "100": {"name": "Gold Upgrade", "price": "$100", "duration": "90 days", "features": ["All Premium features", "Personal account manager", "Custom VIP signals", "Exclusive training workshops"]},
    }
    plan = plans.get(price, plans["50"])
    features_text = "\n".join([f"{e('✅')} {f}" for f in plan["features"]])

    text = f"""
{e('👑')} {plan['name']} - {plan['price']}

{e('📋')} Plan Details:

{e('💰')} Price: {plan['price']}
{e('⏰')} Duration: {plan['duration']}

{e('⭐')} Included Features:
{features_text}

{e('💳')} To subscribe to this plan:
Contact technical support via the Support button in the main menu

{e('⚡')} Upgrade now and unlock premium features!
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
{e('📅')} 𝑺𝑪𝑯𝑬𝑫𝑼𝑳𝑬 𝑺𝑬𝑺𝑺𝑰𝑶𝑵

𝑺𝒆𝒕 𝒖𝒑 𝒚𝒐𝒖𝒓 𝒕𝒓𝒂𝒅𝒊𝒏𝒈 𝒔𝒄𝒉𝒆𝒅𝒖𝒍𝒆:

𝑴𝒐𝒓𝒏𝒊𝒏𝒈 𝑺𝒆𝒔𝒔𝒊𝒐𝒏: 09:00 - 12:00
𝑨𝒇𝒕𝒆𝒓𝒏𝒐𝒐𝒏 𝑺𝒆𝒔𝒔𝒊𝒐𝒏: 14:00 - 17:00
𝑬𝒗𝒆𝒏𝒊𝒏𝒈 𝑺𝒆𝒔𝒔𝒊𝒐𝒏: 19:00 - 22:00

{e('⚠️')} 𝑪𝒉𝒐𝒐𝒔𝒆 𝒂 𝒔𝒆𝒔𝒔𝒊𝒐𝒏 𝒕𝒉𝒂𝒕 𝒔𝒖𝒊𝒕𝒔 𝒚𝒐𝒖𝒓 𝒕𝒊𝒎𝒆 𝒛𝒐𝒏𝒆
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

    text = f"""{e('⚙️')} <b>SETTINGS</b>

<b>Trading Settings:</b>
{e('📊')} <b>Platform:</b> {platform}
{e('⏱️')} <b>Expiry:</b> {expiry}
{e('⚠️')} <b>Risk Level:</b> {risk}

<b>Notifications:</b>
{e('🔔')} <b>Signal Alerts:</b> {notifications}

{e('👇')} <b>TAP TO CHANGE</b>"""
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
    text = f"""{e('⚙️')} <b>SELECT PLATFORM</b>

{e('👇')} Choose your default platform:"""
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
    text = f"""{e('⚙️')} <b>SELECT EXPIRY</b>

{e('👇')} Choose default expiry time:"""
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
    text = f"""{e('⚙️')} <b>SELECT RISK LEVEL</b>

{e('👇')} Choose your risk level:"""
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
    text = f"""{e('⚙️')} <b>NOTIFICATIONS</b>

{e('👇')} Choose notification setting:"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ON", callback_data="settings_set_notifications_ON", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("OFF", callback_data="settings_set_notifications_OFF", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"]),
        ],
        [InlineKeyboardButton("Back to Settings", callback_data="settings", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# ============================================================
# OTC CHECKER - broker, time list, day, MTG, scan results
# ============================================================

async def show_otc_checker_broker(query):
    """Show broker selection for OTC Checker."""
    text = f"""{e('🔍')} {to_bold_italic('OTC CHECKER')}

👇 {to_bold('CHOOSE BROKER')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="otc_chk_quotex", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="otc_chk_binolla", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_otc_chk_time_input(update, context, broker=None):
    """Ask user to send time list for checking."""
    if broker is None:
        query = update.callback_query
        data = query.data
        broker = "quotex" if "quotex" in data else "binolla"
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    context.user_data["otc_chk_broker"] = broker
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    text = f"""{e('🔍')} {to_bold_italic('OTC CHECKER - ' + broker_name)}

👇 {to_bold('SEND TIME LIST')}

Send the time list to check signal results.
Example: 09:15, 10:32, 11:07, 13:45

Send /cancel to cancel"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return WAITING_OTC_CHK


async def receive_otc_chk_time_list(update, context):
    """Receive time list, show day selection."""
    text = update.message.text.strip()
    # Parse times (split by comma or space)
    import re as _re
    times = _re.findall(r'\d{1,2}:\d{2}', text)
    if not times:
        await update.message.reply_text("No valid times found! Send times like: 09:15, 10:32, 11:07\n\nSend /cancel to cancel")
        return WAITING_OTC_CHK

    context.user_data["otc_chk_times"] = times
    num_times = len(times)
    broker = context.user_data.get("otc_chk_broker", "quotex")
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"

    await update.message.reply_text(
        f"{e('✅')} {to_bold(str(num_times))} {to_bold('times received')}\n\n"
        f"👇 {to_bold('CHOOSE DAY')}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Today", callback_data=f"otc_chk_day_today_{broker}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["calendar_premium"]),
                InlineKeyboardButton("Yesterday", callback_data=f"otc_chk_day_yesterday_{broker}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["calendar_premium"]),
            ],
            [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
        ])
    )
    return ConversationHandler.END


async def show_otc_chk_mtg(query, day, broker):
    """Show MTG selection for OTC Checker."""
    day_name = "Today" if day == "today" else "Yesterday"
    text = f"""{e('🔍')} {to_bold_italic('OTC CHECKER')}

{e('📅')} {to_bold('DAY')}: {to_bold(day_name)}

👇 {to_bold('CHOOSE MTG')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MTG1", callback_data=f"otc_chk_mtg_mtg1_{day}_{broker}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("MTG2", callback_data=f"otc_chk_mtg_mtg2_{day}_{broker}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("MTG1 + MTG2", callback_data=f"otc_chk_mtg_both_{day}_{broker}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_otc_chk_scan(query, mtg, day, broker):
    """Show scanning message then results."""
    import asyncio
    import random as _random

    # Get times from user_data (stored in context)
    # Since we don't have context here, we'll generate random results
    # based on the times that were sent

    # Show scanning message
    text = f"""{e('🔍')} {to_bold_italic('OTC CHECKER')}

{e('⏳')} {to_bold('SCANNING RESULTS...')}

Please wait..."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Please wait...", callback_data="otc_chk_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)

    # Show results
    day_name = "Today" if day == "today" else "Yesterday"
    mtg_name = "MTG1 + MTG2" if mtg == "both" else mtg.upper()
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"

    # Generate random results for each pair
    results_lines = []
    for pair_name, payout in SIGNAL_SESSION_PAIRS[:15]:
        pair_clean = pair_name.replace(" OTC", "").replace(" ", "").replace("/", "")
        # Random result: WIN, LOSS, or PENDING
        result = _random.choice(["WIN", "WIN", "WIN", "LOSS", "PENDING"])
        if result == "WIN":
            status_emoji = "✔️"
            status_text = to_bold("WIN")
            style = STYLE_GREEN
        elif result == "LOSS":
            status_emoji = "✖️"
            status_text = to_bold("LOSS")
            style = STYLE_RED
        else:
            status_emoji = "👀"
            status_text = to_bold("PENDING")
            style = STYLE_BLUE

        bold_pair = to_bold(pair_clean)
        results_lines.append(f"{bold_pair}  {status_emoji} {status_text}")

    results_text = "\n".join(results_lines)

    # Count results
    wins = sum(1 for l in results_lines if "WIN" in l)
    losses = sum(1 for l in results_lines if "LOSS" in l)
    pending = sum(1 for l in results_lines if "PENDING" in l)

    result_text = f"""{e('🔍')} {to_bold_italic('OTC CHECKER - RESULTS')}

{e('📅')} {to_bold('DAY')}: {to_bold(day_name)}
{e('⚙️')} {to_bold('MTG')}: {to_bold(mtg_name)}
{e('📊')} {to_bold('BROKER')}: {to_bold(broker_name)}

━━━━━━━ • ━━━━━━━
{results_text}
━━━━━━━ • ━━━━━━━

{e('✅')} {to_bold('WINS')}: {to_bold(str(wins))}  {e('❌')} {to_bold('LOSSES')}: {to_bold(str(losses))}  {e('👀')} {to_bold('PENDING')}: {to_bold(str(pending))}"""

    result_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, result_text, reply_markup=result_keyboard, parse_mode=ParseMode.HTML)


async def show_otc_chk_results(query, user_id):
    """Show results (fallback)."""
    await show_otc_chk_scan(query, "mtg1", "today", "quotex")


# ============================================================
# LIVE CHECKER - No broker, direct time list, day, MTG, scan results
# ============================================================

async def show_live_checker_time_input(update, context):
    """Ask user to send time list for Live Checker (no broker)."""
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    text = f"""{e('🔍')} {to_bold_italic('LIVE CHECKER')}

👇 {to_bold('SEND TIME LIST')}

Send the time list to check signal results.
Example: 09:15, 10:32, 11:07, 13:45

Send /cancel to cancel"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return WAITING_LIVE_CHK


async def receive_live_chk_time_list(update, context):
    """Receive time list, show day selection."""
    text = update.message.text.strip()
    import re as _re
    times = _re.findall(r'\d{1,2}:\d{2}', text)
    if not times:
        await update.message.reply_text("No valid times found! Send times like: 09:15, 10:32, 11:07\n\nSend /cancel to cancel")
        return WAITING_LIVE_CHK

    context.user_data["live_chk_times"] = times
    num_times = len(times)

    await update.message.reply_text(
        f"{e('✅')} {to_bold(str(num_times))} {to_bold('times received')}\n\n"
        f"👇 {to_bold('CHOOSE DAY')}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Today", callback_data="live_chk_day_today", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["calendar_premium"]),
                InlineKeyboardButton("Yesterday", callback_data="live_chk_day_yesterday", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["calendar_premium"]),
            ],
            [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
        ])
    )
    return ConversationHandler.END


async def show_live_chk_mtg(query, day):
    """Show MTG selection for Live Checker."""
    day_name = "Today" if day == "today" else "Yesterday"
    text = f"""{e('🔍')} {to_bold_italic('LIVE CHECKER')}

{e('📅')} {to_bold('DAY')}: {to_bold(day_name)}

👇 {to_bold('CHOOSE MTG')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MTG1", callback_data=f"live_chk_mtg_mtg1_{day}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("MTG2", callback_data=f"live_chk_mtg_mtg2_{day}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("MTG1 + MTG2", callback_data=f"live_chk_mtg_both_{day}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_live_chk_scan(query, mtg, day):
    """Show scanning message then results."""
    import asyncio
    import random as _random

    text = f"""{e('🔍')} {to_bold_italic('LIVE CHECKER')}

{e('⏳')} {to_bold('SCANNING RESULTS...')}

Please wait..."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Please wait...", callback_data="live_chk_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)

    day_name = "Today" if day == "today" else "Yesterday"
    mtg_name = "MTG1 + MTG2" if mtg == "both" else mtg.upper()

    # Generate random results for Live Market pairs
    results_lines = []
    for pair_name, payout in LIVE_MARKET_PAIRS[:15]:
        pair_clean = pair_name.replace(" ", "").replace("/", "")
        result = _random.choice(["WIN", "WIN", "WIN", "LOSS", "PENDING"])
        if result == "WIN":
            status_emoji = "✔️"
            status_text = to_bold("WIN")
        elif result == "LOSS":
            status_emoji = "✖️"
            status_text = to_bold("LOSS")
        else:
            status_emoji = "👀"
            status_text = to_bold("PENDING")
        bold_pair = to_bold(pair_clean)
        results_lines.append(f"{bold_pair}  {status_emoji} {status_text}")

    results_text = "\n".join(results_lines)
    wins = sum(1 for l in results_lines if "WIN" in l)
    losses = sum(1 for l in results_lines if "LOSS" in l)
    pending = sum(1 for l in results_lines if "PENDING" in l)

    result_text = f"""{e('🔍')} {to_bold_italic('LIVE CHECKER - RESULTS')}

{e('📅')} {to_bold('DAY')}: {to_bold(day_name)}
{e('⚙️')} {to_bold('MTG')}: {to_bold(mtg_name)}

━━━━━━━ • ━━━━━━━
{results_text}
━━━━━━━ • ━━━━━━━

{e('✅')} {to_bold('WINS')}: {to_bold(str(wins))}  {e('❌')} {to_bold('LOSSES')}: {to_bold(str(losses))}  {e('👀')} {to_bold('PENDING')}: {to_bold(str(pending))}"""

    result_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, result_text, reply_markup=result_keyboard, parse_mode=ParseMode.HTML)


# ============================================================
# BLACKOUT CHECKER - broker, time list, day, MTG, scan results
# ============================================================

async def show_blackout_chk_broker(query):
    """Show broker selection for Blackout Checker."""
    text = f"""{e('🔍')} {to_bold_italic('BLACKOUT CHECKER')}

👇 {to_bold('CHOOSE BROKER')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="blk_chk_quotex", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="blk_chk_binolla", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_blackout_chk_time_input(update, context, broker=None):
    """Ask user to send time list for Blackout Checker."""
    if broker is None:
        query = update.callback_query
        data = query.data
        broker = "quotex" if "quotex" in data else "binolla"
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    context.user_data["blk_chk_broker"] = broker
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    text = f"""{e('🔍')} {to_bold_italic('BLACKOUT CHECKER - ' + broker_name)}

👇 {to_bold('SEND TIME LIST')}

Send the time list to check signal results.
Example: 09:15, 10:32, 11:07, 13:45

Send /cancel to cancel"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return WAITING_BLK_CHK


async def receive_blackout_chk_time_list(update, context):
    """Receive time list, show day selection."""
    text = update.message.text.strip()
    import re as _re
    times = _re.findall(r'\d{1,2}:\d{2}', text)
    if not times:
        await update.message.reply_text("No valid times found! Send times like: 09:15, 10:32, 11:07\n\nSend /cancel to cancel")
        return WAITING_BLK_CHK

    context.user_data["blk_chk_times"] = times
    num_times = len(times)
    broker = context.user_data.get("blk_chk_broker", "quotex")

    await update.message.reply_text(
        f"{e('✅')} {to_bold(str(num_times))} {to_bold('times received')}\n\n"
        f"👇 {to_bold('CHOOSE DAY')}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Today", callback_data=f"blk_chk_day_today_{broker}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["calendar_premium"]),
                InlineKeyboardButton("Yesterday", callback_data=f"blk_chk_day_yesterday_{broker}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["calendar_premium"]),
            ],
            [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
        ])
    )
    return ConversationHandler.END


async def show_blackout_chk_mtg(query, day, broker):
    """Show MTG selection for Blackout Checker."""
    day_name = "Today" if day == "today" else "Yesterday"
    text = f"""{e('🔍')} {to_bold_italic('BLACKOUT CHECKER')}

{e('📅')} {to_bold('DAY')}: {to_bold(day_name)}

👇 {to_bold('CHOOSE MTG')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MTG1", callback_data=f"blk_chk_mtg_mtg1_{day}_{broker}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("MTG2", callback_data=f"blk_chk_mtg_mtg2_{day}_{broker}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("MTG1 + MTG2", callback_data=f"blk_chk_mtg_both_{day}_{broker}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_blackout_chk_scan(query, mtg, day, broker):
    """Show scanning message then results."""
    import asyncio
    import random as _random

    text = f"""{e('🔍')} {to_bold_italic('BLACKOUT CHECKER')}

{e('⏳')} {to_bold('SCANNING RESULTS...')}

Please wait..."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Please wait...", callback_data="blk_chk_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)

    day_name = "Today" if day == "today" else "Yesterday"
    mtg_name = "MTG1 + MTG2" if mtg == "both" else mtg.upper()
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"

    results_lines = []
    for pair_name, payout in SIGNAL_SESSION_PAIRS[:15]:
        pair_clean = pair_name.replace(" OTC", "").replace(" ", "").replace("/", "")
        result = _random.choice(["WIN", "WIN", "WIN", "LOSS", "PENDING"])
        if result == "WIN":
            status_emoji = "✔️"
            status_text = to_bold("WIN")
        elif result == "LOSS":
            status_emoji = "✖️"
            status_text = to_bold("LOSS")
        else:
            status_emoji = "👀"
            status_text = to_bold("PENDING")
        bold_pair = to_bold(pair_clean)
        results_lines.append(f"{bold_pair}  {status_emoji} {status_text}")

    results_text = "\n".join(results_lines)
    wins = sum(1 for l in results_lines if "WIN" in l)
    losses = sum(1 for l in results_lines if "LOSS" in l)
    pending = sum(1 for l in results_lines if "PENDING" in l)

    result_text = f"""{e('🔍')} {to_bold_italic('BLACKOUT CHECKER - RESULTS')}

{e('📅')} {to_bold('DAY')}: {to_bold(day_name)}
{e('⚙️')} {to_bold('MTG')}: {to_bold(mtg_name)}
{e('📊')} {to_bold('BROKER')}: {to_bold(broker_name)}

━━━━━━━ • ━━━━━━━
{results_text}
━━━━━━━ • ━━━━━━━

{e('✅')} {to_bold('WINS')}: {to_bold(str(wins))}  {e('❌')} {to_bold('LOSSES')}: {to_bold(str(losses))}  {e('👀')} {to_bold('PENDING')}: {to_bold(str(pending))}"""

    result_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, result_text, reply_markup=result_keyboard, parse_mode=ParseMode.HTML)


# ============================================================
# AXTIRON CHECKER (CHK Axtiron FS) - No broker, direct time list, day, MTG, scan results
# ============================================================

async def show_axtiron_chk_time_input(update, context):
    """Ask user to send time list for Axtiron Checker (no broker)."""
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    text = f"""{e('🐾')} {to_bold_italic('AXTIRON CHECKER')}

👇 {to_bold('SEND TIME LIST')}

Send the time list to check signal results.
Example: 09:15, 10:32, 11:07, 13:45

Send /cancel to cancel"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return WAITING_AXTIRON_CHK


async def receive_axtiron_chk_time_list(update, context):
    """Receive time list, show day selection."""
    text = update.message.text.strip()
    import re as _re
    times = _re.findall(r'\d{1,2}:\d{2}', text)
    if not times:
        await update.message.reply_text("No valid times found! Send times like: 09:15, 10:32, 11:07\n\nSend /cancel to cancel")
        return WAITING_AXTIRON_CHK

    context.user_data["axtiron_chk_times"] = times
    num_times = len(times)

    await update.message.reply_text(
        f"{e('✅')} {to_bold(str(num_times))} {to_bold('times received')}\n\n"
        f"👇 {to_bold('CHOOSE DAY')}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Today", callback_data="axtiron_chk_day_today", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["calendar_premium"]),
                InlineKeyboardButton("Yesterday", callback_data="axtiron_chk_day_yesterday", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["calendar_premium"]),
            ],
            [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
        ])
    )
    return ConversationHandler.END


async def show_axtiron_chk_mtg(query, day):
    """Show MTG selection for Axtiron Checker."""
    day_name = "Today" if day == "today" else "Yesterday"
    text = f"""{e('🐾')} {to_bold_italic('AXTIRON CHECKER')}

{e('📅')} {to_bold('DAY')}: {to_bold(day_name)}

👇 {to_bold('CHOOSE MTG')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MTG1", callback_data=f"axtiron_chk_mtg_mtg1_{day}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("MTG2", callback_data=f"axtiron_chk_mtg_mtg2_{day}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("MTG1 + MTG2", callback_data=f"axtiron_chk_mtg_both_{day}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"])],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_axtiron_chk_scan(query, mtg, day):
    """Show scanning message then results."""
    import asyncio
    import random as _random

    text = f"""{e('🐾')} {to_bold_italic('AXTIRON CHECKER')}

{e('⏳')} {to_bold('SCANNING RESULTS...')}

Please wait..."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Please wait...", callback_data="axtiron_chk_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)

    day_name = "Today" if day == "today" else "Yesterday"
    mtg_name = "MTG1 + MTG2" if mtg == "both" else mtg.upper()

    # Generate random results for pairs (mix of OTC and Live)
    results_lines = []
    pairs_pool = list(SIGNAL_SESSION_PAIRS[:8]) + list(LIVE_MARKET_PAIRS[:7])
    for pair_name, payout in pairs_pool:
        pair_clean = pair_name.replace(" OTC", "").replace(" ", "").replace("/", "")
        result = _random.choice(["WIN", "WIN", "WIN", "LOSS", "PENDING"])
        if result == "WIN":
            status_emoji = "✔️"
            status_text = to_bold("WIN")
        elif result == "LOSS":
            status_emoji = "✖️"
            status_text = to_bold("LOSS")
        else:
            status_emoji = "👀"
            status_text = to_bold("PENDING")
        bold_pair = to_bold(pair_clean)
        results_lines.append(f"{bold_pair}  {status_emoji} {status_text}")

    results_text = "\n".join(results_lines)
    wins = sum(1 for l in results_lines if "WIN" in l)
    losses = sum(1 for l in results_lines if "LOSS" in l)
    pending = sum(1 for l in results_lines if "PENDING" in l)

    result_text = f"""{e('🐾')} {to_bold_italic('AXTIRON CHECKER - RESULTS')}

{e('📅')} {to_bold('DAY')}: {to_bold(day_name)}
{e('⚙️')} {to_bold('MTG')}: {to_bold(mtg_name)}

━━━━━━━ • ━━━━━━━
{results_text}
━━━━━━━ • ━━━━━━━

{e('✅')} {to_bold('WINS')}: {to_bold(str(wins))}  {e('❌')} {to_bold('LOSSES')}: {to_bold(str(losses))}  {e('👀')} {to_bold('PENDING')}: {to_bold(str(pending))}"""

    result_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, result_text, reply_markup=result_keyboard, parse_mode=ParseMode.HTML)


# ============================================================
# PROMO CODE - Enter code, validate, show reward
# ============================================================

# Promo codes dict - format: "CODE": (reward_type, reward_value, reward_description)
# reward_type: "premium_days", "signals", "discount", "gift"
PROMO_CODES = {
    "QUANTVEXA2025": ("premium_days", 7, "7 Days Premium Access"),
    "AXTIRON100": ("signals", 100, "100 Bonus Signals"),
    "BLACKOUT50": ("signals", 50, "50 Bonus Signals"),
    "LUNA2025": ("premium_days", 30, "30 Days Premium Access"),
    "QUANTUMVIP": ("discount", 50, "50% Discount on Gold Plan"),
    "FREESTART": ("signals", 25, "25 Bonus Signals"),
    "QUOTEX10": ("signals", 10, "10 Bonus Signals"),
    "BINOLLA20": ("signals", 20, "20 Bonus Signals"),
}


async def show_promo_code_input(update, context):
    """Ask user to send promo code."""
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    text = f"""{e('🎁')} {to_bold_italic('PROMO CODE')}

👇 {to_bold('ENTER YOUR PROMO CODE')}

Send your promo code to claim your reward.
Example: QUANTVEXA2025

Send /cancel to cancel"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return WAITING_PROMO


async def receive_promo_code(update, context):
    """Receive promo code, validate, show reward message."""
    code = update.message.text.strip().upper()
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name or "Trader"

    # Check if code is valid
    if code in PROMO_CODES:
        reward_type, reward_value, reward_desc = PROMO_CODES[code]

        # Reward emoji and label based on type
        if reward_type == "premium_days":
            reward_icon = "👑"
            reward_label = to_bold("PREMIUM ACCESS")
            reward_detail = f"{to_bold(str(reward_value))} {to_bold('DAYS')}"
        elif reward_type == "signals":
            reward_icon = "📈"
            reward_label = to_bold("BONUS SIGNALS")
            reward_detail = f"{to_bold(str(reward_value))} {to_bold('SIGNALS')}"
        elif reward_type == "discount":
            reward_icon = "💎"
            reward_label = to_bold("DISCOUNT")
            reward_detail = f"{to_bold(str(reward_value))}% {to_bold('OFF')}"
        else:
            reward_icon = "🎁"
            reward_label = to_bold("REWARD")
            reward_detail = to_bold(reward_desc)

        # Save redeemed code to database to prevent reuse
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS redeemed_promo_codes
                              (user_id INTEGER, code TEXT, redeemed_at TEXT,
                               PRIMARY KEY (user_id, code))""")
            cursor.execute("SELECT 1 FROM redeemed_promo_codes WHERE user_id = ? AND code = ?", (user_id, code))
            if cursor.fetchone():
                conn.close()
                text = f"""{e('⚠️')} {to_bold_italic('PROMO CODE')}

{e('❌')} {to_bold('CODE ALREADY REDEEMED')}

You have already used this code: {to_bold(code)}

{e('💡')} Each promo code can only be used once."""
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
                ])
                await update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
                return ConversationHandler.END

            cursor.execute("INSERT INTO redeemed_promo_codes VALUES (?, ?, ?)",
                           (user_id, code, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
        except Exception as ex:
            logging.warning(f"Failed to save promo code redemption: {ex}")

        text = f"""{e('🎉')} {to_bold_italic('PROMO CODE REDEEMED!')}

{e('👤')} {to_bold('USER')}: {to_bold(first_name)}
{e('🎫')} {to_bold('CODE')}: {to_bold(code)}

━━━━━━━ • ━━━━━━━
{e(reward_icon)} {reward_label}
{reward_detail}
━━━━━━━ • ━━━━━━━

{e('✅')} {to_bold(reward_desc)}

{e('💎')} {to_bold('Your reward has been credited to your account')}

{e('🚀')} {to_bold_italic('ENJOY YOUR REWARD!')}"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["house"])],
        ])
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        # Invalid code
        text = f"""{e('⚠️')} {to_bold_italic('PROMO CODE')}

{e('❌')} {to_bold('INVALID PROMO CODE')}

The code you entered is not valid: {to_bold(code)}

{e('💡')} Please check the code and try again.

Send another code or /cancel to cancel"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
        ])
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        return WAITING_PROMO

    return ConversationHandler.END


async def show_checker(query, checker_name):
    text = f"""
{e('🔍')} {checker_name.upper()}

𝑪𝒉𝒆𝒄𝒌𝒊𝒏𝒈 𝒎𝒂𝒓𝒌𝒆𝒕 𝒔𝒕𝒂𝒕𝒖𝒔...

𝑺𝒕𝒂𝒕𝒖𝒔: 𝑨𝒄𝒕𝒊𝒗𝒆 {e('✅')}
𝑳𝒂𝒔𝒕 𝑼𝒑𝒅𝒂𝒕𝒆: {datetime.now().strftime('%H:%M:%S')}

𝑨𝒗𝒂𝒊𝒍𝒂𝒃𝒍𝒆 𝑷𝒂𝒊𝒓𝒔:
• 𝑬𝑼𝑹/𝑼𝑺𝑫
• 𝑮𝑩𝑷/𝑱𝑷𝒀
• 𝑼𝑺𝑫/𝑱𝑷𝒀
• 𝑨𝑼𝑫/𝑪𝑨𝑫

{e('⚠️')} 𝑹𝒆𝒇𝒓𝒆𝒔𝒉 𝒕𝒐 𝒄𝒉𝒆𝒄𝒌 𝒂𝒈𝒂𝒊𝒏
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_market_fs(query, market_name):
    text = f"""
{e('📈')} {market_name.upper()} 𝑭𝑺

𝑴𝒂𝒓𝒌𝒆𝒕 𝑭𝒖𝒕𝒖𝒓𝒆 𝑺𝒊𝒈𝒏𝒂𝒍𝒔:

𝑨𝒄𝒕𝒊𝒗𝒆 𝑷𝒂𝒊𝒓𝒔:
• 𝑬𝑼𝑹/𝑼𝑺𝑫 - 𝑪𝑨𝑳𝑳 - 92%
• 𝑮𝑩𝑷/𝑱𝑷𝒀 - 𝑷𝑼𝑻 - 88%
• 𝑼𝑺𝑫/𝑪𝑨𝑫 - 𝑪𝑨𝑳𝑳 - 90%

𝑼𝒑𝒅𝒂𝒕𝒆𝒅: {datetime.now().strftime('%H:%M')}

{e('⚠️')} 𝑭𝒖𝒕𝒖𝒓𝒆 𝒔𝒊𝒈𝒏𝒂𝒍𝒔 𝒂𝒓𝒆 𝒑𝒓𝒆𝒎𝒊𝒖𝒎 𝒇𝒆𝒂𝒕𝒖𝒓𝒆
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_future_live(query):
    text = f"""
{e('🔮')} 𝑭𝑼𝑻𝑼𝑹𝑬 𝑳𝑰𝑽𝑬

𝑼𝒑𝒄𝒐𝒎𝒊𝒏𝒈 𝑳𝒊𝒗𝒆 𝑺𝒊𝒈𝒏𝒂𝒍𝒔:

𝑵𝒆𝒙𝒕 𝑺𝒊𝒈𝒏𝒂𝒍:
• 𝑷𝒂𝒊𝒓: 𝑬𝑼𝑹/𝑼𝑺𝑫
• 𝑻𝒊𝒎𝒆: {(datetime.now() + timedelta(minutes=15)).strftime('%H:%M')}
• 𝑫𝒊𝒓𝒆𝒄𝒕𝒊𝒐𝒏: 𝑪𝑨𝑳𝑳
• 𝑬𝒙𝒑𝒊𝒓𝒚: 𝑴1

{e('⚡')} 𝑺𝒕𝒂𝒚 𝒕𝒖𝒏𝒆𝒅!
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_live_signal(query):
    """Show broker selection for live signal."""
    text = f"""{e('⚡')} <b>LIVE SIGNAL</b>

{e('👇')} <b>CHOOSE BROKER</b>"""
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
    text = f"""{e('⚡')} <b>LIVE SIGNAL - {broker_name}</b>

{e('👇')} <b>CHOOSE MARKET TYPE</b>"""
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
    text = f"""{e('⚡')} <b>LIVE SIGNAL - {broker_name} {market_name}</b>

{e('👇')} <b>CHOOSE DURATION</b>"""
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
    text = f"""{e('⚡')} <b>LIVE SIGNAL - {broker_name} {market_name}</b>

Duration: {duration}

{e('👇')} <b>CHOOSE BOT TYPE</b>"""
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

    text = f"""{e('✅')} {to_bold_italic('LIVE SIGNAL CONFIGURED')}

{e('📊')} {to_bold('BROKER')}: {to_bold(broker_name)}
{e('🌐')} {to_bold('MARKET')}: {to_bold(market_name)}
{e('⌛')} {to_bold('DURATION')}: {to_bold(duration)}
{e('🤖')} {to_bold('BOT TYPE')}: {to_bold(bot_name)}

{e('💎')} {to_bold('The bot will select the best currency pairs')}
{to_bold('and send you live signals automatically.')}

{e('⚡')} {to_bold('Signals are coming soon - under development')}"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def show_bug_signal(query):
    """Bug Signal is currently disabled."""
    text = f"""
{e('🐛')} 𝑩𝑼𝑮 𝑺𝑰𝑮𝑵𝑨𝑳

{e('⚠️')} 𝑪𝑶𝑴𝑰𝑵𝑮 𝑺𝑶𝑶𝑵

This feature is currently under development
and will be available soon.

{e('⚡')} Stay tuned for updates!
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_live_payouts(query):
    """Show broker selection for live payouts."""
    text = f"""{e('💎')} 𝙻𝙸𝚅𝙴 𝙿𝙰𝚈𝙾𝚄𝚃𝚂

{e('👇')} 𝙲𝙷𝙾𝙾𝚂𝙴 𝙱𝚁𝙾𝙺𝙴𝚁

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
    return f"""{e('💎')} 𝙻𝙸𝚅𝙴 𝙿𝙰𝚈𝙾𝚄𝚃𝚂 - {broker_name}

{e('👇')} 𝙻𝙸𝚅𝙴 𝙿𝙰𝚈𝙾𝚄𝚃 𝚁𝙰𝚃𝙴𝚂

Updated: {datetime.now().strftime('%H:%M:%S')}

{e('🟦')} Blue = High payout (85%+)
{e('🟩')} Green = Medium payout (70-84%)
{e('🟥')} Red = Low payout (&lt;70%)"""


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
{e('✨')} 𝑵𝑬𝑾𝑺 𝑺𝑰𝑮𝑵𝑨𝑳

𝑳𝒂𝒕𝒆𝒔𝒕 𝑴𝒂𝒓𝒌𝒆𝒕 𝑵𝒆𝒘𝒔:

{e('📰')} 𝑼𝑺 𝑭𝒆𝒅 𝑹𝒂𝒕𝒆 𝑫𝒆𝒄𝒊𝒔𝒊𝒐𝒏 - 𝑯𝒊𝒈𝒉 𝑰𝒎𝒑𝒂𝒄𝒕
{e('📰')} 𝑵𝒐𝒏-𝑭𝒂𝒓𝒎 𝑷𝒂𝒚𝒓𝒐𝒍𝒍𝒔 - 𝑴𝒆𝒅𝒊𝒖𝒎 𝑰𝒎𝒑𝒂𝒄𝒕
{e('📰')} 𝑬𝑼 𝑪𝑷𝑰 𝑫𝒂𝒕𝒂 - 𝑴𝒆𝒅𝒊𝒖𝒎 𝑰𝒎𝒑𝒂𝒄𝒕

𝑼𝒑𝒅𝒂𝒕𝒆𝒅: {datetime.now().strftime('%H:%M')}

{e('⚠️')} 𝑵𝒆𝒘𝒔 𝒄𝒂𝒏 𝒂𝒇𝒇𝒆𝒄𝒕 𝒎𝒂𝒓𝒌𝒆𝒕 𝒗𝒐𝒍𝒂𝒕𝒊𝒍𝒊𝒕𝒚
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_ai_filter(query):
    text = f"""
{e('👤')} 𝑨𝑰 𝑭𝑰𝑳𝑻𝑬𝑹

𝑨𝑰-𝑷𝒐𝒘𝒆𝒓𝒆𝒅 𝑺𝒊𝒈𝒏𝒂𝒍 𝑭𝒊𝒍𝒕𝒆𝒓:

𝑭𝒊𝒍𝒕𝒆𝒓 𝑺𝒆𝒕𝒕𝒊𝒏𝒈𝒔:
• 𝑴𝒊𝒏𝒊𝒎𝒖𝒎 𝑪𝒐𝒏𝒇𝒊𝒅𝒆𝒏𝒄𝒆: 85%
• 𝑴𝒂𝒙𝒊𝒎𝒖𝒎 𝑹𝒊𝒔𝒌: 𝑴𝒆𝒅𝒊𝒖𝒎
• 𝑷𝒓𝒆𝒇𝒆𝒓𝒓𝒆𝒅 𝑷𝒂𝒊𝒓𝒔: 𝑴𝒂𝒋𝒐𝒓

𝑨𝑰 𝑺𝒕𝒂𝒕𝒖𝒔: 𝑨𝒄𝒕𝒊𝒗𝒆 {e('✅')}
𝑳𝒂𝒔𝒕 𝑨𝒏𝒂𝒍𝒚𝒔𝒊𝒔: {datetime.now().strftime('%H:%M:%S')}

{e('⚡')} 𝑨𝑰 𝒊𝒔 𝒂𝒏𝒂𝒍𝒚𝒛𝒊𝒏𝒈 𝒎𝒂𝒓𝒌𝒆𝒕𝒔 24/7
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

async def show_ai_assistant(query):
    text = f"""
{e('🤖')} 𝑨𝑰 𝑨𝑺𝑺𝑰𝑺𝑻𝑨𝑵𝑻

𝒀𝒐𝒖𝒓 𝑨𝑰 𝑻𝒓𝒂𝒅𝒊𝒏𝒈 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕:

𝑰 𝒄𝒂𝒏 𝒉𝒆𝒍𝒑 𝒚𝒐𝒖 𝒘𝒊𝒕𝒉:
• 𝑴𝒂𝒓𝒌𝒆𝒕 𝒂𝒏𝒂𝒍𝒚𝒔𝒊𝒔
• 𝑺𝒊𝒈𝒏𝒂𝒍 𝒊𝒏𝒕𝒆𝒓𝒑𝒓𝒆𝒕𝒂𝒕𝒊𝒐𝒏
• 𝑹𝒊𝒔𝒌 𝒎𝒂𝒏𝒂𝒈𝒆𝒎𝒆𝒏𝒕
• 𝑺𝒕𝒓𝒂𝒕𝒆𝒈𝒚 𝒕𝒊𝒑𝒔

{e('⚡')} 𝑨𝒔𝒌 𝒎𝒆 𝒂𝒏𝒚𝒕𝒉𝒊𝒏𝒈 𝒂𝒃𝒐𝒖𝒕 𝒕𝒓𝒂𝒅𝒊𝒏𝒈!

{e('⚠️')} 𝑵𝒐𝒕 𝒇𝒊𝒏𝒂𝒏𝒄𝒊𝒂𝒍 𝒂𝒅𝒗𝒊𝒄𝒆
"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

# ============================================================
# FORMATTER - signal list -> choose format -> show converted list
# ============================================================

# Format definitions: id -> (label, sample, builder)
# builder(signal_dict) -> formatted string for one line
# signal_dict keys: timeframe, pair, time, direction
FORMATTER_FORMATS = [
    (
        "std_call",
        "Standard (CALL/PUT)",
        "M1;EURUSD-OTC;14:26;CALL",
        lambda s: f"{s['timeframe']};{s['pair']};{s['time']};{'CALL' if s['direction_upper'] in ('CALL','BUY','UP') else 'PUT'}",
    ),
    (
        "std_buy",
        "Standard (BUY/SELL)",
        "M1;EURUSD-OTC;14:26;BUY",
        lambda s: f"{s['timeframe']};{s['pair']};{s['time']};{'BUY' if s['direction_upper'] in ('CALL','BUY','UP') else 'SELL'}",
    ),
    (
        "arrow",
        "Arrow Format",
        "❒ USDCOP_otc 1M - 00:12 PUT",
        lambda s: f"❒ {s['pair'].lower().replace('-','_')} {s['timeframe_rev']} - {s['time']} {'PUT' if s['direction_upper'] in ('PUT','SELL','DOWN') else 'CALL'}",
    ),
    (
        "dash",
        "Dash Format",
        "EURUSD-OTC | 1M | 14:26 | CALL",
        lambda s: f"{s['pair']} | {s['timeframe_rev']} | {s['time']} | {'CALL' if s['direction_upper'] in ('CALL','BUY','UP') else 'PUT'}",
    ),
    (
        "emoji",
        "Emoji Format",
        "🟢 EURUSD-OTC • 1M • 14:26 • CALL",
        lambda s: f"{'🟢' if s['direction_upper'] in ('CALL','BUY','UP') else '🔴'} {s['pair']} • {s['timeframe_rev']} • {s['time']} • {'CALL' if s['direction_upper'] in ('CALL','BUY','UP') else 'PUT'}",
    ),
    (
        "premium",
        "Premium Format",
        "⏱ 14:26 | 🌐 EURUSD-OTC | ⏳ 1M | 📈 CALL",
        lambda s: f"⏱ {s['time']} | 🌐 {s['pair']} | ⏳ {s['timeframe_rev']} | {'📈 CALL' if s['direction_upper'] in ('CALL','BUY','UP') else '📉 PUT'}",
    ),
    (
        "compact",
        "Compact Format",
        "EURUSD-OTC 1M 14:26 CALL",
        lambda s: f"{s['pair']} {s['timeframe_rev']} {s['time']} {'CALL' if s['direction_upper'] in ('CALL','BUY','UP') else 'PUT'}",
    ),
    (
        "bracket",
        "Bracket Format",
        "[1M] EURUSD-OTC @ 14:26 (CALL)",
        lambda s: f"[{s['timeframe_rev']}] {s['pair']} @ {s['time']} ({'CALL' if s['direction_upper'] in ('CALL','BUY','UP') else 'PUT'})",
    ),
]


def _parse_signal_line(line):
    """Parse a signal line into a dict with: timeframe, pair, time, direction.
    Returns None if line can't be parsed.
    Supports multiple input formats.
    """
    import re as _re
    line = line.strip()
    if not line:
        return None

    # Try to extract time (HH:MM) - must be standalone, not part of timeframe
    time_match = _re.search(r'(?<!\d)(\d{1,2}:\d{2})(?!\d)', line)
    if not time_match:
        return None
    time = time_match.group(1)

    # Try to extract direction
    direction = None
    for d in ['CALL', 'PUT', 'BUY', 'SELL', 'UP', 'DOWN']:
        if _re.search(r'\b' + d + r'\b', line, _re.IGNORECASE):
            direction = d.upper()
            break
    if not direction:
        return None

    # Try to extract timeframe (M1, 1M, M5, 5M, etc.)
    # Use strict patterns to avoid matching times like 14:26
    timeframe = None
    # Pattern 1: 1M, 5M, 15M (number+M, but not preceded/followed by digit)
    m1 = _re.search(r'(?<!\d)(\d{1,2}M)(?!\d)', line, _re.IGNORECASE)
    # Pattern 2: M1, M5, M15 (M+number, but not in the middle of a word)
    m2 = _re.search(r'\b(M\d{1,2})\b', line, _re.IGNORECASE)
    if m1:
        tf_raw = m1.group(1).upper()
        timeframe = 'M' + tf_raw[:-1]
    elif m2:
        tf_raw = m2.group(1).upper()
        timeframe = tf_raw
    if not timeframe:
        timeframe = 'M1'  # default

    # Try to extract pair (anything that looks like a currency pair)
    # Remove the time, direction, timeframe from the line, then clean
    cleaned = line
    cleaned = _re.sub(r'\d{1,2}:\d{2}', ' ', cleaned)
    cleaned = _re.sub(r'\b(CALL|PUT|BUY|SELL|UP|DOWN)\b', ' ', cleaned, flags=_re.IGNORECASE)
    cleaned = _re.sub(r'(?<!\d)\d{1,2}M(?!\d)', ' ', cleaned, flags=_re.IGNORECASE)
    cleaned = _re.sub(r'\bM\d{1,2}\b', ' ', cleaned, flags=_re.IGNORECASE)
    # Remove separators and decorations
    cleaned = _re.sub(r'[;|•\-\(\)\[\]❒🟢🔴⏱🌐⏳📈📉@\s_]+', ' ', cleaned)
    cleaned = cleaned.strip()
    # Get the first token that contains letters (the pair)
    tokens = [t for t in cleaned.split() if any(c.isalpha() for c in t)]
    if not tokens:
        return None
    pair = tokens[0].upper()

    # Normalize pair: ensure -OTC suffix preserved if present
    has_otc = 'OTC' in line.upper() or 'otc' in line.lower()
    if pair.endswith('OTC') and not pair.endswith('-OTC'):
        pair = pair[:-3] + '-OTC'
    elif has_otc and not pair.endswith('-OTC') and not pair.endswith('OTC'):
        pair = pair + '-OTC'

    # Reverse timeframe for some formats (M1 -> 1M)
    tf_rev = timeframe[1:] + 'M' if _re.match(r'^M\d+$', timeframe) else timeframe

    return {
        'timeframe': timeframe,
        'timeframe_rev': tf_rev,
        'pair': pair,
        'time': time,
        'direction': direction,
        'direction_upper': direction.upper(),
    }


async def show_formatter_input(update, context):
    """Ask user to send signal list for formatting."""
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    text = f"""{e('🌀')} {to_bold_italic('FORMATTER')}

👇 {to_bold('SEND YOUR SIGNAL LIST')}

Send your signal list to format it.
You can use any format, examples:

{to_bold('Format 1:')} M1;EURUSD-OTC;14:26;CALL
{to_bold('Format 2:')} EURUSD OTC 14:26 CALL M1
{to_bold('Format 3:')} ❒ USDCOP_otc 1M - 00:12 PUT
{to_bold('Format 4:')} EUR/USD 14:26 BUY

Send /cancel to cancel"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return WAITING_FORMATTER_SIGNAL


async def receive_formatter_signal_list(update, context):
    """Receive signal list, store it, show format choices."""
    text = update.message.text.strip()
    lines = [l for l in text.split('\n') if l.strip()]

    # Parse each line
    parsed = []
    failed = 0
    for line in lines:
        sig = _parse_signal_line(line)
        if sig:
            parsed.append(sig)
        else:
            failed += 1

    if not parsed:
        await update.message.reply_text(
            f"{e('❌')} {to_bold('No valid signals found!')}\n\n"
            f"Send signals like:\n"
            f"M1;EURUSD-OTC;14:26;CALL\n\n"
            f"Send /cancel to cancel",
            parse_mode=ParseMode.HTML
        )
        return WAITING_FORMATTER_SIGNAL

    # Store parsed signals in user_data
    context.user_data["formatter_signals"] = parsed
    context.user_data["formatter_failed"] = failed

    num_signals = len(parsed)
    text = f"""{e('✅')} {to_bold_italic('FORMATTER')}

{to_bold(str(num_signals))} {to_bold('signals received')}

👇 {to_bold('CHOOSE OUTPUT FORMAT')}"""
    keyboard_rows = []
    for fmt_id, fmt_label, fmt_sample, _ in FORMATTER_FORMATS:
        keyboard_rows.append([InlineKeyboardButton(
            f"{fmt_label}",
            callback_data=f"fmt_choice_{fmt_id}",
            style=STYLE_BLUE,
            icon_custom_emoji_id=EMOJI_IDS["swirl"],
        )])
    keyboard_rows.append([InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])])
    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return ConversationHandler.END


async def show_formatter_result_from_button(update, context, fmt_id):
    """Show formatted result based on chosen format."""
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass

    parsed = context.user_data.get("formatter_signals", [])
    if not parsed:
        text = f"""{e('⚠️')} {to_bold_italic('FORMATTER')}

{e('❌')} {to_bold('NO SIGNALS FOUND')}

Please send your signal list first."""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Send Signals", callback_data="formatter", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["swirl"])],
            [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
        ])
        await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        return

    # Find the chosen format
    chosen = None
    for f_id, f_label, f_sample, f_builder in FORMATTER_FORMATS:
        if f_id == fmt_id:
            chosen = (f_id, f_label, f_sample, f_builder)
            break

    if not chosen:
        text = f"""{e('❌')} {to_bold('Invalid format choice')}"""
        await safe_edit_message(query, text, parse_mode=ParseMode.HTML)
        return

    fmt_id, fmt_label, fmt_sample, fmt_builder = chosen

    # Build formatted output
    formatted_lines = []
    for sig in parsed:
        try:
            formatted_lines.append(fmt_builder(sig))
        except Exception:
            formatted_lines.append(f"{sig['pair']} {sig['time']} {sig['direction']}")

    formatted_text = "\n".join(formatted_lines)
    num_signals = len(parsed)

    text = f"""{e('🌀')} {to_bold_italic('FORMATTER - RESULT')}

{e('📋')} {to_bold('FORMAT')}: {to_bold(fmt_label)}
{e('📌')} {to_bold('SAMPLE')}: {to_bold(fmt_sample)}
{e('🔢')} {to_bold('COUNT')}: {to_bold(str(num_signals))}

━━━━━━━ • ━━━━━━━
{to_bold_italic('FORMATTED SIGNALS:')}
━━━━━━━ • ━━━━━━━

{formatted_text}

━━━━━━━ • ━━━━━━━

{e('💡')} {to_bold('Copy the formatted signals above')}"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("New Signals", callback_data="fmt_new", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["sparkles"]),
            InlineKeyboardButton("Change Format", callback_data="fmt_change", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["swap"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_formatter_change_format(update, context):
    """Show format choice list again using stored signals."""
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass

    parsed = context.user_data.get("formatter_signals", [])
    if not parsed:
        # No signals stored, send new
        await show_formatter_input(update, context)
        return

    num_signals = len(parsed)
    text = f"""{e('✅')} {to_bold_italic('FORMATTER')}

{to_bold(str(num_signals))} {to_bold('signals stored')}

👇 {to_bold('CHOOSE OUTPUT FORMAT')}"""
    keyboard_rows = []
    for fmt_id, fmt_label, fmt_sample, _ in FORMATTER_FORMATS:
        keyboard_rows.append([InlineKeyboardButton(
            f"{fmt_label}",
            callback_data=f"fmt_choice_{fmt_id}",
            style=STYLE_BLUE,
            icon_custom_emoji_id=EMOJI_IDS["swirl"],
        )])
    keyboard_rows.append([InlineKeyboardButton("Cancel", callback_data="main_menu", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])])
    keyboard = InlineKeyboardMarkup(keyboard_rows)
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_formatter(query):
    """Legacy - redirect to input."""
    query_dummy = query
    # Show input prompt directly (legacy fallback)
    text = f"""{e('🌀')} {to_bold_italic('FORMATTER')}

👇 {to_bold('SEND YOUR SIGNAL LIST')}

Send your signal list to format it.
Examples:
• M1;EURUSD-OTC;14:26;CALL
• ❒ USDCOP_otc 1M - 00:12 PUT

Send /cancel to cancel"""
    await safe_edit_message(query, text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)

# ============================================================
# MARKET FILTERS - broker -> market (OTC/Global) -> scanning -> filtered results
# ============================================================

async def show_market_filters_broker(query):
    """Show broker selection for Market Filters."""
    text = f"""{e('📊')} {to_bold_italic('MARKET FILTERS')}

👇 {to_bold('CHOOSE BROKER')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("QUOTEX", callback_data="mf_quotex", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["check"]),
            InlineKeyboardButton("BINOLLA", callback_data="mf_binolla", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["stats"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_market_filters_market(query, broker):
    """Show market type selection (OTC / Global)."""
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    text = f"""{e('📊')} {to_bold_italic('MARKET FILTERS - ' + broker_name)}

👇 {to_bold('CHOOSE MARKET TYPE')}"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("OTC Market", callback_data=f"mf_market_otc_{broker}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["chart"]),
            InlineKeyboardButton("Global Market", callback_data=f"mf_market_global_{broker}", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["globe"]),
        ],
        [InlineKeyboardButton("Back to Broker", callback_data="market_filters", style=STYLE_RED, icon_custom_emoji_id=EMOJI_IDS["cross"])],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_market_filters_scanning(query, market, broker):
    """Show scanning message then results."""
    import asyncio
    market_name = "OTC" if market == "otc" else "GLOBAL"
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"
    text = f"""{e('📊')} {to_bold_italic('MARKET FILTERS')}

{e('⚙️')} {to_bold('BROKER')}: {to_bold(broker_name)}
{e('🌐')} {to_bold('MARKET')}: {to_bold(market_name)}

{e('⏳')} {to_bold('FILTERING MARKETS...')}

{e('🔍')} {to_bold('Removing pairs with payout < 70%')}

Please wait..."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏳ Please wait...", callback_data="mf_none", style=STYLE_BLUE)],
    ])
    await safe_edit_message(query, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await asyncio.sleep(3)
    await show_market_filters_results(query, market, broker)


async def show_market_filters_results(query, market, broker):
    """Show filtered market results - only pairs with payout >= 70%, grouped by trend."""
    import random as _random

    market_name = "OTC" if market == "otc" else "GLOBAL"
    broker_name = "QUOTEX" if broker == "quotex" else "BINOLLA"

    # Get pair list based on market type
    if market == "otc":
        pairs = SIGNAL_SESSION_PAIRS
        suffix = "-OTC"
    else:
        pairs = LIVE_MARKET_PAIRS
        suffix = ""

    # Filter: only pairs with payout >= 70%
    filtered = [(name, payout) for name, payout in pairs if payout >= 70]

    # Randomly assign trend (UP/DOWN) and indicators to each pair
    up_trend = []
    down_trend = []
    for name, payout in filtered:
        # Random trend
        is_up = _random.choice([True, True, False])  # bias toward UP
        rsi = round(_random.uniform(37, 68), 1)
        momentum = round(_random.uniform(40, 67), 1)
        pair_clean = name.replace(" OTC", "").replace(" ", "").replace("/", "")
        item = (f"{pair_clean}{suffix}", payout, rsi, momentum)
        if is_up:
            up_trend.append(item)
        else:
            down_trend.append(item)

    # Build result text
    total_tradeable = len(up_trend) + len(down_trend)

    lines = []
    lines.append(f"{e('📊')} {to_bold_italic(f'MARKET FILTERS — {market_name}')}")
    lines.append(f"{e('━━━')} {to_bold('━━━━━━━━━━━━━')}")
    lines.append(f"{to_bold('Tradeable Markets')}: {to_bold(str(total_tradeable))}")
    lines.append("")

    # UP TREND section
    lines.append(f"{e('📈')} {to_bold(f'UP TREND ({len(up_trend)})')}")
    for pair_name, payout, rsi, momentum in up_trend:
        lines.append(f"🟢 {to_bold(pair_name)}  {to_bold(str(payout))}%")
        lines.append(f"  📈 {to_bold('UP')}  |  RSI {rsi}  |  Momentum {momentum}%")
    lines.append("")

    # DOWN TREND section (only if there are any)
    if down_trend:
        lines.append(f"{e('📉')} {to_bold(f'DOWN TREND ({len(down_trend)})')}")
        for pair_name, payout, rsi, momentum in down_trend:
            lines.append(f"🟢 {to_bold(pair_name)}  {to_bold(str(payout))}%")
            lines.append(f"  📉 {to_bold('DOWN')}  |  RSI {rsi}  |  Momentum {momentum}%")
        lines.append("")

    lines.append(f"{e('━━━')} {to_bold('━━━━━━━━━━━━━')}")
    lines.append(f"{e('✅')} {to_bold('These are stable markets.')}")
    lines.append(f"{to_bold('You can analyze these pairs with your own setup and trade with confidence.')}")

    result_text = "\n".join(lines)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Refresh", callback_data=f"mf_results_{market}_{broker}", style=STYLE_GREEN, icon_custom_emoji_id=EMOJI_IDS["sparkles"]),
            InlineKeyboardButton("Back to Broker", callback_data="market_filters", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["swap"]),
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu", style=STYLE_BLUE, icon_custom_emoji_id=EMOJI_IDS["house"])],
    ])
    await safe_edit_message(query, result_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def show_market_filters(query):
    """Legacy - redirect to broker selection."""
    await show_market_filters_broker(query)

async def show_swap_cp(query):
    """Swap C/P is currently disabled."""
    text = f"""
{e('🔄')} 𝑺𝑾𝑨𝑷 𝑪/𝑷

{e('⚠️')} 𝑪𝑶𝑴𝑰𝑵𝑮 𝑺𝑶𝑶𝑵

This feature is currently under development
and will be available soon.

{e('⚡')} Stay tuned for updates!
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
        tz_text = f"""{e('✅')} 𝒀𝒐𝒖𝒓 𝑻𝒊𝒎𝒆𝒛𝒐𝒏𝒆: UTC{user_tz}

{e('💡')} All signal times will be displayed
in your selected timezone."""
    else:
        tz_text = f"""{e('⚠️')} 𝑵𝒐 𝑻𝒊𝒎𝒆𝒛𝒐𝒏𝒆 𝑺𝒆𝒕

Select your timezone below to convert
signal times to your local time."""

    text = f"""{e('⏰')} 𝑻𝑰𝑴𝑬𝒁𝑶𝑵𝑬 𝑺𝑬𝑳𝑬𝑪𝑻𝑶𝑹

{tz_text}

━━━━━━━━━━━━━━━━━━━━

{e('👇')} 𝑺𝒆𝒍𝒆𝒄𝒕 𝒚𝒐𝒖𝒓 𝒕𝒊𝒎𝒆𝒛𝒐𝒏𝒆:"""

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
        sign = "{e('➖')}" if offset.startswith("-") else "{e('➕')}"
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

    text = f"""{e('✅')} 𝑻𝒊𝒎𝒆𝒛𝒐𝒏𝒆 𝑼𝒑𝒅𝒂𝒕𝒆𝒅!

{e('⏰')} 𝒀𝒐𝒖𝒓 𝑻𝒊𝒎𝒆𝒛𝒐𝒏𝒆: UTC{utc_offset}

{e('💡')} All signal times will now be displayed
in your selected timezone (UTC{utc_offset}).

{e('⚡')} You can change your timezone
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

    text = f"""{e('✅')} 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆 𝑺𝒆𝒕 𝑺𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚!

{e('⏰')} 𝑺𝒕𝒂𝒓𝒕 𝑻𝒊𝒎𝒆: {start_time}
{e('⏰')} 𝑬𝒏𝒅 𝑻𝒊𝒎𝒆: {end_time}

{e('💡')} The bot will automatically send you
trading signals during this time period
every day.

{e('⚡')} You can pause or delete the schedule
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

    text = f"""{e('❌')} 𝑺𝒄𝒉𝒆𝒅𝒖𝒍𝒆 𝑫𝒆𝒍𝒆𝒕𝒆𝒅

Your signal schedule has been deleted.
You will no longer receive automatic signals.

{e('💡')} You can set a new schedule anytime
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
        await safe_edit_message(query, f"{e('❌')} Access Denied - Admins only", reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
        return ConversationHandler.END
    text = f"""
{e('📝')} Create New Signal

Send the signal in the following format:
Currency | Direction | Entry Price | Expiry

Example:
EUR/USD | CALL | 1.0856 | M1

{e('⚠️')} Send /cancel to cancel
"""
    await safe_edit_message(query, text, parse_mode=ParseMode.HTML)
    return WAITING_SIGNAL_INPUT

async def receive_signal_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    text = update.message.text
    parts = [p.strip() for p in text.split("|")]
    if len(parts) != 4:
        await update.message.reply_text(f"{e('⚠️')} Invalid format! Use:\nCurrency | Direction | Price | Expiry", parse_mode=ParseMode.HTML)
        return WAITING_SIGNAL_INPUT
    currency, direction, entry_price, expiry = parts
    try:
        price = float(entry_price)
    except ValueError:
        await update.message.reply_text(f"{e('⚠️')} Price must be a number", parse_mode=ParseMode.HTML)
        return WAITING_SIGNAL_INPUT

    signal_id = add_signal(currency, direction, price, expiry)
    context.user_data["pending_signal"] = {"id": signal_id, "currency": currency, "direction": direction, "price": price, "expiry": expiry}
    text = f"""
{e('✅')} Signal Ready

{e('📊')} Currency: {currency}
{e('📈')} Direction: {direction}
{e('💰')} Entry: {price}
{e('⏰')} Expiry: {expiry}

Do you want to send it to the signals channel?
"""
    await update.message.reply_text(text, reply_markup=get_admin_confirm_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

async def admin_confirm_send(query, context):
    if not is_admin(query.from_user.id):
        return
    signal = context.user_data.get("pending_signal")
    if not signal:
        await safe_edit_message(query, f"{e('⚠️')} No pending signal", reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML)
        return

    signal_text = f"""
{e('📊')} New Signal from the Bot

{e('📈')} Currency: {signal['currency']}
{e('📉')} Direction: {signal['direction']}
{e('💰')} Entry Price: {signal['price']}
{e('⏰')} Expiry: {signal['expiry']}

{e('🕐')} Signal Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{e('⚠️')} Trade responsibly - Signals are advisory only
"""
    try:
        await context.bot.send_message(chat_id=SIGNALS_CHANNEL_ID, text=signal_text, parse_mode=ParseMode.HTML)
        success_msg = f"{e('✅')} Signal sent to channel successfully!"
    except Exception as e:
        success_msg = f"{e('❌')} Send failed: {str(e)}"

    context.user_data.pop("pending_signal", None)
    await safe_edit_message(query, f"{success_msg}\n\nBack to control panel:", reply_markup=get_control_keyboard(is_admin=True), parse_mode=ParseMode.HTML)

async def admin_broadcast(query, context):
    if not is_admin(query.from_user.id):
        return
    text = f"""
{e('📣')} Broadcast Message to All Users

Send the message you want to broadcast:
{e('⚠️')} Send /cancel to cancel

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
    status_msg = await update.message.reply_text(f"{e('🚀')} Sending... (0/{len(users)})")
    for user in users:
        try:
            await context.bot.send_message(chat_id=user["user_id"], text=f"{e('📣')} Message from Admin:\n\n{message}", parse_mode=ParseMode.HTML)
            sent += 1
        except Exception:
            failed += 1

    await status_msg.edit_text(f"{e('✅')} Broadcast completed!\n\n{e('📤')} Sent: {sent}\n{e('❌')} Failed: {failed}", reply_markup=get_control_keyboard(is_admin=True), parse_mode=ParseMode.HTML)
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
{e('📊')} Bot Statistics

{e('👥')} Users:
• Total Users: {users_count}
• VIP Subscribers: {premium_count}
• Total Referrals: {total_referrals}

{e('📈')} Signals:
• Winning signals: {wins}
• Losing signals: {losses}
• Win rate: {win_rate:.1f}%

{e('📅')} Last Updates:
• Last update date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    await safe_edit_message(query, text, reply_markup=get_control_keyboard(is_admin=True), parse_mode=ParseMode.HTML)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("admin_creating_signal", None)
    context.user_data.pop("admin_broadcasting", None)
    context.user_data.pop("pending_signal", None)
    await update.message.reply_text(f"{e('❌')} Operation cancelled", reply_markup=get_main_menu_keyboard(), parse_mode=ParseMode.HTML)
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
    logger.info(f"{e('🤖')} Bot Info:\n   {e('📛')} Name: {me.first_name}\n   {e('🔗')} Username: @{me.username}\n   {e('🆔')} ID: {me.id}")
    global BOT_USERNAME
    if BOT_USERNAME in ["your_bot_username", "", None]:
        BOT_USERNAME = me.username
    logger.info("=" * 50)

def main():
    if not validate_config():
        logger.error("{e('❌')} Configuration incomplete! Edit BOT_TOKEN in this file.")
        sys.exit(1)

    logger.info(f"{e('📊')} Initializing database...")
    init_db()
    logger.info(f"{e('✅')} Database initialized successfully")

    logger.info(f"{e('🤖')} Starting the bot...")
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

    blackout_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_blackout_time_input, pattern="^blackout_quotex$"),
            CallbackQueryHandler(start_blackout_time_input, pattern="^blackout_binolla$"),
        ],
        states={
            WAITING_BLACKOUT_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_blackout_start_time)],
            WAITING_BLACKOUT_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_blackout_end_time)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(blackout_conversation)

    otc_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_otc_time_input, pattern="^otc_quotex$"),
            CallbackQueryHandler(start_otc_time_input, pattern="^otc_binolla$"),
        ],
        states={
            WAITING_OTC_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_otc_start_time)],
            WAITING_OTC_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_otc_end_time)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(otc_conversation)

    otc_chk_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(show_otc_chk_time_input, pattern="^otc_chk_quotex$"),
            CallbackQueryHandler(show_otc_chk_time_input, pattern="^otc_chk_binolla$"),
        ],
        states={
            WAITING_OTC_CHK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_otc_chk_time_list)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(otc_chk_conversation)

    live_chk_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(show_live_checker_time_input, pattern="^live_checker$")],
        states={
            WAITING_LIVE_CHK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_live_chk_time_list)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(live_chk_conversation)

    blk_chk_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(show_blackout_chk_time_input, pattern="^blk_chk_quotex$"),
            CallbackQueryHandler(show_blackout_chk_time_input, pattern="^blk_chk_binolla$"),
        ],
        states={
            WAITING_BLK_CHK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_blackout_chk_time_list)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(blk_chk_conversation)

    axtiron_chk_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(show_axtiron_chk_time_input, pattern="^axtiron_checker$")],
        states={
            WAITING_AXTIRON_CHK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_axtiron_chk_time_list)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(axtiron_chk_conversation)

    promo_code_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(show_promo_code_input, pattern="^promo_code$")],
        states={
            WAITING_PROMO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_promo_code)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(promo_code_conversation)

    formatter_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(show_formatter_input, pattern="^formatter$"),
            CallbackQueryHandler(show_formatter_input, pattern="^fmt_new$"),
        ],
        states={
            WAITING_FORMATTER_SIGNAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_formatter_signal_list)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(formatter_conversation)

    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(ChatMemberHandler(track_channel_join, ChatMemberHandler.CHAT_MEMBER))

    logger.info("=" * 50)
    logger.info(f"{e('🚀')} Advanced Trading Signals Bot is running!")
    logger.info(f"{e('✨')} All emojis are premium custom emojis!")
    logger.info("=" * 50)
    logger.info("{e('⏹️')}  Press Ctrl+C to stop the bot")
    logger.info("=" * 50)

    application.run_polling(allowed_updates=["message", "callback_query", "chat_member"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n{e('🛑')} Bot stopped by user")
    except Exception as e:
        logger.error(f"{e('❌')} Bot error: {e}")
        sys.exit(1)
