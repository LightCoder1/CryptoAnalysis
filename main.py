import requests

# Создаем глобальную сессию для повторного использования соединений
session = requests.Session()

tokens_under_monitoring = ["AMBUSDT", "ARKUSDT", "BONDUSDT",  "JASMYUSDT", "LINAUSDT", "LOOMUSDT", "OMGUSDT", "REEFUSDT", "RENUSDT", "UNFIUSDT", "XEMUSDT", "LOOMUSDT",  "ZECUSDT", "ZENUSDT"]

def get_market_depth(symbol, distance, min_volume):
    url = f'https://fapi.binance.com/fapi/v1/depth?symbol={symbol}&limit=500'
    # Используем созданную сессию для запроса
    response = session.get(url)
    if response.status_code == 200:
        data = response.json()
        bids = data.get('bids', [])
        if bids:
            best_bid = float(bids[0][0])
            volume_in_usdt = sum(float(bid[0]) * float(bid[1]) for bid in bids if float(bid[0]) >= best_bid * distance)
            return volume_in_usdt
    return 0

def main():
    user_input = input('Введите список токенов через запятую (например, BTCUSDT,ETHUSDT): ')
    user_symbols = [symbol.strip().upper() for symbol in user_input.split(',')]
    min_volume = float(input("Введите минимальный объем в USDT: "))

    distances_input = input("Введите три дистанции через запятую в следующем формате: для 1%-0.99,1.5%-0.985,2%-0.98 (например, 0.99,0.985,0.98): ")
    distances = [float(distance.strip()) for distance in distances_input.split(',')]

    tokens_lists = {distance: [] for distance in distances}
    not_qualified_tokens = set()
    monitored_tokens = []

    for symbol in user_symbols:
        qualified = False
        if symbol in tokens_under_monitoring:
            monitored_tokens.append(symbol)
        for distance in distances:
            volume_in_usdt = get_market_depth(symbol, distance, min_volume)
            if volume_in_usdt > min_volume:
                tokens_lists[distance].append(symbol)
                qualified = True
                break
        if not qualified:
            not_qualified_tokens.add(symbol)

    for distance, tokens in tokens_lists.items():
        print(f"Дистанция до {round(float((1-distance)*100),2)}%: {','.join(sorted(tokens))}")
    print(f"Токены, не попавшие ни в один список: {','.join(sorted(not_qualified_tokens))}")
    print(f"Из них токены под наблюдением/с высоким риском: {','.join(sorted(monitored_tokens))}")

if __name__ == "__main__":
    main()
