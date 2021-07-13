import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import threading
import time
import random
import datetime

city_data = []
city_count = 0
city_distance = []
exe_time = 1            # 최대 실행 시간(초)
b_running = False       # 실행 중 신호

def CalcDistance():
    for i in range(city_count):
        city_distance.append([0 for i in range(city_count)])

    for i in range(city_count - 1):
        for j in range(i + 1, city_count):
            pt1 = city_data[i]
            pt2 = city_data[j]
            distance = int(math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2))
            city_distance[i][j] = distance
            city_distance[j][i] = distance

    #print(city_distance)

def ReadData(filename):
    global city_count
    infile = open(filename, "r")

    line = infile.readline().strip()
    city_count = int(line)

    for i in range(city_count):
        line = infile.readline().strip()
        line = line.split()
        line = [eval(x) for x in line]
        x = line[1]
        y = line[2]
        city_data.append([x, y])

    infile.close()

    CalcDistance()

def DrawCircle(canvas, pt):
    canvas.create_oval(pt[0] - 3, pt[1] - 3, pt[0] + 3, pt[1] + 3, fill="black")

def DrawLine(canvas, pt1, pt2, tag):
    canvas.create_line(pt1[0], pt1[1], pt2[0], pt2[1], tags=tag)

def DrawCityNumber(canvas, pt, number):
    canvas.create_text(pt[0], pt[1] - 10, text=number)

def InitDraw():
    canvas.delete(tk.ALL)

    for i in range(city_count):
        pt = city_data[i]
        DrawCircle(canvas, pt)
        DrawCityNumber(canvas, pt, str(i))

def DrawTSP(old_order, order):
    old_lines = [(0, old_order[0])]
    for i in range(len(order) - 1):
        old_lines.append((old_order[i], old_order[i + 1]))
        old_lines.append((old_order[i + 1], old_order[i]))
    old_lines.append((old_order[len(order) - 1], 0))

    lines = [(0, order[0])]
    for i in range(len(order) - 1):
        lines.append((order[i], order[i+1]))
        lines.append((order[i+1], order[i]))
    lines.append((order[len(order) - 1], 0))

    if (0, old_order[0]) not in lines:
        canvas.delete("0_" + str(old_order[0]))
    for i in range(len(order) - 1):
        if (old_order[i], old_order[i+1]) not in lines:
            canvas.delete(str(old_order[i]) + "_" + str(old_order[i + 1]))
            canvas.delete(str(old_order[i + 1]) + "_" + str(old_order[i]))
    if (old_order[len(order) - 1], 0) not in lines:
        canvas.delete(str(old_order[len(order) - 1]) + "_0")

    if (0, order[0]) not in old_lines:
        DrawLine(canvas, city_data[0], city_data[order[0]], "0_" + str(order[0]))
    for i in range(len(order) - 1):
        if (order[i], order[i+1]) not in old_lines:
            DrawLine(canvas, city_data[order[i]], city_data[order[i + 1]], str(order[i]) + "_" + str(order[i + 1]))
    if (order[len(order) - 1], 0) not in old_lines:
        DrawLine(canvas, city_data[order[len(order) - 1]], city_data[0], str(order[len(order) - 1]) + "_0")

    window.update()
    #time.sleep(0.5)

def DrawTSP_First(order):
    #InitDraw()

    DrawLine(canvas, city_data[0], city_data[order[0]], "0_" + str(order[0]))
    for i in range(len(order) - 1):
        DrawLine(canvas, city_data[order[i]], city_data[order[i + 1]], str(order[i]) + "_" + str(order[i + 1]))
    DrawLine(canvas, city_data[order[len(order) - 1]], city_data[0], str(order[len(order) - 1]) + "_0")

    window.update()
    #time.sleep(0.5)

def GetDistance(order):
    distance = city_distance[0][order[0]]
    for i in range(len(order) - 1):
        distance += city_distance[order[i]][order[i + 1]]
    distance += city_distance[order[len(order) - 1]][0]
    return distance

def TimeOver(start_time):
    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    lbl_cur_exe_time.config(text=str(int(elapsed)))
    if elapsed >= exe_time:
        return True
    else:
        return False

