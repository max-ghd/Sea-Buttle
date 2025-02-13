from tkinter import * # створення робочої зони морського бою
from tkinter import messagebox # для закриття робочої зони використали імпорт меседжбокс
import time
import random

tk = Tk() # робоча зона
work = True # відстеження роботи робочої зони, тобто, перевіряє, працює вікно це чи ні

size_x = 600
size_y = 600# розміри робочої зони

s_line_x = s_line_y = 10  # створення змінних  10 клітинок для поля гри

step_x = size_x // s_line_x  # шаг по горизонталі
step_y = size_y // s_line_y  # шаг по вертикалі
size_x = step_x * s_line_x
size_y = step_y * s_line_y


delta_menu_x = 4
menu_x = step_x * delta_menu_x # зробили вільне поле для кнопок, ми цю змінну за допомогою додавання розширили по горизонталі додоючи її на size_x

menu_y = 40 # створили вільний простір знизу, щоб було зрозуміліше де чиє поле знаходиться



ships = s_line_x // 2  # визначаємо максимальну кількість кораблів
ship_len1 = s_line_x // 4  # довжина першого типа корабля
ship_len2 = s_line_x // 3  # довжина другого типа корабля
ship_len3 = s_line_x // 2  # довжина третього типа корабля

enemy1 = [[0 for i in range(s_line_x + 1)] for i in range(s_line_y + 1)]# за допомогою  цикла фор, можна динамічно визначити список для наших об'єктів enemy1, тобто   ми будемо отримувати той розмір списку для розміру кораблів
enemy2 = [[0 for i in range(s_line_x + 1)] for i in range(s_line_y + 1)]
list_id = []  # список відрисованих об'єктів


klick1 = [[-1 for i in range(s_line_x)] for i in range(s_line_y)] # список, куди ми натиснули мишкою
klick2 = [[-1 for i in range(s_line_x)] for i in range(s_line_y)]

boom = [[0 for i in range(s_line_x)] for i in range(s_line_y)] # список того, що ми попали по кораблю супротивника

ships_list =[] # список кораблів гравця 1 і 2



def on_closing():  # функція для закриття програми
    global work # Використав цю змінну через глобал, тим самим указуючи, що вона головна, бо без глобала, ця змінна прияйнла у функціїї іншні значення, а у середовище не передала б свої значення
    if messagebox.askokcancel("Вихід з гри", "Бажаете вийти з гри?"): # Буде задаватись питання на момент виходу з гри
        work = False  # робимо нове значення, щоб можна було б вийти з гри, без глобальної змінної, ця змінна залишитьс у функції і не зможе передатись у код таким чином не закриється програма
        tk.destroy() # Функція виходу з гри


tk.protocol("WM_DELETE_WINDOW", on_closing) # визначення того, що ми будемо робити на момент того, що ми будемо робити після закриття вікна
tk.title("Sea Fight")  # Назва вікна
tk.resizable(0, 0) # Функція, що робить так, щоб не можна було змінити розмір вікна
tk.wm_attributes("-topmost", 1) # атрибут, що робить вікно  на поверхні всіх інших вікон
window = Canvas(tk, width=size_x + menu_x + size_x, height=size_y + menu_y, bd=0, highlightthickness=0) # роюимо відрисовку за допомогою Канвас
window.create_rectangle(0, 0, size_x, size_y, fill="lightblue") # створення прямокутника 
window.create_rectangle(size_x + menu_x, 0, size_x + menu_x + size_x, size_y, fill="lightblue") # створення поля для 2 гравця
window.pack() # додавання Canvas у вікно
tk.update()


def table(pole2 = 0): # створення функції, для того, щоб  створити поле з клітинок, також створили необов'язковий параметр для другого поля для переміщення ліній на друге поле
    for i in range(0, s_line_x + 1): # цей цикл відрисовує лінії які ми задали в s_line_x по горизонталі
        window.create_line(pole2+ step_x * i, 0, pole2 + step_x * i, size_y)
    for i in range(0, s_line_y + 1): # цей цикл відрисовує лінії які ми задали в  s_line_y по вертикалі
        window.create_line(pole2, step_y * i, pole2 + size_x, step_y * i)


