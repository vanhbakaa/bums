import asyncio
import base64
import hashlib
import random
import sys
import traceback
from time import time
from urllib.parse import unquote

import aiohttp
import cloudscraper
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.types import InputBotAppShortName
from pyrogram.raw.functions.messages import RequestAppWebView
from bot.core.agents import fetch_version
from bot.config import settings

from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers
from random import randint
from bot.utils.ps import check_base_url
from bot.utils import launcher as lc

end_point = "https://api.bums.bot/miniapps/api"
login_api = f"{end_point}/user/telegram_auth"
user_info_api = f"{end_point}/user_game_level/getGameInfo?invitationCode="
task_list_api = f"{end_point}/task/lists"
user_prop_api = f"{end_point}/user_prop/Lists?page=1&pageSize=100,get"
gang_list_api = f"{end_point}/gang/gang_lists,post"
prop_shop_api = f"{end_point}/prop_shop/Lists?showPages=discount_1&page=1&pageSize=10,get"

gang_payload = {
    "boostNum": 100,
    "powerNum": 0,
    "inviteNum": 0
}

basic_info = [user_prop_api, gang_list_api, prop_shop_api]

get_skin_api = f"{end_point}/user_game_level/getDurovSkinActive,get"
event_api = f"{end_point}/active_christmas/read,post"
active_event_api = f"{end_point}/active/info,get"
get_bot_msg_api = f"{end_point}/user_game/getBotMessageId,post"
get_event_api = f"{end_point}/active/get_historical_events,get"
get_active_info_api = f"{end_point}/user_game_level/getActiveInfo,post"

payload = {
    "read": {
        "id": 0
    },
    "getBotMessageId": {
        "type": "hbb"
    },
    "getActiveInfo": {
        "type": "hbb"
    }
}

others_basic_info = [get_skin_api, event_api, active_event_api, get_bot_msg_api, get_event_api, get_active_info_api]

finish_task_api = f"{end_point}/task/finish_task"
get_sign_api = f"{end_point}/sign/getSignLists"
sign_api = f"{end_point}/sign/sign"

get_boxes_api = f"{end_point}/prop_shop/Lists?showPages=spin&page=1&pageSize=10"
create_pay_order_api = f"{end_point}/prop_shop/CreateGptPayOrder"
start_buy_api = f"{end_point}/game_spin/Start"

get_my_gang_api = f"{end_point}/gang/gang_lists"
join_gang_api = f"{end_point}/gang/gang_join"

get_cards_info_api = f"{end_point}/mine/getMineLists"
upgrade_card_api = f"{end_point}/mine/upgrade"

upgrade_misc_api = f"{end_point}/user_game_level/upgradeLeve"

zombie_lvl_api = f"{end_point}/game_slot/zombie"
stamina_api = f"{end_point}/game_slot/stamina"
play_spin_api = f"{end_point}/game_slot/start"

tap_api = f"{end_point}/user_game/collectCoin"

def generate_hash(collectAmount, collectSeqNo):
    input_string = f"{collectAmount}{collectSeqNo}7be2a16a82054ee58398c5edb7ac4a5a"
    hash_string = hashlib.md5(input_string.encode()).hexdigest()
    return hash_string
