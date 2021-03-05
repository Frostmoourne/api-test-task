import csv
import time


def db_handler() -> dict:
    """
    Функция-обработчик csv-файла.
    Создает словарь с ключами по имени товара и значениями в виде рекомедаций подходящих товаров.
    {
        sku: [
                [sku2, 0.6],
                [sku3, 0.3]
            ]
    }
    """
    items = {}
    with open('recommends.csv', newline='') as recs:
        reader = csv.reader(recs)
        for row in reader:
            # Если такой ключ уже существует берется его значение, иначе пустой список
            if row[0] in items:
                matched_key = items.get(row[0])
            else:
                matched_key = []
            matched_key.append(row[1:])
            items[row[0]] = matched_key
        return items


if __name__ == '__main__':
    start = time.time()
    db_handler()
    print(time.time() - start)