table()
table(size_x + menu_x) # визиваємо другий раз функцію, для того, щоб перемістити лінії


#створюємо підписи полей і задаємо координати для підписей
table0 = Label(tk, text="Гравець 1", font=("Verdana 11 normal roman", 15))
table0.place(x = size_x//2 - table0.winfo_reqwidth()//2, y = size_y+3)
table1 = Label(tk, text="Гравець 2", font=("Verdana 11 normal roman", 15))
table1.place(x = size_x + menu_x + size_x // 2 - table1.winfo_reqwidth()//2, y = size_y + 3)

table0.configure(bg="yellow") # cтворили фон для підписів гравців
table1.configure(bg="yellow") 



def button_show_enemy1(): # кнопка показу замальованих кораблів супротивника в синій колір
    for i in range(0, s_line_x):
        for j in range(0, s_line_y):
            if enemy1[j][i] > 0:
                color = "blue"
                if klick1[j][i] != -1: # якщо об'єкт був вже найденим, то він змінює колір на темніший
                    color = "darkred"
                id = window.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y, fill=color)
                list_id.append(id)


def button_show_enemy2(): # кнопка показу замальованих кораблів супротивника в синій колір
    for i in range(0, s_line_x):
        for j in range(0, s_line_y):
            if enemy2[j][i] > 0:
                color = "blue"
                if klick2[j][i] != -1: # якщо об'єкт був вже найденим, то він змінює колір на темніший
                    color = "darkred"
                id = window.create_rectangle(size_x + menu_x + i * step_x, j * step_y, size_x + menu_x + i * step_x + step_x, j * step_y + step_y, fill=color)
                list_id.append(id)


def button_begin_again(): # ця кнопка буде чистити поле, у функцію треба написати список, щоб його видалити з поля
    global list_id
    global klick1, klick2
    global boom
    global enemy1, enemy2
    for element in list_id:
        window.delete(element)
    list_id = []
    generate_ship_list()
    print(ships_list)
    enemy1  = generate_enemy()
    enemy2 = generate_enemy() # додав цю функцію, щоб знову згенерувати нові кораблі
    klick1 = [[-1 for i in range(s_line_x)] for i in range(s_line_y)] # після наших натискань на поле, наш список буде оновлюватись, для того, щоб після натискання на кноку розпочати заново, можна було зіграти ще раз
    klick2 = [[-1 for i in range(s_line_x)] for i in range(s_line_y)]
    boom = [[0 for i in range(s_line_x)] for i in range(s_line_y)]



knopka0 = Button(tk, text="Показати кораблі Гравця 1", command=button_show_enemy1) #створили першу кнопку, щоб показати кораблі гравця 1
knopka0.place(x=size_x+20, y = 30)# встановили координати кнопки 

knopka1 = Button(tk, text="Показати кораблі Гравця 2", command=button_show_enemy2)
knopka1.place(x = size_x + 20, y = 70)

knopka2 = Button(tk, text="Розпочати заново", command=button_begin_again) #створили першу кнопку, щоб показати розпочати заново
knopka2.place(x=size_x + 20, y=110) # встановили координати кнопки 


def point(x, y): # в цій функції відрисовка того, якщо ми попали, чи не попали
    #print(enemy1[y][x])
    if  enemy1[y][x] == 0: # якщо ми не попали, відрисується червоний кружочок
        color = "red"
        id1 = window.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        list_id.append(id1) # після того, коли ми натиснемо кнопку розпочати заново, ці кружочки пропадуть
    if enemy1[y][x] > 0: # якщо попали, відрисується крестик 
        color = "green"
        id1 = window.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x, y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = window.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y, x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_id.append(id1)# так само пропадуть крестики, після оновлення 
        list_id.append(id2)

def point2(x, y, pole2=size_x + menu_x):
    # print(enemy_ships1[y][x])
    if enemy2[y][x] == 0:
        color = "red"
        id1 = window.create_oval(pole2+ x * step_x, y * step_y, pole2 + x * step_x + step_x, y * step_y + step_y, fill=color)
        list_id.append(id1)
        
    
    if enemy2[y][x] > 0:
        color = "green"
        id1 = window.create_rectangle(pole2 + x * step_x, y * step_y + step_y // 2 - step_y // 10, pole2 + x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = window.create_rectangle(pole2 + x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      pole2 + x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_id.append(id1)
        list_id.append(id2)

def show_winner(player):
    messagebox.showinfo("Перемога!", f"Гравець {player} переміг!")

def winner(x, y): # перевірка на перемогу і оновлює список boom 
    win = True
    
    for i in range(0, s_line_x):
        for j in range(0, s_line_y):
            if enemy1[j][i] > 0: # Якщо у всіх елементамх, де знаходиться корабель супротивника, куди ми натиснули, тоді ми перемогли
                if klick1[j][i] == -1:
                    win = False
    if win:
        show_winner(2)
    #print(win)
    return win

def winner2(x, y): # перевірка на перемогу і оновлює список boom для гравця 2 
    win = True
    
    for i in range(0, s_line_x):
        for j in range(0, s_line_y):
            if enemy2[j][i] > 0: # Якщо у всіх елементамх, де знаходиться корабель супротивника, куди ми натиснули, тоді ми перемогли
                if klick2[j][i] == -1:
                    win = False
    if win:
        show_winner(1)
    #print(win)
    return win
    

def myszka(event):
    global klick1, klick2
    type = 0  # змінна для того, щоб зберігати наше натискання на кнопку, яку ми відтворили, тобто 0 буде для нашої лівої кнопки миші
    if event.num == 3:
        type = 1  # а 3 буде для правої кнопки миші
    
    
    mouse_x = window.winfo_pointerx() - window.winfo_rootx()# визначення координатів мишки по х всередині клітинок, для того, щоб  потім було легше працювати зі списками
    mouse_y = window.winfo_pointery() - window.winfo_rooty()# визначення координатів мишки по у всередині клітинок, для того, щоб  потім було легше працювати зі списками
    
    game_x = mouse_x // step_x  # точні координати ігрового поля по горизонталі, для того, щоб визначити в яку саме частину ми натиснули
    game_y = mouse_y // step_y # точні координати ігрового поля по вертикалі, для того, щоб визначити в яку саме частину ми натиснули
    #print(game_x, game_y, "type:", type)


    if game_x < s_line_x and game_y < s_line_y: # перевірка кліку в першій ігровій  області
        if klick1[game_y][game_x] == -1:# перевірка того, чи натискали ми на поле чи ні, якщо так, то вже не список поповнюватись не буде, щоб не займати пам'ять на комп'ютері
            klick1[game_y][game_x] = type # записується тип ігрового кліку
            point(game_x, game_y) # відрисовка кружочка чи крестика, куди ми попали
            if winner(game_x, game_y): # перевірка перемоги за допомогою функції winner
                print("WIN Player 2!")
                klick1 = [[10 for i in range(s_line_x)] for i in range(s_line_y)]# блокування натискань по полю
                klick2 = [[10 for i in range(s_line_x)] for i in range(s_line_y)]

        #print(len(list_id))
    
    # друге ігрове поле
    if game_x >= s_line_x + delta_menu_x and game_x < s_line_x + s_line_x + delta_menu_x and game_y < s_line_y: # перевірка кліку в першій ігровій  області
        #print("ok")
        if klick2[game_y][game_x - s_line_x - delta_menu_x] == -1:# перевірка того, чи натискали ми на поле чи ні, якщо так, то вже не список поповнюватись не буде, щоб не займати пам'ять на комп'ютері
            klick2[game_y][game_x - s_line_x - delta_menu_x] = type # записується тип ігрового кліку
            point2(game_x - s_line_x - delta_menu_x, game_y)
            if winner2(game_x, game_y):
                print("WIN Player 1!")
                klick1 = [[10 for i in range(s_line_x)] for i in range(s_line_y)] # блокування натискань по полю
                klick2 = [[10 for i in range(s_line_x)] for i in range(s_line_y)]

window.bind_all("<Button-1>", myszka)  #для нажаття на ліву кнопки мишки
window.bind_all("<Button-3>", myszka)  #для нажаття на праву кнопки мишки



def generate_ship_list():
    global ships_list # список довжин кораблів, для розкидання кораблів по всій зоні
    ships_list = []


    # генерація випадкових довжин кораблів
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3]))




