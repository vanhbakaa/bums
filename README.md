## Table of Contents
- [Recommendation before use](#recommendation-before-use)
- [Features](#features)
- [Settings](#settings)
- [Wallet](#wallet)
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Obtaining API Keys](#obtaining-api-keys)
- [Installation](#installation)
- [Support](#support-this-project)
- [Contacts](#contacts)

> [!WARNING]
> ⚠️ I do my best to avoid detection of bots, but using bots is forbidden in all airdrops. i cannot guarantee that you will not be detected as a bot. Use at your own risk. I am not responsible for any consequences of using this software.


# 🔥🔥 Use PYTHON 3.10-3.11 🔥🔥

## Features  
| Feature                                                     | Supported  |
|---------------------------------------------------------------|:----------------:|
| Multithreading                                                |        ✅        |
| Proxy binding to session                                      |        ✅        |
| Auto ref                                                      |        ✅        |
| Auto checkin                                                  |        ✅        |
| Auto tasks                                                    |        ✅        |
| Auto tap                                                      |        ✅        |
| Auto upgrade cards                                            |        ✅        |
| Auto play spin                                                |        ✅        |
| Auto cliam free box                                           |        ✅        |
| Support for pyrogram .session / Query                         |        ✅        |

## [Settings](https://github.com/vanhbakaa/bums/blob/main/.env-example)
| Settings | Description |
|----------------------------|:-------------------------------------------------------------------------------------------------------------:|
| **API_ID / API_HASH**      | Platform data from which to run the Telegram session (default - android)                                      |       
| **REF_LINK**               | Put your ref link here (default: my ref link)                                                                 |
| **AUTO_TAP**             | Auto tap (default: True)                                                                                 |
| **MIN_ENERGY**             | Minium energy to sleep (default: 500)                                                                                 |
| **SLEEP_BETWEEN_TAPS**             | Sleep time between taps (default: [20, 30] seconds)                                                                                 |
| **RANDOM_TAP_TIMES**             | Total tap times (default: [5, 10])                                                                                 |
| **AUTO_TASK**             | Auto do tasks (default: True)                                                                                 |
| **BLACK_LIST_TASKS**               | Auto join channel to complete channel tasks (default: False)                                                                        |
| **GAMES_TO_PLAY**               | Bot won't do these tasks(default: ["invite 1 friend", "Promote TON Blockchain", "Boost channel", "Boinkers: Spin the Slut 10 times"]) |
| **AUTO_JOIN_GANG**             | Auto join gang(default: True)                                                                                 |
| **DELAY_EACH_ACCOUNT**               | Random delay bewteen accounts (default: [20, 30] in seconds)                                                                        |
| **GANG_TO_JOIN**             | Name of gang to join (default: My gang)                                                                                 |
| **AUTO_UPGRADE_TAP**             | Auto upgrade tap (default: True)                                                                                 |
| **TAP_MAX_LVL**             | Maxium level to upgrade tap (default: 9)                                                                                 |
| **AUTO_UPGRADE_ENERGY**             | Auto upgrade energy (default: True)                                                                                 |
| **ENERGY_MAX_LVL**             | Maxium level to upgrade energy (default: 5)                                                                                 |
| **AUTO_UPGRADE_RECOVERY**             | Auto upgrade recovery (default: True)                                                                                 |
| **RECOVERY_MAX_LVL**             | Maxium level to upgrade recovery (default: 9)                                                                                 |
| **AUTO_UPGRADE_CRIT_MULTI**             | Auto upgrade crit multi (default: True)                                                                                 |
| **CRIT_MULTI_MAX_LVL**             | Maxium level to upgrade crit multi (default: 5)                                                                                 |
| **AUTO_UPGRADE_JACKPOT_CHANCE**             | Auto upgrade jackpot chance (default: True)                                                                                 |
| **CRIT_MULTI_MAX_LVL**             | Maxium level to upgrade jackpot chance (default: 5)                                                                                 |
| **AUTO_UPGRADE_CARDS**             | Auto upgrade cards (default: True)                                                                                 |
| **AUTO_PLAY_SPIN**             | Autoplay spin (default: True)                                                                                 |
| **DELAY_EACH_ACCOUNT**               | Random delay bewteen each account (default: [20, 30] seconds)                   |
| **SLEEP_TIME_BETWEEN_EACH_ROUND**               | Random delay bewteen each round (default: [1,2] in hours)                   |
| **ADVANCED_ANTI_DETECTION**  | Add more protection for your account (default: True)                                           |
| **USE_PROXY_FROM_FILE**    | Whether to use a proxy from the bot/config/proxies.txt file (True / False)                        |



## Quick Start

To install libraries and run bot - open run.bat on Windows

## Prerequisites
Before you begin, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) **IMPORTANT**: Make sure to use **3.10 - 3.11**. 

## Obtaining API Keys
1. Go to my.telegram.org and log in using your phone number.
2. Select "API development tools" and fill out the form to register a new application.
3. Record the API_ID and API_HASH provided after registering your application in the .env file.


## Installation
You can download the [**repository**](https://github.com/vanhbakaa/bums) by cloning it to your system and installing the necessary dependencies:
```shell
git clone https://github.com/vanhbakaa/bums.git
cd bums
```

Then you can do automatic installation by typing:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux manual installation
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
```

You can also use arguments for quick start, for example:
```shell
~/Paws >>> python3 main.py --action (1/2)
# Or
~/Paws >>> python3 main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

# Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
```
You can also use arguments for quick start, for example:
```shell
~/Paws >>> python3 main.py --action (1/2)
# Or
~/Paws >>> python3 main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

# Termux manual installation
```
> pkg update && pkg upgrade -y
> pkg install python rust git -y
> git clone https://github.com/vanhbakaa/bums.git
> cd Clayton
> pip install -r requirements.txt
> python main.py
```

You can also use arguments for quick start, for example:
```termux
~/bums > python main.py --action (1/2)
# Or
~/bums > python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session 
```
# Support This Project

If you'd like to support the development of this project, please consider making a donation. Every little bit helps!

👉 **[Click here to view donation options](https://github.com/vanhbakaa/Donation/blob/main/README.md)** 👈

Your support allows us to keep improving the project and bring more features!

Thank you for your generosity! 🙌

### Contacts

For support or questions, you can contact me [![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/airdrop_tool_vanh)
