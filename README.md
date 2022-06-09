Purpose: to create a general spider that can scrapy data from interesting websites

Requirement:
1. spider can scrapy data from URL provided by user
1-1. if there's no related module to parser the URL provided then it should feedback the msg (TBD)

2. to create 2 spcific spiders, one is to collecte data from XINHUN & RENMIN about XIjinPing, another one is to collect Realestimate price from Royal 

3. after collecting data, the fisrt sipder can send notification automatically to user if there's update about XIJINGPING latest activities;
3-1. also the data could be saved into SQL (not finish)

4. The second spider can collect the data as well as to store in SQL
4-1. also the data could be analyzed (TBD)

5. ADDED 31/MAY/2022, Multiprocessing to get more cities house price, and optimize the framwork in house price scrapy
6. ADDED 2/JUNE/2022, Image process modules: image binarization, image noise reduction

7. ADDED 7/JUNE/2022, a spider to download pdf or video from MUN Online website (Memorial University online course website)


Spider-Frame design:
3 layers design:
	- Interface layer
		- src.py
		  - show main screen to users and transfer users's selections to user_interface
		- user_interface.py
		  - get users' inputs from src.py and transfer to scrapy.py
		  - one-to-one functions between src.py and user_interface.py

	- Operation layer
		- scrapy.py
		  - create spiders and get data to parser
		  - save data to db folder with preset rules
              - includes 3 particular scarpy functions and 1 sub-scrapy
                - scrapy_XH(): scrapy in XINHUA(any chinese top leader)
                - scrapy_XJP_RMZW(): scrapy in RENMING Xijinping column(only xijinping)
                - scrapy_canada_house(): scrapy Canada main cities' housing price
                    - get_house_price(): sub function
	
	- data handle layer
		- models.py
		  - class spider  and general functions
		  - particular child spider class:
		    - class spiderXJP_XH(spider)
		    - class spiderXJP_RM(spider)
		    - class spider_housePrice(spider)

		- db_handlers.py
		  - includes several data operation functions
		    - save2text(): save data to text;
		    - sendmail(): send mail of scrapy result
		        - checkFile(): used to check if the latest chinese top leader's file exists
		        - sortTextFile(): load text from text files and remove special punctuation before sending mail
		        - sortNewsNyield(): sort text in descending order before sending mail

     - img_handlers.py
       - contains 2 image fuctions:
         - img_binarization(): binarize image to make it clearer
         - img_noise_reduct(): reduce image noise to make it clearer based on binarization
         
      - save2mysql.py
        - contains basic MySQL operations that's encapsulated in python
