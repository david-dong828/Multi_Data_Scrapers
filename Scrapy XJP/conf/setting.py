
import os

BASE_PATH = os.path.dirname(
    os.path.dirname(__file__)
)

DB_PATH = os.path.join(BASE_PATH,'db')
def main():
    print(DB_PATH)

if __name__ == '__main__':
    main()