def NextPermutation(a):
    """Generate the lexicographically next permutation inplace.

    https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
    Return false if there is no next permutation.
    """
    # Find the largest index i such that a[i] < a[i + 1]. If no such
    # index exists, the permutation is the last permutation
    for i in reversed(range(len(a) - 1)):
        if a[i] < a[i + 1]:
            break  # found
    else:  # no break: not found
        return False  # no next permutation

    # Find the largest index j greater than i such that a[i] < a[j]
    j = next(j for j in reversed(range(i + 1, len(a))) if a[i] < a[j])

    # Swap the value of a[i] with that of a[j]
    a[i], a[j] = a[j], a[i]

    # Reverse sequence from a[i + 1] up to and including the final element a[n]
    a[i + 1:] = reversed(a[i + 1:])
    return True

def ExhaustiveSearch():
    cities = [i for i in range(1, city_count)]

    best_distance = GetDistance(cities)
    print(best_distance)
    list_result.insert(1.0, "time : 0, " + "distance : " + str(best_distance) + ", " + "order : " + str(cities) + "\n")
    DrawTSP_First(cities)
    old_cities = cities.copy()

    start_time = datetime.datetime.now()

    while True:
        ok = NextPermutation(cities)
        if not ok:
            break

        cur_distance = GetDistance(cities)
        if cur_distance < best_distance:
            best_distance = cur_distance
            print(best_distance)
            elapsed = int((datetime.datetime.now() - start_time).total_seconds())
            list_result.insert(1.0, "time : " + str(elapsed) + ", " + "distance : " + str(best_distance) + ", " + "order : " + str(cities) + "\n")

            DrawTSP(old_cities, cities)
            old_cities = cities.copy()

        if TimeOver(start_time):
            return "시간 초과"
        if not b_running:
            return "강제 종료"

    return "실행 완료"

# Steepest-ascent Hill-climbing Search
# 현재해로부터 모든 도시 쌍들을 교체하여 현재해보다 같거나 더 좋은 해가 있으면 이동함
# 현재해와 다음해 사이에 거리가 같다면(A, B 해 사이에 반복) 지정된 실행 시간까지 실행될 수 있음
def SteepestAscentHillClimbingSearch():
    cities = [i for i in range(1, city_count)]
    random.shuffle(cities)

    best_distance = GetDistance(cities)
    print(best_distance)
    list_result.insert(1.0, "time : 0, " + "distance : " + str(best_distance) + ", " + "order : " + str(cities) + "\n")
    DrawTSP_First(cities)
    old_cities = cities.copy()

    start_time = datetime.datetime.now()
    cur_best_distance = best_distance

    while True:
        cur_best_solutions = []                     # 거리가 같은 해가 여러 개인 경우 저장 & 무작위로 선택

        for i in range(0, city_count - 2):          # 도시가 5개면 0번 도시를 제외하고 4개 도시에 대해 (0~2) 각각에 대해
            for j in range(i + 1, city_count - 1):    # (i + 1, 3)까지의 모든 쌍에 대한 swap 실행
                new_cities = cities.copy()
                new_cities[i], new_cities[j] = new_cities[j], new_cities[i]
                cur_distance = GetDistance(new_cities)

                if cur_distance <= cur_best_distance:   # best 해와 같거나 더 좋은 해가 발견되었음
                    cur_best_solutions.append(new_cities)
                    if cur_distance < cur_best_distance:    # 더 좋은 해가 발견되었음
                        cur_best_distance = cur_distance
                        cur_best_solutions = []     # 가장 좋은 해 하나만 저장
                        cur_best_solutions.append(new_cities)

        if len(cur_best_solutions) > 0:     # 같거나 더 좋은 해 발견
            cities = random.choice(cur_best_solutions)
            if cur_best_distance < best_distance:
                best_distance = cur_best_distance
                print(best_distance)
                elapsed = int((datetime.datetime.now() - start_time).total_seconds())
                list_result.insert(1.0, "time : " + str(elapsed) + ", " + "distance : " + str(best_distance) + ", " + "order : " + str(cities) + "\n")
                DrawTSP(old_cities, cities)
                old_cities = cities.copy()
        else:       # 같거나 더 좋은 해가 없으면 종료
            break

        if TimeOver(start_time):
            return "시간 초과"
        if not b_running:
            return "강제 종료"

    return "실행 완료"

