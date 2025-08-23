# monitor_multi_advanced.py — v2.4 с максимальными покупками по фильтрам

import asyncio
import os
import json
import argparse
from datetime import datetime
from telethon import TelegramClient, functions, types, errors
from config import API_ID, API_HASH, SESSION_NAME, ADMIN_USERNAME, HEARTBEAT_INTERVAL, ENABLE_HEARTBEAT

CHECK_INTERVAL = 10
seen_gifts = {}
pending_gifts = {}
last_bought = {}
purchase_summary = {}

# Мониторинг живости
last_heartbeat = 0
bot_start_time = None

async def send_admin_notification(client, message):
    """Отправляет уведомление администратору"""
    try:
        await client.send_message(ADMIN_USERNAME, message)
    except Exception as e:
        print(f"[ERROR] Не удалось отправить уведомление админу: {e}")

async def send_heartbeat(client, iteration, gifts_count, active_peers):
    """Отправляет сообщение о живости бота"""
    if not ENABLE_HEARTBEAT:
        return
    
    global last_heartbeat, bot_start_time
    now = datetime.now().timestamp()
    
    if now - last_heartbeat >= HEARTBEAT_INTERVAL:
        uptime = datetime.now() - bot_start_time if bot_start_time else None
        uptime_str = str(uptime).split('.')[0] if uptime else "unknown"
        
        message = f"💚 Бот жив!\n"
        message += f"🕐 Работает: {uptime_str}\n"
        message += f"🔄 Итераций: {iteration}\n"
        message += f"🎁 Подарков в очереди: {gifts_count}\n"
        message += f"👥 Активных каналов: {active_peers}\n"
        message += f"📅 {datetime.now().strftime('%H:%M:%S')}"
        
        await send_admin_notification(client, message)
        last_heartbeat = now

async def get_current_gifts(client):
    gifts = {}
    try:
        result = await client(functions.payments.GetStarGiftsRequest(hash=0))
        for gift in result.gifts:
            price = gift.stars
            remain = getattr(gift, "availability_remains", None)
            gifts[gift.id] = (price, remain)
    except errors.RPCError as e:
        print(f"[ERROR get_current_gifts] {e}")
    return gifts

async def purchase_gift_for_peer(client, peer, gift_id, price):
    try:
        peer_entity = await client.get_input_entity(peer)
        invoice = types.InputInvoiceStarGift(peer_entity, gift_id, None, False)
        payment_form = await client(functions.payments.GetPaymentFormRequest(invoice=invoice))
        await client(functions.payments.SendStarsFormRequest(payment_form.form_id, invoice))
        print(f"[PURCHASE] Peer={peer} купил GiftID={gift_id} за {price}⭐")
        purchase_summary.setdefault(peer, {})
        purchase_summary[peer][price] = purchase_summary[peer].get(price, 0) + 1
        return True
    except errors.RPCError as e:
        if "BALANCE_TOO_LOW" in str(e):
            return "low"
        print(f"[ERROR purchase_gift_for_peer] {e}")
        return False

def write_purchase_log(path="purchase_log.txt"):
    if not purchase_summary:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"=== {timestamp} ===\n")
        for peer, purchases in purchase_summary.items():
            f.write(f"{peer}:\n")
            print(f"{peer}:")
            for price, count in sorted(purchases.items()):
                word = "подарков" if count > 1 else "подарок"
                line = f"  {count} {word} по {price}⭐"
                f.write(line + "\n")
                print(line)
        f.write("\n")

def load_budgets(path="budgets.json"):
    if not os.path.exists(path):
        print(f"[ERROR] Файл {path} не найден.")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for peer, info in data.items():
        info.setdefault("spent", 0)
        info.setdefault("min_price", 0)
        info.setdefault("max_price", float('inf'))
        info.setdefault("filters", [])
    return data