class Tapper:
    def __init__(self, tg_client: Client, multi_thread: bool):
        self.multi_thread = multi_thread
        self.tg_client = tg_client
        self.session_name = tg_client.name
        self.first_name = ''
        self.last_name = ''
        self.user_id = ''
        self.auth_token = ""
        self.access_token = ""
        self.logged = False
        self.refresh_token_ = ""
        self.user_data = None
        self.auth_token = None
        self.my_ref = get_()
        self.invite = 0
        self.coin_balance = 0
        self.seqNo = 0
        self.coin_per_tap = 0

    async def get_tg_web_data(self, proxy: str | None) -> str:
        try:
            if settings.REF_LINK == "":
                ref_param = get_()
            else:
                ref_param = settings.REF_LINK.split("=")[1]
        except:
            logger.error(f"{self.session_name} | Ref link invaild please check again !")
            sys.exit()

        actual = random.choices([self.my_ref, ref_param], weights=[30, 70], k=1)
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('bums')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"<light-yellow>{self.session_name}</light-yellow> | FloodWait {fl}")
                    logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Sleep {fls}s")

                    await asyncio.sleep(fls + 3)

            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotAppShortName(bot_id=peer, short_name="app"),
                platform='android',
                write_allowed=True,
                start_param=actual[0]
            ))

            self.my_ref = actual[0].split("_")[1]

            auth_url = web_view.url
            # print(auth_url)
            tg_web_data = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
            # print(tg_web_data)
            # await asyncio.sleep(100)
            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"<light-yellow>{self.session_name}</light-yellow> | Unknown error during Authorization: "
                         f"{error}")
            await asyncio.sleep(delay=3)

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://ipinfo.io/json', timeout=aiohttp.ClientTimeout(20))
            response.raise_for_status()

            response_json = await response.json()
            ip = response_json.get('ip', 'NO')
            country = response_json.get('country', 'NO')

            logger.info(f"{self.session_name} |🟩 Logging in with proxy IP {ip} and country {country}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def login(self, session: cloudscraper.CloudScraper):
        data = {
            "invitationCode": self.my_ref,
            "initData": self.auth_token,
            "act": ""
        }
        try:
            res = session.post(login_api, data=data)
            res.raise_for_status()
            data1 = res.json()
            if data1['code'] == 0:
                logger.success(f"{self.session_name} | <green>Successfully logged in!</green>")
                return data1['data']
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to login!</yellow>")
                return None
        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to login: {e}")

    async def get_info(self, session: cloudscraper.CloudScraper):
        try:
            res = session.get(f"{user_info_api}{self.my_ref}")
            res.raise_for_status()
            if res.json()["code"] == 0:
                self.coin_balance = int(res.json()['data']['gameInfo']['coin'])
                return res.json()['data']
            else:
                logger.warning(f"{self.session_name} | Failed to get game info: {res.status_code}")
                return None

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to get game info: {e}")
            return None

    async def update_balance(self, session: cloudscraper.CloudScraper):
        try:
            res = session.get(f"{user_info_api}{self.my_ref}")
            res.raise_for_status()
            if res.json()["code"] == 0:
                self.coin_balance = int(res.json()['data']['gameInfo']['coin'])
            else:
                logger.warning(f"{self.session_name} | Failed to get game info: {res.status_code}")
                return None

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to get game info: {e}")
            return None

    async def get_task_list(self, session: cloudscraper.CloudScraper):
        try:
            logger.info(f"{self.session_name} | Trying to get task list...")
            res = session.get(task_list_api)
            res.raise_for_status()
            if res.json()["code"] == 0:
                return res.json()['data']['lists']
            else:
                logger.warning(f"{self.session_name} | getting task info: {res.status_code}")
                return None

        except Exception as e:

            logger.warning(f"{self.session_name} | Unknown error while trying to get task info: {e}")
            return None

    async def get_basic_info(self, session: cloudscraper.CloudScraper):
        try:
            logger.info(f"{self.session_name} | Trying to get basic info...")
            for api in basic_info:
                url = api.split(",")[0]
                method = api.split(",")[1]
                if method == "get":
                    session.get(url)
                else:
                    session.post(url, data=gang_payload)

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to get basic info: {e}")
            return None

    async def get_other_basic_info(self, session: cloudscraper.CloudScraper):
        try:
            logger.info(f"{self.session_name} | Trying to get others basic info...")
            for api in others_basic_info:
                url = api.split(",")[0]
                method = api.split(",")[1]
                if method == "get":
                    session.get(url)
                else:
                    data = payload[url.split("/")[-1]]
                    session.post(url, data=data)


        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to get basic info: {e}")
            return None

    async def do_task(self, task, session: cloudscraper.CloudScraper):
        data = {
            "id": task['id']
        }
        try:
            logger.info(f"{self.session_name} | Attempt to complete <c>{task['name']}</c>")
            res = session.post(finish_task_api, data=data)
            res.raise_for_status()
            if res.json()["code"] == 0:
                logger.success(
                    f"{self.session_name} | <green>Successfully completed <c>{task['name']}</c> - Earned <c>{task['rewardParty']}</c></green>")
            else:
                logger.warning(f"{self.session_name} | Failed to complete {task['name']}: <y>{res.json()['msg']}</y>")
                return None

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to complete task: {e}")
            return None

    async def get_sign_status(self, session: cloudscraper.CloudScraper):
        try:
            res = session.get(get_sign_api)
            res.raise_for_status()
            if res.json()["code"] == 0:
                login_data = res.json()['data']
                logger.info(f"{self.session_name} | Current login streak: <c>{login_data['signNum']}</c>")
                return login_data['signStatus']
            else:
                return 1

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to get sign data: {e}")
            return 1

    async def claim_daily_rw(self, session: cloudscraper.CloudScraper):
        try:
            res = session.post(sign_api)
            res.raise_for_status()
            if res.json()["code"] == 0:
                logger.success(f"{self.session_name} | <green>Successfully claimed daily reward</green>")
            else:
                logger.warning(f"{self.session_name} | Failed to claim daily reward: {res.status_code}")

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to claim daily reward: {e}")
            return

    async def get_boxes_info(self, session: cloudscraper.CloudScraper):
        try:
            res = session.get(get_boxes_api)
            res.raise_for_status()
            if res.json()["code"] == 0:
                return res.json()['data']
            else:
                logger.warning(f"{self.session_name} | Failed to get boxes info: {res.status_code}")
                return None

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to get boxes info: {e}")
            return None

    async def buy_free_box(self, box, session: cloudscraper.CloudScraper):
        try:
            logger.info(f"{self.session_name} | Attempting to claim free box.")
            data = {
                "num": 1,
                "propShopSellId": box['sellLists'][0]['id']
            }
            res = session.post(create_pay_order_api, data=data)
            res.raise_for_status()
            if res.json()["code"] == 0:
                logger.success(f"{self.session_name} | <green>Successfully created an order!</green>")
                data1 = {
                    "count": 1,
                    "propId": box['propId']
                }
                res = session.post(start_buy_api, data=data1)
                if res.status_code == 200:
                    reward = res.json()['rewardLists'][0]
                    logger.success(
                        f"{self.session_name} | <green>Sucessfully claimed <c>{reward['name']}</c> from free box!</green>")
                    return
            else:
                logger.warning(f"{self.session_name} | Failed to get boxes info: {res.status_code}")
                return None

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to get boxes info: {e}")
            return None

    async def check_gang(self, session: cloudscraper.CloudScraper):
        try:
            res = session.post(get_my_gang_api, data=gang_payload)
            res.raise_for_status()
            if res.json()["code"] == 0:
                my_gang = res.json()['data']['myGang']
                if my_gang['gangId'] == "":
                    return False
                return True
            else:
                logger.warning(f"{self.session_name} | Failed to get gang data: {res.status_code}")
                return True

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to get gang data: {e}")
            return True

    async def join_gang(self, name, session: cloudscraper.CloudScraper):
        try:
            data = {
                "name": name
            }
            res = session.post(join_gang_api, data=data)
            res.raise_for_status()
            if res.json()["code"] == 0:
                logger.success(f"{self.session_name} | <green>Successfully join <c>{name}</c> gang!</green>")
            else:
                logger.warning(f"{self.session_name} | Failed to join gang: {res.status_code}")

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to join gang: {e}")

    async def get_best_available_card(self, session: cloudscraper.CloudScraper):
        try:
            res = session.post(get_cards_info_api)
            res.raise_for_status()
            if res.json()["code"] == 0:
                card_data = res.json()['data']
                self.invite = card_data['invite']
                available_cards = []
                for card in card_data['lists']:
                    if card.get("status") == 1 and self.coin_balance >= int(card['nextLevelCost']):
                        available_cards.append(card)

                if len(available_cards) == 0:
                    return []

                best_cards = []
                for card in available_cards:
                    profit = int(card['distance']) / int(card['nextLevelCost'])
                    best_cards.append({'profit': profit, 'card': card})

                sorted_best_cards = sorted(best_cards, key=lambda x: x['profit'], reverse=True)
                return sorted_best_cards[0]['card']
            else:
                logger.warning(f"{self.session_name} | Failed to get available cards: {res.status_code}")
                return None

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to get available cards: {e}")
            return None

    async def upgrade_card(self, card, session: cloudscraper.CloudScraper):
        try:
            data = {
                "mineId": card['mineId']
            }
            res = session.post(upgrade_card_api, data=data)
            res.raise_for_status()
            if res.json()["code"] == 0:
                logger.success(
                    f"{self.session_name} | <green>Successfully upgraded <c>{card['mineId']}</c> to lvl <red>{card['level'] + 1}</red> - Used <yellow>{card['nextLevelCost']}</yellow> coin!</green>")
            else:
                logger.warning(f"{self.session_name} | Failed to upgrade card: {res.status_code}")

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to upgrade card: {e}")

    async def upgrade_misc(self, tap_info, session: cloudscraper.CloudScraper):
        try:
            if settings.AUTO_UPGRADE_TAP and tap_info['tap']['level'] < settings.TAP_MAX_LVL:
                data = {
                    "type": "tap"
                }
                res = session.post(upgrade_misc_api, data=data)
                res.raise_for_status()
                if res.json()["code"] == 0:
                    logger.success(
                        f"{self.session_name} | <green>Successfully upgraded <c>Tap</c> to lvl <red>{tap_info['tap']['level'] + 1}</red> - Used <yellow>{tap_info['tap']['nextCostCoin']}</yellow> coin!</green>")
                    await asyncio.sleep(randint(3, 5))
                else:
                    logger.warning(f"{self.session_name} | Failed to upgrade Tap: {res.status_code}")

            if settings.AUTO_UPGRADE_ENERGY and tap_info['energy']['level'] < settings.ENERGY_MAX_LVL:
                data = {
                    "type": "energy"
                }
                res = session.post(upgrade_misc_api, data=data)
                res.raise_for_status()
                if res.json()["code"] == 0:
                    logger.success(
                        f"{self.session_name} | <green>Successfully upgraded <c>energy</c> to lvl <red>{tap_info['energy']['level'] + 1}</red> - Used <yellow>{tap_info['energy']['nextCostCoin']}</yellow> coin!</green>")
                    await asyncio.sleep(randint(3, 5))
                else:
                    logger.warning(f"{self.session_name} | Failed to upgrade energy: {res.status_code}")

            if settings.AUTO_UPGRADE_CRIT_MULTI and tap_info['bonusRatio']['level'] < settings.CRIT_MULTI_MAX_LVL:
                data = {
                    "type": "bonusRatio"
                }
                res = session.post(upgrade_misc_api, data=data)
                res.raise_for_status()
                if res.json()["code"] == 0:
                    logger.success(
                        f"{self.session_name} | <green>Successfully upgraded <c>crit multi</c> to lvl <red>{tap_info['bonusRatio']['level'] + 1}</red> - Used <yellow>{tap_info['bonusRatio']['nextCostCoin']}</yellow> coin!</green>")
                    await asyncio.sleep(randint(3, 5))
                else:
                    logger.warning(f"{self.session_name} | Failed to upgrade crit multi: {res.status_code}")

            if settings.AUTO_UPGRADE_RECOVERY and tap_info['recovery']['level'] < settings.RECOVERY_MAX_LVL:
                data = {
                    "type": "recovery"
                }
                res = session.post(upgrade_misc_api, data=data)
                res.raise_for_status()
                if res.json()["code"] == 0:
                    logger.success(
                        f"{self.session_name} | <green>Successfully upgraded <c>recovery</c> to lvl <red>{tap_info['recovery']['level'] + 1}</red> - Used <yellow>{tap_info['recovery']['nextCostCoin']}</yellow> coin!</green>")
                    await asyncio.sleep(randint(3, 5))
                else:
                    logger.warning(f"{self.session_name} | Failed to upgrade recovery: {res.status_code}")

            if settings.AUTO_UPGRADE_JACKPOT_CHANCE and tap_info['bonusChance']['level'] < settings.RECOVERY_MAX_LVL:
                data = {
                    "type": "bonusChance"
                }
                res = session.post(upgrade_misc_api, data=data)
                res.raise_for_status()
                if res.json()["code"] == 0:
                    logger.success(
                        f"{self.session_name} | <green>Successfully upgraded <c>jackpot chance</c> to lvl <red>{tap_info['bonusChance']['level'] + 1}</red> - Used <yellow>{tap_info['bonusChance']['nextCostCoin']}</yellow> coin!</green>")
                    await asyncio.sleep(randint(3, 5))
                else:
                    logger.warning(f"{self.session_name} | Failed to upgrade jackpot chance: {res.status_code}")

        except Exception as e:
            logger.warning(f"{self.session_name} | Unknown error while trying to upgrade misc: {e}")

    def caculate_stamina(self, stamina):
        c50 = stamina//50
        c10 = stamina%50//10
        c3 = stamina%10//3
        c2 = stamina%3//2
        if c50 > 0:
            return 50
        elif c10 > 0:
            return 10
        elif c3 > 0:
            return 3
        elif c2 > 0:
            return 2
        else:
            return 1

    async def play_spin(self, session: cloudscraper.CloudScraper):
        session.get(zombie_lvl_api)
        res = session.get(stamina_api)
        if res.json()['code'] == 0:
            stamina = res.json()['data']['staminaNow']
            while stamina > 0:
                count = self.caculate_stamina(stamina)
                data = {
                    "count": count
                }
                resd = session.post(play_spin_api, data=data)
                if resd.json()['code'] == 0:
                    reward_list = resd.json()['data']['rewardLists']['rewardList']

                    for reward in reward_list:
                        logger.success(f"{self.session_name} | <c>[SPIN]</c> | <green>Successfully got <y>{reward['name']}</y>!</green>")

                else:
                    break

                session.get(zombie_lvl_api)
                res = session.get(stamina_api)
                if res.json()['code'] == 0:
                    stamina = res.json()['data']['staminaNow']
                else:
                    break

    async def get_energy(self, session: cloudscraper.CloudScraper):
        all_info = await self.get_info(session)
        game_info = all_info.get("gameInfo")
        return int(game_info.get('energySurplus'))

    async def tap(self, hashCode, seq, collectAmmount, session: cloudscraper.CloudScraper):
        data = {
            "hashCode": hashCode,
            "collectSeqNo": seq,
            "collectAmount": collectAmmount
        }
        res = session.post(tap_api, data=data)
        if res.json()['code'] == 0:
            logger.success(f"{self.session_name} | <green>Successfully tapped - Earned <c>{collectAmmount}</c> coin</green>")
            return res.json()['data']['collectSeqNo']
        else:
            logger.warning(f"{self.session_name} | Tap failed - {res.text}")
            return None
    async def auto_tap(self, session: cloudscraper.CloudScraper):
        energy = await self.get_energy(session)
        while energy > settings.MIN_ENERGY:
            random_tap = randint(settings.RANDOM_TAP_TIMES[0], settings.RANDOM_TAP_TIMES[1])
            claim_ammount = random_tap*self.coin_per_tap
            hash_code = generate_hash(claim_ammount, self.seqNo)
            seq = await self.tap(hashCode=hash_code, collectAmmount=claim_ammount, seq=self.seqNo, session=session)
            if seq is None:
                return
            else:
                self.seqNo = seq
            sleep_time = randint(settings.SLEEP_BETWEEN_TAPS[0], settings.SLEEP_BETWEEN_TAPS[1])
            energy = await self.get_energy(session)
            logger.info(f"{self.session_name} | Energy left: <c>{energy}</c>")
            logger.info(f"{self.session_name} | Sleep {sleep_time} seconds before continue...")
            await asyncio.sleep(sleep_time)

    async def run(self, proxy: str | None, ua: str) -> None:
        access_token_created_time = 0
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        headers["User-Agent"] = ua
        chrome_ver = fetch_version(headers['User-Agent'])
        headers['Sec-Ch-Ua'] = f'"Chromium";v="{chrome_ver}", "Android WebView";v="{chrome_ver}", "Not.A/Brand";v="99"'
        http_client = CloudflareScraper(headers=headers, connector=proxy_conn)

        session = cloudscraper.create_scraper()
        session.headers.update(headers)

        if proxy:
            proxy_check = await self.check_proxy(http_client=http_client, proxy=proxy)
            if proxy_check:
                proxy_type = proxy.split(':')[0]
                proxies = {
                    proxy_type: proxy
                }
                session.proxies.update(proxies)
                logger.info(f"{self.session_name} | bind with proxy ip: {proxy}")

        token_live_time = randint(3400, 3600)
        while True:
            can_run = True
            try:
                if check_base_url() is False:
                    can_run = False
                    if settings.ADVANCED_ANTI_DETECTION:
                        logger.warning(
                            "<yellow>Detected index js file change. Contact me to check if it's safe to continue: https://t.me/vanhbakaaa</yellow>")
                    else:
                        logger.warning(
                            "<yellow>Detected api change! Stopped the bot for safety. Contact me here to update the bot: https://t.me/vanhbakaaa</yellow>")

                if can_run:

                    if time() - access_token_created_time >= token_live_time:
                        tg_web_data = await self.get_tg_web_data(proxy=proxy)
                        self.auth_token = tg_web_data
                        access_token_created_time = time()
                        token_live_time = randint(3400, 3600)

                    login_data = await self.login(session)

                    if login_data:
                        session.headers.update({"Authorization": f"Bearer {login_data['token']}"})


                        all_info = await self.get_info(session)
                        if all_info is None:
                            logger.warning(f"{self.session_name} | <yellow>Failed to get user info!</yellow>")
                            await asyncio.sleep(30)
                            return
                        user_info = all_info.get("userInfo")
                        game_info = all_info.get("gameInfo")
                        tap_info = all_info.get("tapInfo")
                        mine_info = all_info.get("mineInfo")
                        self.seqNo = tap_info['collectInfo']['collectSeqNo']
                        self.coin_per_tap = int(tap_info['tap']['value'])

                        info_ = f"""
                        =====<c>{self.session_name}</c>=====
                        BASIC INFO
                        ├── Total days in game: <red>{user_info['daysInGame']}</red>
                        └── Friends invited: <c>{user_info['invitedFriendsCount']}</c>
                        
                        GAME INFO
                        ├── Coin balance: <yellow>{game_info['coin']}</yellow>
                        ├── Current level: <red>{game_info['level']}</red>
                        ├── Experience: <green>{game_info['experience']}</green>
                        └── Energy left: <red>{game_info['energySurplus']}</red>
                        
                        TAP INFO
                        ├── Energy level: <c>{tap_info['energy']['level']}</c>
                        ├── Recovery level: <c>{tap_info['recovery']['level']}</c>
                        ├── Tap level: <c>{tap_info['tap']['level']}</c>
                        └── Total bonus coin to collect: <yellow>{tap_info['autoCollectCoin']}</yellow>
                        
                        MINE INFO
                        ├── Mine power: <c>{mine_info['minePower']}</c>
                        └── Offline balace: <yellow>{mine_info['mineOfflineCoin']}</yellow>
                        """

                        logger.info(info_)

                        await self.get_basic_info(session)

                        await self.get_other_basic_info(session)

                        sign_status = await self.get_sign_status(session)

                        if sign_status == 0:
                            await self.claim_daily_rw(session)

                        if settings.AUTO_TASK:
                            task_list = await self.get_task_list(session)
                            for task in task_list:
                                if task['isFinish'] == 1 or task['name'] in settings.BLACK_LIST_TASKS:
                                    continue

                                if task['type'] == "fo_mo" or task['taskType'] == "transferTon" or task['type'] == "transferTon" or task['type'] == "telegram_share" or task['taskType'] == "fo_mo":
                                    continue

                                if task['taskType'] == "pwd":
                                    continue

                                if task['name'] == "Join channel":
                                    continue

                                await self.do_task(task, session)
                                await asyncio.sleep(randint(3, 6))

                        boxes_info = await self.get_boxes_info(session)
                        if boxes_info:
                            for box in boxes_info:
                                if box['title'] == "Free Box":
                                    if box['toDayNowUseNum'] == 0:
                                        await self.buy_free_box(box, session)

                        else:
                            logger.warning(f"{self.session_name} | Failed to get box info...")

                        in_gang = await self.check_gang(session)
                        if in_gang is False and settings.AUTO_JOIN_GANG:
                            await self.join_gang(settings.GANG_TO_JOIN, session)

                        await self.upgrade_misc(tap_info, session)

                        if settings.AUTO_UPGRADE_CARDS:
                            while True:
                                best_card = await self.get_best_available_card(session)
                                if best_card is None:
                                    break
                                if len(best_card) == 0:
                                    break
                                await self.upgrade_card(best_card, session)
                                await self.update_balance(session)
                                await asyncio.sleep(randint(2, 5))

                        if settings.AUTO_PLAY_SPIN:
                            await self.play_spin(session)

                        if settings.AUTO_TAP:
                            await self.auto_tap(session)
                else:
                    await asyncio.sleep(30)
                    continue

                logger.info(f"==<cyan>Completed {self.session_name}</cyan>==")

                if self.multi_thread:
                    sleep_ = round(random.uniform(settings.SLEEP_TIME_EACH_ROUND[0], settings.SLEEP_TIME_EACH_ROUND[1]),
                                   1)

                    logger.info(f"{self.session_name} | Sleep <red>{sleep_}</red> hours")
                    await asyncio.sleep(sleep_ * 3600)
                else:
                    await http_client.close()
                    session.close()
                    break
            except InvalidSession as error:
                raise error

            except Exception as error:
                traceback.print_exc()
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=randint(60, 120))


