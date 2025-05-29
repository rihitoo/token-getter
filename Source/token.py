import uuid
import requests
import random
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def rikuo():
    android_version = f"{random.randint(5, 14)}.{random.randint(0, 9)}"
    fb_version = f"{random.randint(100, 999)}.0.0.{random.randint(10, 99)}.{random.randint(100, 999)}"
    fbbv = random.randint(100000000, 999999999)
    fbca = random.choice([
        "armeabi-v7a:armeabi", "arm64-v8a:armeabi", "armeabi-v7a",
        "armeabi", "arm86-v6a", "arm64-v8a"
    ])
    manufacturer = random.choice([
        "Samsung", "Realme", "Oppo", "Vivo", "Xiaomi", "Huawei",
        "OnePlus", "Infinix", "Nokia", "Tecno", "Asus", "Sony"
    ])
    model = random.choice([
        f"SM-{random.randint(100, 9999)}U", f"RMX{random.randint(1000, 9999)}",
        f"CPH{random.randint(1000, 9999)}", f"V{random.randint(1000, 9999)}",
        f"M{random.randint(1000, 9999)}", f"ELS-{random.choice(['NX9', 'AN10', 'AL00'])}",
        f"KB{random.randint(1000, 9999)}", f"X{random.randint(1000, 9999)}",
        f"TA-{random.randint(1000, 9999)}"
    ])
    return f"Dalvik/2.1.0 (Linux; U; Android {android_version}; {model} Build/{manufacturer}) [FBAN/FB4A;FBAV/{fb_version};FBBV/{fbbv};FBDM={{density=2.0,width=1080,height=1920}};FBLC/en_US;FBOP/1;FBCA/{fbca}]"

def manual_token_getter(user, password):
    access_token = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
    data = {
        'adid': str(uuid.uuid4()),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'cpl': 'true',
        'family_device_id': str(uuid.uuid4()),
        'credentials_type': 'device_based_login_password',
        'email': user,
        'password': password,
        'access_token': access_token,
        'generate_session_cookies': '1',
        'locale': 'en_US',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'api_key': '62f8ce9f74b12f84c123cc23437a4a32',
    }

    headers = {
        'User-Agent': rikuo(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'graph.facebook.com'
    }

    try:
        response = requests.post("https://b-graph.facebook.com/auth/login", headers=headers, data=data).json()

        if "session_key" in response and "session_cookies" in response:
            token = response.get("access_token", "N/A")
            c_user = next((c['value'] for c in response['session_cookies'] if c['name'] == 'c_user'), "N/A")
            cookies = '; '.join(f"{c['name']}={c['value']}" for c in response['session_cookies'])

            # Create save directory
            save_dir = "/sdcard/Rikuo"
            os.makedirs(save_dir, exist_ok=True)

            # Save token
            with open(f"{save_dir}/fbtoken.txt", "a") as tf:
                tf.write(token + "\n")

            # Save cookie
            with open(f"{save_dir}/fbcookie.txt", "a") as cf:
                cf.write(cookies + "\n")

            console.print(Panel.fit(
                f"[green]Login Success[/green]\n"
                f"[bold]User:[/bold] {user}\n"
                f"[bold]C_USER:[/bold] {c_user}\n"
                f"[bold]Access Token:[/bold] {token}\n"
                f"[bold]Cookies:[/bold] {cookies}",
                title="Success", border_style="green"))

        else:
            msg = response.get("error", {}).get("message", "Unknown error")
            console.print(Panel(f"[red]Login Failed[/red]\n{msg}", title="Error", border_style="red"))

    except Exception as e:
        console.print(Panel(f"[red]Exception[/red]\n{str(e)}", title="Error", border_style="red"))

def banner():
    console.print(Panel("[bold cyan]Facebook Token & Cookie Grabber[/bold cyan]", style="cyan"))

def fbcookie():
    banner()
    user = input("Enter Email / ID / Phone: ").strip()
    password = input("Enter Password: ").strip()
    manual_token_getter(user, password)

def main():
    fbcookie()

if __name__ == "__main__":
    main()
