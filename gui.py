import os
import tkinter
import tkinter.font
import tkinter.ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import chromedriver_autoinstaller
import random
import os
import sys
import threading

driver = None

def num_random():
    random_num = random.uniform(2, 5)
    return round(random_num, 2)

def save(level, save_name):
    file = open(f'./{save_name}.txt', 'a', encoding='utf-8')
    for i, j in level:
        file.write(f"{i}, {j}명\n")
    file.close()

def following_list_1(level0, driver):
    people_list = []
    for i in level0:
        driver.execute_script("arguments[0].scrollIntoView();", i)
        try:
            if driver.find_element(By.CLASS_NAME, '_ab8w._ab94._ab97._ab9f._ab9m._ab9p._abc0._abcm').is_displayed() == True:
                cmd_box.insert(tkinter.INSERT,"팔로잉 로딩중\n")
                cmd_box.see(tkinter.END)
                sleep(3)
        except:
            pass
        following_id = i.find_element(By.CLASS_NAME, '_aacl._aaco._aacw._adda._aacx._aad7._aade').text.strip("인증됨\n")
        div = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div')
        people = div.find_elements(By.CLASS_NAME, '_ab8w._ab94._ab97._ab9f._ab9k._ab9p._ab9-._aba8._abcm')
        for j in people[len(level0):]:
            if j not in level0:
                level0.append(j)
            
        i_href = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.execute_script(f'window.open("{i_href}");')
        driver.switch_to.window(driver.window_handles[1])
        sleep(4)
        num = driver.find_elements(By.CLASS_NAME, '_ac2a')
        following_num = num[2].text
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        sleep(1)
        people_list.append((following_id, following_num))
    return tuple(set(tuple(people_list)))

def following_list_2(level1, driver, url):
    people_list = ()
    for i in level1:
        following_id, following_num = i
        try:
            driver.get(f'{url}{following_id}/following/')
            sleep(4)
            div = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div')
            people = div.find_elements(By.CLASS_NAME, '_ab8w._ab94._ab97._ab9f._ab9k._ab9p._ab9-._aba8._abcm')
            people_list += following_list_1(people)
        except:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            pass
        sleep(num_random())
    return tuple(set(people_list))

def following_list_3(level2, driver, url):
    people_list = ()
    for i in level2:
        following_id, following_num = i
        try:
            driver.get(f'{url}{following_id}/following/')
            sleep(4)
            div = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div')
            people = div.find_elements(By.CLASS_NAME, '_ab8w._ab94._ab97._ab9f._ab9k._ab9p._ab9-._aba8._abcm')
            people_list += following_list_1(people)
        except:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            pass 
        sleep(num_random())
    return tuple(set(people_list))

def step1(level0, driver, save_name, url):
    level1 = following_list_1(level0, driver)
    try:
        save(level1, save_name)
    except:
        cmd_box.insert(tkinter.INSERT,"알수없는 이유로 종료\n")
        cmd_box.see(tkinter.END)
        driver.close()    
    cmd_box.insert(tkinter.INSERT,"크롬 드라이버 종료\n")
    cmd_box.see(tkinter.END)
    driver.close()

def step2(level0, driver, save_name, url):
    level1 = following_list_1(level0, driver, url)
    level2 = following_list_2(level1, driver, url)
    try:
        save(level1+level2, save_name)
    except:
        cmd_box.insert(tkinter.INSERT,"알수없는 이유로 종료\n")
        cmd_box.see(tkinter.END)
        driver.close()
    cmd_box.insert(tkinter.INSERT,"크롬 드라이버 종료\n")
    cmd_box.see(tkinter.END)
    driver.close()

def step3(level0, driver, save_name, url):
    level1 = following_list_1(level0, driver, url)
    level2 = following_list_2(level1, driver, url)
    level3 = following_list_3(level2, driver, url)
    try:
        save(level1+level2+level3, save_name)
    except:
        cmd_box.insert(tkinter.INSERT,"알수없는 이유로 종료\n")
        cmd_box.see(tkinter.END)
        driver.close()
    cmd_box.insert(tkinter.INSERT,"크롬 드라이버 종료\n")
    cmd_box.see(tkinter.END)
    driver.close()

