import hashlib 
import json 
import time 
import sys
import io

# Настройка кодировки для корректного вывода русских буква
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
      
        self.index = index
        
        self.timestamp = timestamp
        
        self.data = data
       
        self.previous_hash = previous_hash

        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # данные 
        block_info = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
        }

        block_string = json.dumps(block_info, sort_keys=True, ensure_ascii=False).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

def create_blockchain(): 
    # Здесь будет храниться вся цепочка блоков
    chain = []
    first_block = Block(0, time.time(), "Стартовый блок", "0")
    chain.append(first_block)
    # Создаём ещё 4 блока
    for index in range(1, 5):
        text = f"Данные внутри блока номер {index}"
        new_block = Block(index, time.time(), text, chain[-1].hash)
        chain.append(new_block)
    return chain

def check_blockchain(chain):
    
    for index in range(1, len(chain)):
        current_block = chain[index]
        previous_block = chain[index - 1]
        #  Проверяем, что сохранённый хеш совпадает с пересчитанным.
        if current_block.hash != current_block.calculate_hash():
            print(f"Ошибка: у блока {current_block.index} изменились данные или хеш")
            return False
        #  Проверяем, что блок правильно ссылается на предыдущий блок.
        if current_block.previous_hash != previous_block.hash:
            print(f"Ошибка: блок {current_block.index} неправильно связан с предыдущим")
            return False
    # Проверим нулевой блок, вдруг в нём тоже что-то поменяли.
    if chain[0].hash != chain[0].calculate_hash():
        print("Ошибка: нулевой блок был изменён")
        return False
    return True

def print_blockchain(chain):
    for block in chain:
        print("-" * 70)
        print("Номер блока:", block.index)
        print("Время создания:", block.timestamp)
        print("Данные:", block.data)
        print("Хеш прошлого блока:", block.previous_hash)
        print("Хеш блока:", block.hash)

def demo():
    blockchain = create_blockchain()
    print("ГОТОВАЯ ЦЕПОЧКА ИЗ 5 БЛОКОВ")
    print_blockchain(blockchain)
    print("\nПроверка целостности цепочки:", check_blockchain(blockchain))
    print("\nПробуем испортить данные во втором блоке...")
    blockchain[2].data = "Кто-то поменял данные блока"
    print("Проверка после изменения:", check_blockchain(blockchain))

if __name__ == "__main__":
    demo()