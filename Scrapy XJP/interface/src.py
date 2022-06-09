# coding=utf-8
'''
user main view
'''

from interface import user_interface
func_dict = {
    '1': user_interface.general_spider,
    '2': user_interface.spider_top_china_XH,
    '3': user_interface.spider_top_china_RM,
    '4': user_interface.spider_XJP_RM,
    '5': user_interface.sendMail,
    '6': user_interface.spider_HousePrice_Canada,
    '7': user_interface.spider_MUNonLine,
    '8': 'Exit'
}

def run():
    while True:
        print(
            '''
            ========= Welcome to Spider field ========
                1. General spider
                2. Spider for Chinese Top leaders in XINHUA net
                3. Spider for Chinese Top leaders in RENMIN net(stay tuned)
                4. Spider for XJP in RINMIN net
                5. -->To Send Chinese Top leaders's news 
                6. Spider for RealEstimate price in Canada
                7. Spider for MUN Online downloading PDFs&Videos
                8. Exit
            =================== END ===================
            '''
        )

        choice = input('Please select the number: ').strip()

        if choice not in func_dict:
            print('Wrong Number! Please select a new one')
            continue
        if choice == '8':
            break
        func_dict.get(choice)()