def start():
    cmd_box.insert(tkinter.INSERT,"시작\n")
    cmd_box.see(tkinter.END)
    global driver
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path) != True:
        cmd_box.insert(tkinter.INSERT,"크롬버전에 맞는 크롬드라이버 설치중...\n")
        cmd_box.see(tkinter.END)
        chromedriver_autoinstaller.install(True)
        cmd_box.insert(tkinter.INSERT,"크롬드라이버 설치완료\n")
        cmd_box.see(tkinter.END)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--privileged')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36")
    chrome_options.add_argument('lang=ko_KR')
    chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])

    url = 'https://www.instagram.com/'

    Id = input_ID.get("1.0", "end")
    if len(Id) == 0:
        cmd_box.insert(tkinter.INSERT,"아이디를 입력해주세요\n")
        cmd_box.see(tkinter.END)
        return
    Pw = input_PW.get()
    if len(Pw) == 0:
        cmd_box.insert(tkinter.INSERT,"패스워드를 입력해주세요\n")
        cmd_box.see(tkinter.END)
        return
    search_id = input_search_ID.get("1.0", "end")
    if len(Id) == 0:
        cmd_box.insert(tkinter.INSERT,"검색할 인스타 아이디를 입력해주세요\n")
        cmd_box.see(tkinter.END)
        return
    save_name = input_save_file.get("1.0", "end").strip("\n")
    if len(save_name) == 0:
        cmd_box.insert(tkinter.INSERT,"저장할 파일 이름을 입력해주세요\n")
        cmd_box.see(tkinter.END)
        return
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    sleep(2)

    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(Id)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(Pw)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]').click()
    sleep(4)

    while True:
        if driver.current_url != 'https://www.instagram.com/accounts/login/':
            cmd_box.insert(tkinter.INSERT,"로그인 성공\n")
            cmd_box.see(tkinter.END)
            break
        else:
            cmd_box.insert(tkinter.INSERT,"아이디와 패스워드를 다시 입력해주세요\n")
            cmd_box.see(tkinter.END)
            cmd_box.insert(tkinter.INSERT,"크롬 드라이버 종료\n")
            cmd_box.see(tkinter.END)
            driver.close()

    driver.get(f'{url}{search_id}/following/')
    sleep(4)
    div = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div')
    level0 = div.find_elements(By.CLASS_NAME, '_ab8w._ab94._ab97._ab9f._ab9k._ab9p._ab9-._aba8._abcm')

    
    if num_var.get() == 1:
        step1(level0, driver, save_name)
    elif num_var.get() == 2:
        step2(level0, driver, save_name)
    elif num_var.get() == 3:
        step3(level0, driver, save_name)
    else:
        cmd_box.insert(tkinter.INSERT,"단계를 선택해주세요\n")
        cmd_box.see(tkinter.END)
        return

def threading_start():
    start_t = threading.Thread(target=start)
    start_t.start()

def exit():
    try:
        cmd_box.insert(tkinter.INSERT,"크롬드라이버 종료\n")
        cmd_box.see(tkinter.END)
        driver.close()
    except:
        cmd_box.insert(tkinter.INSERT,"종료\n")
        cmd_box.see(tkinter.END)
        sys.exit()
    sys.exit()

# TTK 초기 설정
window=tkinter.Tk()
window.title("인스타그램 매크로")
window.geometry("570x350")
#window.iconbitmap('icon.ico')
window.resizable(False, False)

# [ 아이디, 비밀번호, 검색 아이디, 저장 파일 이름, 단계 ]
frame1 = tkinter.Frame(window, relief="solid", bd=1)
frame1.pack(side="top", fill="both", expand=False, padx=5, pady=5)

# [[ 아이디, 비밀번호, 검색 아이디, 저장 파일 이름 ]]
frame1_1=tkinter.Frame(frame1)
frame1_1.pack(side="left", fill="both", expand=True, padx=0, pady=0)

# [[[ 아이디, 비밀번호 ]]]
frame1_1_1=tkinter.Frame(frame1_1, relief="solid",bd=1)
frame1_1_1.pack(side="top", fill="both", expand=False, padx=5, pady=5)

