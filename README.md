---------------------------------------------------------------------------------------------------------------------------------------------
**Folder Scrapy XJP**

It contains several scrapers
  - To collect Chinese Top leaders' latest activities, such as Xi JinPing(习近平)，Li keqiang(李克强)...
  - To collect Canada several main cities' real estate Price, Toronto, Ottawa, Vancouver...
  - To download files from Memorial online course 
  -  More details could be found in READ ME in that folder

---------------------------------------------------------------------------------------------------------------------------------------------

**munD2LfileDownload** 
- It's a scraper Used to Download files (pdf , video, zip ) from Memorial University online course wesite BrightSpace:  https://online.mun.ca/d2l/home
- Maybe can download ppt files as well (have no chance to test till now)
- Files after download then save to _**C:\downloads folder**_.

Manual:
1. Open mun online website, choose one course then click the _**"Course Content"**_ section once you enter this course.
2. Copy the _**URL**_ of that Couse Content section, URL should be like https://online.mun.ca/d2l/le/content/473098/Home
3. Run this spider, paste the URL into the spider, then files could be downloaded automatically to C:\downloads folder.

---> Attached a screenshot below for visual instructions <---

![1656637495(1)](https://user-images.githubusercontent.com/106771290/176802672-3775b7f0-f499-49c7-96d9-363cb7c37ec2.png)



Notice: 
- For some reasons, the scrapper can only download the files shown in current page. Guess it's caused by the cookie since everytime the scrapper needs to get the current page cookie to porcess the download function.
- In that case, if you want to download all files of this course, you'd better click **Table of Contents** in left side area under Course Content.

Update:
- A new function to *download ZIP* files has updated in the scrapper in the Folder **Scrapy XJP**. You are encouraged to try this function in that more versatile spiders. 
- Now the function to download ZIP files has updated to the single scrapper - *munD2LfileDownload.py*