def RandomRestartSteepestAscentHillClimbingSearch():
    ori_cities = [i for i in range(1, city_count)]
    random.shuffle(ori_cities)
    
    start_time = datetime.datetime.now()
    while not TimeOver(start_time):
        cities = ori_cities
        best_distance = GetDistance(cities)
        print(best_distance)
        list_result.insert(1.0, "time : 0, " + "distance : " + str(best_distance) + ", " + "order : " + str(cities) + "\n")
        DrawTSP_First(cities)
        old_cities = cities.copy()

        ori_start_time = datetime.datetime.now()
        cur_best_distance = best_distance

        while True:
            cur_best_solutions = []                     # 거리가 같은 해가 여러 개인 경우 저장 & 무작위로 선택

            lst = [i for i in range(0, city_count - 2)]
            random.shuffle(lst)
            for idx, i in enumerate(lst[:-1]):          # 도시가 5개면 0번 도시를 제외하고 4개 도시에 대해 (0~2) 각각에 대해
                for j in range(idx + 1, len(lst)-1):    # (i + 1, 3)까지의 모든 쌍에 대한 swap 실행
                    new_cities = cities.copy()
                    new_cities[i], new_cities[lst[j]] = new_cities[lst[j]], new_cities[i]
                    cur_distance = GetDistance(new_cities)

                    if cur_distance <= cur_best_distance:   # best 해와 같거나 더 좋은 해가 발견되었음
                        cur_best_solutions.append(new_cities)
                        if cur_distance < cur_best_distance:    # 더 좋은 해가 발견되었음
                            cur_best_distance = cur_distance
                            cur_best_solutions = []     # 가장 좋은 해 하나만 저장
                            cur_best_solutions.append(new_cities)

            if len(cur_best_solutions) > 0:     # 같거나 더 좋은 해 발견
                cities = random.choice(cur_best_solutions)
                if cur_best_distance < best_distance:
                    best_distance = cur_best_distance
                    print(best_distance)
                    elapsed = int((datetime.datetime.now() - ori_start_time).total_seconds())
                    list_result.insert(1.0, "time : " + str(elapsed) + ", " + "distance : " + str(best_distance) + ", " + "order : " + str(cities) + "\n")
                    DrawTSP(old_cities, cities)
                    old_cities = cities.copy()
            else:       # 같거나 더 좋은 해가 없으면 종료
                break

            if TimeOver(start_time):
                return "시간 초과"
            if not b_running:
                return "강제 종료"

        if TimeOver(start_time):
            return "시간 초과"
        if not b_running:
            return "강제 종료"

        list_result.insert(1.0, "\n================Restart================\n")

    return "실행 완료"

# First-choice Hill-climbing Search
# 현재해로부터 이웃해 하나를 만들어 더 좋거나 같으면 이동함
# 지정된 실행 시간까지 실행됨
def FirstChoiceHillClimbingSearch():
    cities = [i for i in range(1, city_count)]
    random.shuffle(cities)

    best_distance = GetDistance(cities)
    print(best_distance)
    list_result.insert(1.0, "time : 0, " + "distance : " + str(best_distance) + ", " + "order : " + str(cities) + "\n")
    DrawTSP_First(cities)
    old_cities = cities.copy()

    start_time = datetime.datetime.now()

    while True:
        index1 = random.randint(0, city_count - 2)
        index2 = random.randint(0, city_count - 2)
        new_cities = cities.copy()
        new_cities[index1], new_cities[index2] = new_cities[index2], new_cities[index1]
        cur_distance = GetDistance(new_cities)

        if cur_distance <= best_distance:
            cities = new_cities
            if cur_distance < best_distance:
                best_distance = cur_distance
                print(best_distance)
                elapsed = int((datetime.datetime.now() - start_time).total_seconds())
                list_result.insert(1.0, "time : " + str(elapsed) + ", " + "distance : " + str(best_distance) + ", " + "order : " + str(cities) + "\n")
                DrawTSP(old_cities, cities)
                old_cities = cities.copy()

        if TimeOver(start_time):
            return "시간 초과"
        if not b_running:
            return "강제 종료"

    return "실행 완료"