lable_ID = tkinter.Label(frame1_1_1, text="ID")
lable_ID.grid(row=0, column=0)
input_ID = tkinter.Text(frame1_1_1, width=15, height=1) # 아이디 입력칸
input_ID.grid(row=0, column=1, padx= 7, pady = 5)

lable_PW = tkinter.Label(frame1_1_1, text="PW")
lable_PW.grid(row=0, column=2, pady = 5)
input_PW = tkinter.Entry(frame1_1_1, width=15, show="*") # 비밀번호 입력칸
input_PW.grid(row=0, column=3, padx= 7, pady = 5)

# [[[ 검색 아이디, 저장 파일 이름 ]]]
frame1_1_2=tkinter.Frame(frame1_1, relief="solid", bd=1)
frame1_1_2.pack(side="bottom", fill="both", expand=False, padx=5, pady=5)

lable_search_ID = tkinter.Label(frame1_1_2, text="검색 아이디")
lable_search_ID.grid(row=0, column=0)
input_search_ID = tkinter.Text(frame1_1_2, width=50, height=1) # 검색 아이디 입력칸
input_search_ID.grid(row=0, column=1, padx= 7, pady = 5)

lable_save_file = tkinter.Label(frame1_1_2, text="저장 파일 이름")
lable_save_file.grid(row=1, column=0)
input_save_file = tkinter.Text(frame1_1_2, width=50, height=1) # 저장 파일 이름 입력칸
input_save_file.grid(row=1, column=1, padx= 7, pady = 5)

# [[ 단계 ]]
frame1_2=tkinter.Frame(frame1, relief="solid", bd=1)
frame1_2.pack(side="right", fill="both", expand=False, padx=5, pady=5)

num_var = tkinter.IntVar()
num1_button = tkinter.Radiobutton(frame1_2, text="1단계", variable=num_var, value=1) # 1단계 체크 박스
num1_button.grid(row=0, column=0, padx=0, pady=2)

num2_var = tkinter.IntVar()
num2_button = tkinter.Radiobutton(frame1_2, text="2단계", variable=num_var, value=2) # 2단계 체크 박스
num2_button.grid(row=1, column=0, padx=0, pady=2)

num3_var = tkinter.IntVar()
num3_button = tkinter.Radiobutton(frame1_2, text="3단계", variable=num_var, value=3) # 3단계 체크 박스
num3_button.grid(row=2, column=0, padx=0, pady=2)

# [ 진행 상황, 저작권 표시, 실행, 종료 ]
frame2 = tkinter.Frame(window, relief="solid", bd=1)
frame2.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

# [[ 진행 상황 ]]
frame2_1 = tkinter.Frame(frame2)
frame2_1.pack(side="left", fill="both", expand=False, padx=1, pady=4)

cmd_box = tkinter.Text(frame2_1, width=45, height=15) # 진행 상황 박스 출력칸
cmd_box.grid(row=0, column=0, padx = 5, pady=5)
# cmd_box.configure(state='disabled')

# [[ 저작권 표시, 실행, 종료 ]]
frame2_2 = tkinter.Frame(frame2)
frame2_2.pack(side="right", fill="both", expand=True, padx=5, pady=5)

# [[[ 저작권 표시 ]]]
frame2_2_1 = tkinter.Frame(frame2_2, relief="solid", bd=1)
frame2_2_1.pack(side="top", fill="both", expand=True, padx=1, pady=5)

lable_copy = tkinter.Label(frame2_2_1, text="\n[Copyright 2022.singsingCom0Stone]\n[All rights reserved.]\n\n\n문의: cjuacin2022@gmail.com").grid(row=0, column=0, pady=2)

# [[[ 실행, 종료 ]]]
frame2_2_2 = tkinter.Frame(frame2_2, relief="solid", bd=1)
frame2_2_2.pack(side="bottom", fill="both", expand=False, padx=1, pady=5) 

start_btn = tkinter.Button(frame2_2_2, text="실행", width=27, command=threading_start) # 실행 버튼
start_btn.grid(row = 0, column= 0, padx=5, pady=5)

end_btn = tkinter.Button(frame2_2_2, text="종료", width=27, command=exit) # 종료 버튼
end_btn.grid(row = 1, column= 0, padx=5, pady=5)

# GUI작동
window.mainloop()