def save_budgets(data, path="budgets.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-unlimited", action="store_true", default=False)
    args = parser.parse_args()

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    global seen_gifts, pending_gifts, last_bought, purchase_summary, bot_start_time
    bot_start_time = datetime.now()
    
    # Уведомляем о старте
    await send_admin_notification(client, f"🚀 Бот запущен!\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    budgets = load_budgets()
    if not budgets:
        return
    peers = list(budgets.keys())
    last_bought = {p: None for p in peers}
    filter_counters = {p: [0]*len(budgets[p].get("filters", [])) for p in peers}

    current = await get_current_gifts(client)
    seen_gifts = {gid: None for gid, (_, remain) in current.items() if remain is not None}
    with open("seen_gifts.json", "w", encoding="utf-8") as f:
        json.dump(list(seen_gifts.keys()), f)

    print("[INFO] Каналы и лимиты:")
    for peer in peers:
        b = budgets[peer]["budget"]
        s = budgets[peer]["spent"]
        mn = budgets[peer].get("min_price", 0)
        mx = budgets[peer].get("max_price", float('inf'))
        print(f"  {peer}: spent={s}/{b}, range=[{mn}–{mx}]")

    print("[INFO] Стартовые finite-подарки:")
    for gid, (price, remain) in current.items():
        if remain is not None:
            print(f"  ID={gid}, цена={price}⭐, осталось={remain}")

    iteration = 0
    while True:
        try:
            new_budgets = load_budgets()
            for peer in new_budgets:
                if peer in budgets:
                    new_budgets[peer]["spent"] = budgets[peer].get("spent", 0)
            budgets = new_budgets
            peers = list(budgets.keys())
            last_bought = {p: last_bought.get(p) for p in peers}

            current_gifts = await get_current_gifts(client)
            for gid, (price, remain) in current_gifts.items():
                if gid in seen_gifts:
                    continue
                if remain is not None:
                    seen_gifts[gid] = None
                    pending_gifts[gid] = [price, remain]
                    message = f"🚨 НОВЫЙ ПОДАРОК!\n🎁 ID: {gid}\n💰 Цена: {price}⭐\n📦 Осталось: {remain}"
                    print(f"[INFO] Новый finite-подарок: ID={gid}, цена={price}⭐, осталось={remain}")
                    await send_admin_notification(client, message)
                elif args.allow_unlimited:
                    seen_gifts[gid] = None
                    pending_gifts[gid] = [price, None]
                    message = f"🚨 НОВЫЙ БЕЗЛИМИТНЫЙ ПОДАРОК!\n🎁 ID: {gid}\n💰 Цена: {price}⭐\n♾️ Количество: неограничено"
                    await send_admin_notification(client, message)

            with open("seen_gifts.json", "w", encoding="utf-8") as f:
                json.dump(list(seen_gifts.keys()), f)

            bought_something = True
            while bought_something:
                bought_something = False
                # Удаляем подарки с 0 остатком
                for gid in list(pending_gifts.keys()):
                    price, remain = pending_gifts[gid]
                    if remain is not None and remain <= 0:
                        del pending_gifts[gid]

                for peer in peers:
                    info = budgets[peer]
                    budget, spent = info["budget"], info["spent"]
                    available = budget - spent
                    if available <= 0:
                        continue

                    filters = info.get("filters")
                if filters:
                    for i, f in enumerate(filters):
                        limit = f.get("limit", 0)
                        bought_count = filter_counters[peer][i]
                        can_buy = limit - bought_count
                        if can_buy <= 0:
                            continue

                        max_price = f.get("max_price", float('inf'))
                        max_remain = f.get("max_remain", float('inf'))

                        for gid, (price, remain) in list(pending_gifts.items()):
                            if remain is not None and remain <= 0:
                                continue
                            if price > max_price or (remain is not None and remain > max_remain):
                                continue
                            if price > available:
                                continue
                            if gid == last_bought.get(peer):
                                continue

                            max_gifts_by_budget = available // price
                            max_gifts = min(can_buy, max_gifts_by_budget)
                            if remain is not None:
                                max_gifts = min(max_gifts, remain)

                            if max_gifts <= 0:
                                continue

                            for _ in range(max_gifts):
                                status = await purchase_gift_for_peer(client, peer, gid, price)
                                if status is True:
                                    budgets[peer]["spent"] += price
                                    save_budgets(budgets)
                                    last_bought[peer] = gid
                                    filter_counters[peer][i] += 1
                                    available -= price
                                    bought_something = True
                                    remain = remain - 1 if remain is not None else None
                                    if remain == 0:
                                        pending_gifts.pop(gid)
                                        break
                                    else:
                                        pending_gifts[gid] = [price, remain]
                                    try:
                                        await client.send_message(peer, f"✅ Gift ID={gid} куплен за {price}⭐. Осталось {remain}.")
                                    except:
                                        pass
                                elif status == "low":
                                    budgets[peer]["spent"] = budget
                                    save_budgets(budgets)
                                    break
                                else:
                                    break
                            if available <= 0 or filter_counters[peer][i] >= limit:
                                break
                    continue

                # Если фильтров нет — стандартная логика (один подарок)
                mn, mx = info.get("min_price", 0), info.get("max_price", float('inf'))
                chosen_gid = None
                for gid, (price, remain) in pending_gifts.items():
                    if remain is not None and remain <= 0:
                        continue
                    if not (mn <= price <= mx) or price > available:
                        continue
                    if gid == last_bought.get(peer):
                        continue
                    chosen_gid = gid
                    break

                if chosen_gid is None and last_bought.get(peer) in pending_gifts:
                    price0, remain0 = pending_gifts[last_bought[peer]]
                    if (remain0 is None or remain0 > 0) and (mn <= price0 <= mx) and price0 <= available:
                        chosen_gid = last_bought[peer]

                if chosen_gid is None:
                    continue

                price, remain = pending_gifts[chosen_gid]
                status = await purchase_gift_for_peer(client, peer, chosen_gid, price)
                if status is True:
                    budgets[peer]["spent"] += price
                    save_budgets(budgets)
                    last_bought[peer] = chosen_gid
                    if remain is not None:
                        remain -= 1
                    pending_gifts.pop(chosen_gid)
                    if remain is None or remain > 0:
                        pending_gifts[chosen_gid] = [price, remain]
                    bought_something = True
                    try:
                        await client.send_message(peer, f"Gift ID={chosen_gid} куплен за {price}⭐. Осталось {remain}.")
                    except:
                        pass
                                elif status == "low":
                                    budgets[peer]["spent"] = budget
                                    save_budgets(budgets)

            write_purchase_log()
            purchase_summary.clear()

            # Отправляем heartbeat
            active_peers = len([p for p in peers if budgets[p]["budget"] - budgets[p]["spent"] > 0])
            await send_heartbeat(client, iteration, len(pending_gifts), active_peers)

            iteration += 1
            if iteration % 3 == 0:
                print(f"[DEBUG] Бот активен. Ждём {CHECK_INTERVAL} сек...")

            await asyncio.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            error_msg = f"🚨 КРИТИЧЕСКАЯ ОШИБКА!\n❌ {str(e)}\n🔄 Перезапускаюсь через 30 сек..."
            print(f"[ERROR] {e}")
            await send_admin_notification(client, error_msg)
            await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
#python -m venv venv скачать
#source venv/bin/activate активировать
#python monitor_multi_advanced.py стартовать 
#python monitor_multi_advanced.py --allow-unlimited стартовать тест на безлимитках 
