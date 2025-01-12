from BTrees.OOBTree import OOBTree
import csv
import timeit

# Створення OOBTree
tree = OOBTree()
# OOBTree для сортування за ціною та швидкого пошуку
correct_tree = OOBTree()
# Створення словника
item_dict = {}

# Додавання об'єктів до дерева за структурою відповідно до опису домашнього завдання
def add_item_to_tree(tree):
    with open('generated_items_data.csv', mode='r') as file:
        csv_rows = csv.reader(file)
        next(csv_rows)
        for row in csv_rows:
            price = float(row[3])  # Переконуємося, що ціна є числом (float)
            tree.update({row[0]: {'Name': row[1], 'Category': row[2], 'Price': price}})

# Додавання об'єктів до дерева зі зміненою структурою для шкидкого пошуку діапазону цін
def add_item_to_correct_tree(tree):
    with open('generated_items_data.csv', mode='r') as file:
        csv_rows = csv.reader(file)
        next(csv_rows)
        for row in csv_rows:
            tree.update({float(row[3]): {'Name': row[1], 'Category': row[2], 'ID':row[0]}})



# Додавання об'єктів в словник
def add_item_to_dict(dict):
    with open('generated_items_data.csv', mode='r') as file:
        csv_rows = csv.reader(file)
        next(csv_rows)
        for row in csv_rows:
            price = float(row[3])  # Переконуємося, що ціна є числом (float)
            dict[row[0]] = {'Name': row[1], 'Category': row[2], 'Price': price}

# Заповнюємо дерево даними
add_item_to_tree(tree)

# Заповнюємо відкориговане дерево
add_item_to_correct_tree(correct_tree)

# Заповнюємо словник
add_item_to_dict(item_dict)

# Діапазонний запит для дерева
def range_query_tree(tree, min_price, max_price):
    result = []
    for key, value in tree.items():  # Отримуємо всі пари ключ-значення
        price = value['Price']
        if min_price <= price <= max_price:  # Перевіряємо чи ціна в межах діапазону
            result.append((key, value))
    return result

# Діапазонний запит для дерева
def range_query_correct_tree(tree, min_price, max_price):
    result = []
    for key, value in tree.items(min_price, max_price):  # Отримуємо всі пари ключ-значення
            result.append((key, value))
    return result
    
# Діапазонний запит для словника
def range_query_dict(item_dict, min_price, max_price):
    result = []
    for key, value in item_dict.items():
        price = value['Price']
        if min_price <= price <= max_price:
            result.append((key, value))
    return result

# Порівняння часу виконання
def compare_time(min_price, max_price):
    # Використовуємо timeit для вимірювання часу
    tree_time = timeit.timeit(lambda: range_query_tree(tree, min_price, max_price), number=100)
    correct_tree_time = timeit.timeit(lambda: range_query_correct_tree(correct_tree, min_price, max_price), number=100)
    dict_time = timeit.timeit(lambda: range_query_dict(item_dict, min_price, max_price), number=100)

    # Виводимо загальний час для кожної структури
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Correct OOBTree: {correct_tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

# Визначаємо діапазон цін для порівняння
min_price = 100
max_price = 500

# Викликаємо функцію для порівняння часу
compare_time(min_price, max_price)