def Run():
    global exe_time, b_running
    btn_init['state'] = tk.DISABLED
    btn_run['state'] = tk.DISABLED
    btn_run['text'] = "수행 중 ..."
    btn_cancel['state'] = tk.NORMAL
    b_running = True

    method = cbo_method.get()      # Exhaustive Search, First-choice Hill-climbing Search
    exe_time = int(cbo_exe_time.get())

    if method == "Exhaustive Search":
        msg = ExhaustiveSearch()
    elif method == "Steepest-ascent Hill-climbing Search":
        msg = SteepestAscentHillClimbingSearch()
    elif method == "RandomRestartSteepestAscentHillClimbing Search":
        msg = RandomRestartSteepestAscentHillClimbingSearch()
    elif method == "First-choice Hill-climbing Search":
        msg = FirstChoiceHillClimbingSearch()

    print("끝")
    btn_init['state'] = tk.NORMAL
    #btn_run['state'] = tk.NORMAL
    btn_run['text'] = "시작"
    btn_cancel['state'] = tk.DISABLED
    b_running = False

    messagebox.showinfo("Information", msg)

def RunCancel():
    global b_running
    b_running = False

def InitData():
    global city_count
    city_count = int(cbo_city_count.get())
    InitDraw()
    list_result.delete("1.0","end")
    btn_run['state'] = tk.NORMAL
    lbl_cur_exe_time.config(text="0")

window = tk.Tk()
canvas = tk.Canvas(window, width=600, height=600, bg="white")
canvas.pack(side = tk.LEFT, padx = 3, pady = 3)
frame1 = tk.Frame(window)
frame1.pack(fill = tk.X, padx = 3, pady = 3)
lbl_city_count = tk.Label(frame1, text = "도시 개수 :", width = 11, height = 2)
lbl_city_count.pack(side = tk.LEFT)
cbo_city_count = ttk.Combobox(frame1, values=[i for i in range(5, 501)])
cbo_city_count.pack(expand = 1, fill = tk.X, padx = 5)
cbo_city_count.set(10)
frame2 = tk.Frame(window)
frame2.pack(fill = tk.X, padx = 3, pady = 3)
lbl_method = tk.Label(frame2, text = "탐색 기법 :", width = 11, height = 2)
lbl_method.pack(side = tk.LEFT)
cbo_method = ttk.Combobox(frame2, values=["RandomRestartSteepestAscentHillClimbing Search", "Exhaustive Search", "Steepest-ascent Hill-climbing Search", "First-choice Hill-climbing Search"])
cbo_method.pack(expand = 1, fill = tk.X, padx = 5)
cbo_method.set("Exhaustive Search")
frame3 = tk.Frame(window)
frame3.pack(fill = tk.X, padx = 3, pady = 3)
lbl_exe_time = tk.Label(frame3, text = "실행 시간(초) :", width = 11, height = 2)
lbl_exe_time.pack(side = tk.LEFT)
cbo_exe_time = ttk.Combobox(frame3, values=[i for i in range(1, 3601)])
cbo_exe_time.pack(side = tk.LEFT, expand = 1, fill = tk.X, padx = 5)
lbl_cur_exe_time = tk.Label(frame3, text = "0", width = 6, height = 2)
lbl_cur_exe_time.pack(side = tk.LEFT)
cbo_exe_time.set(180)
btn_init = tk.Button(window, text = "초기화", width = 40, height = 2, command = InitData)
btn_init.pack(fill = tk.X, padx = 3, pady = 3)
btn_run = tk.Button(window, text = "시작", width = 40, height = 2, command = lambda : threading.Thread(target=Run).start())
btn_run.pack(fill = tk.X, padx = 3, pady = 3)
btn_run['state'] = tk.DISABLED
btn_cancel = tk.Button(window, text = "취소", width = 40, height = 2, command = RunCancel)
btn_cancel.pack(fill = tk.X, padx = 3, pady = 3)
btn_cancel['state'] = tk.DISABLED
lbl_result = tk.Label(window, text = "<<< Result >>>")
lbl_result.pack(fill = tk.X, padx = 3, pady = 3)
list_result = tk.Text(window, width = 40, wrap = "none")
list_result.pack(expand = 1, fill = tk.BOTH, padx = 3, pady = 3)

ReadData("tsp_data.txt")
window.mainloop()