def generate_enemy(): # функція для генерування кораблі ворогів

    global ships_list
    enemy = [] # створив глобальну зміну, для того, щоб вона не залишалась всередині функції і не створювалась копія
    
    

    # підррахунок сумарної довжини кораблів, при генерації кораблів, воно може один на одного накластись, а ця команда робить, так, щоб таких випадків не було
    sum_ships = sum(ships_list)
    sum_enemy = 0 # команда для підрахунку кораблів супротивника 

    while sum_enemy != sum_ships: # генерація розположення кораблів супортивника
        # обнулюємо массив кораблей супротивника
        enemy = [[0 for i in range(s_line_x + 1)] for i in range(s_line_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника

        for i in range(0, ships): #цикл для розположення кораблів по гориз та вертикалі
            len = ships_list[i]
            rozpolozenia = random.randrange(1, 3) # випадкове розположення корабля по вертикалі це 2 чи горизонталі це 2

            ship_x = random.randrange(0, s_line_x)# розположення корабля по координатам х
            if ship_x + len > s_line_x: # умова для того, щоб корабель вліз у поле по координатам х
                ship_x = ship_x - len

            # такі самі маніпуляції і для координат у
            ship_y = random.randrange(0, s_line_y)
            if ship_y + len > s_line_y:
                ship_y = ship_y - len

            
            if rozpolozenia == 1: # умова для горизонтального розположення
                if ship_x + len <= s_line_x:# перевірка того, щоб не вийти за кордон поля

                    for j in range(0, len):
                        try: # перевіряє ліву, праву, нижню праву і ліву, верхню ліву і праву сусідню клітинку поточного розташування корабля
                            check_enemy = 0
                            check_enemy = enemy[ship_y][ship_x - 1] + \
                                               enemy[ship_y][ship_x + j] + \
                                               enemy[ship_y][ship_x + j + 1] + \
                                               enemy[ship_y + 1][ship_x + j + 1] + \
                                               enemy[ship_y - 1][ship_x + j + 1] + \
                                               enemy[ship_y + 1][ship_x + j] + \
                                               enemy[ship_y - 1][ship_x + j]
                            if check_enemy == 0:  # якщо немає в сусідніх клітинках супротивника, то будемо записувати номер нашогго корабля
                                enemy[ship_y][ship_x + j] = i + 1 # тут записується номер нашого коробля
                        except Exception: # якщо буде виняток, то ми нічого не робимо
                            pass
            # такі самі розположення і по вертикалі
            if rozpolozenia == 2:
                if ship_y + len <= s_line_y:
                    for j in range(0, len):
                        try:
                            check_enemy = 0
                            check_enemy = enemy[ship_y - 1][ship_x] + \
                                               enemy[ship_y + j][ship_x] + \
                                               enemy [ship_y + j + 1][ship_x] + \
                                               enemy[ship_y + j + 1][ship_x + 1] + \
                                               enemy [ship_y + j + 1][ship_x - 1] + \
                                               enemy[ship_y + j][ship_x + 1] + \
                                               enemy[ship_y + j][ship_x - 1]
                            
                            if check_enemy == 0:
                                enemy[ship_y + j][ship_x] = i + 1 
                        except Exception:
                            pass

        # підрахунок ворожих клітинок
        sum_enemy = 0
        # проходимо по всіх клітинках ігрового поля на наявність ворога
        for i in range(0, s_line_x):
            for j in range(0, s_line_y):
                if enemy[j][i] > 0: # якщо є ворог
                    sum_enemy = sum_enemy + 1 # додаємо до лічильника

        # print(sum_1_enemy)
        # print(ships_list)
        #print(enemy1)
    return enemy
generate_ship_list()
#print(ships_list)
enemy1  = generate_enemy()
enemy2 = generate_enemy()
# print("***************************")
# print(enemy1)
# print("***************************")
# print(enemy2)
# print("***************************")

generate_enemy()

while work: # нескінчений цикл для роботи нашої гри
    if work:
        tk.update_idletasks() # якщо наша програма запущена, то ми завжди будемо її оновлювати за допомогою апдейт
        tk.update()
    time.sleep(0.005)# затримка для оновлення