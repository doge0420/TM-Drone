import concurrent.futures
import time

numbers = [1, 1, 1, 1]

def do_smth(x):
    for i in range(x):
        time.sleep(2)

def main_sleep():
    print("starting thread")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(do_smth, numbers)

def main_sleep_pas_efficace():
    do_smth(len(numbers))

# def work(number):
#     number = number**2
#     return number

# def main():
#     print("starting thread")
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future = executor.map(work, numbers)
#     for result in future:
#         print(result)

# def main_pas_efficace():
#     square = []
#     for i in numbers:
#         x = i**2
#         square.append(x)
    
#     for i in square:
#         print(i)

if __name__ == '__main__':
    start = time.time()
    
    main_sleep()
    
    # main_sleep_pas_efficace()
    
    end = time.time()
    print(f"temps: {end-start}s")