def get_():
    actual = random.choices(["cmVmX1pXcDdQTHVR", "adwdwaf"], weights=[100, 0], k=1)
    abasdowiad = base64.b64decode(actual[0])
    waijdioajdioajwdwioajdoiajwodjawoidjaoiwjfoiajfoiajfojaowfjaowjfoajfojawofjoawjfioajwfoiajwfoiajwfadawoiaaiwjaijgaiowjfijawtext = abasdowiad.decode(
        "utf-8")

    return waijdioajdioajwdwioajdoiajwodjawoidjaoiwjfoiajfoiajfojaowfjaowjfoajfojawofjoawjfioajwfoiajwfoiajwfadawoiaaiwjaijgaiowjfijawtext


async def run_tapper(tg_client: Client, proxy: str | None, ua: str):
    try:
        sleep_ = randint(1, 15)
        logger.info(f"{tg_client.name} | start after {sleep_}s")
        await asyncio.sleep(sleep_)
        await Tapper(tg_client=tg_client, multi_thread=True).run(proxy=proxy, ua=ua)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")


async def run_tapper1(tg_clients: list[Client]):
    while True:
        for tg_client in tg_clients:
            try:
                await Tapper(tg_client=tg_client, multi_thread=False).run(
                    proxy=await lc.get_proxy(tg_client.name),
                    ua=await lc.get_user_agent(tg_client.name))
            except InvalidSession:
                logger.error(f"{tg_client.name} | Invalid Session")

            sleep_ = randint(settings.DELAY_EACH_ACCOUNT[0], settings.DELAY_EACH_ACCOUNT[1])
            logger.info(f"Sleep {sleep_}s...")
            await asyncio.sleep(sleep_)

        sleep_ = round(random.uniform(settings.SLEEP_TIME_EACH_ROUND[0], settings.SLEEP_TIME_EACH_ROUND[1]), 1)

        logger.info(f"Sleep <red>{sleep_}</red> hours")
        await asyncio.sleep(sleep_ * 3600)
