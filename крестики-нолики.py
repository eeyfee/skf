# Создание словаря отвечающего за заполнение val при его заполнении в начале новой игры
original_val = {'11':"-", '12':"-", '13':"-", '21':"-",
     '22':"-", '23':"-", '31':"-", '32':"-", '33':"-"}

# Заполнение словаря для самого первого запуска
val = original_val.copy()


def stopping_conditions():  # функция проверки завершенности игры

    for game in [(val['11'], val['12'], val['13']),
                 (val['21'], val['22'], val['23']),
                 (val['31'], val['32'], val['33']),
                 (val['11'], val['21'], val['31']),
                 (val['12'], val['22'], val['32']),
                 (val['13'], val['23'], val['33']),
                 (val['11'], val['22'], val['33']),
                 (val['13'], val['22'], val['31'])]:
        if game == ("X", "X", "X") or game == ("O", "O", "O"):
            return False

    if "-" not in val.values():
        return "draw"  

    return True 

# функция вывода игрового поля
def playing_field():
    print(f"  1 2 3")
    print(f"1 {val['11']} {val['12']} {val['13']}")
    print(f"2 {val['21']} {val['22']} {val['23']}")
    print(f"3 {val['31']} {val['32']} {val['33']}")


def game_process():

    global val
    sum_moves = 0

    while stopping_conditions() == True: # пока нет ничьей и нет победителя
        position = str(input("укажите позицию: "))
        if position == "стоп":
            break
        while position not in val.keys() or val[position] in ["X", "O"]: # проверка корректности введенных данных
            position = str(input("пожалуйста, укажите разрешенную позицию: "))

        if sum_moves % 2 == 0:
            val[position] = "X"
        else:
            val[position] = "O"
        playing_field()
        sum_moves +=1

        if stopping_conditions() == False: # далее определение победителя
            if sum_moves % 2 != 0:
                player = "первого"
            else:
                player = "второго"
            print(f"победа {player} игрока")
            print()
            break
        if stopping_conditions() == "draw":
            print("Ничья")
            break
    start()
        


def start():
    
    global val
    global sum_moves
    val = original_val.copy() # при каждой новой игре словарь val будет принимать изначальный вид
    sum_moves = 0 # аналагично и с sum_moves

    agr = input("Желаете ли вы начать игру (да/нет): ")
    if agr == "да":
        playing_field()
        game_process() 
    elif agr == "нет":
        print("игра окончена")
    else:
        print("Введите один из предложенных вариантов") # проверка корректности введенных данных
        start()


print("для преждевременного выхода из игры вместо позиции напишите слово 'стоп' ")
print()
start()

