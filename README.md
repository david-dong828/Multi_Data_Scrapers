---------------------------------------------------------------------------------------------------------------------------------------------
**Folder Scrapy XJP**

It contains several spiders
  - To collect Chinese Top leaders' latest activities, such as Xi JinPing(习近平)，Li keqiang(李克强)...
  - To collect Canada several main cities' real estate Price, Toronto, Ottawa, Vancouver...
  - To download files from Memorial online course 
  -  More details could be found in READ ME in that folder

---------------------------------------------------------------------------------------------------------------------------------------------

**munD2LfileDownload** 
- It's a spider Used to Download files (pdf , video, zip ) from Memorial University online course wesite https://online.mun.ca/d2l/home
- Maybe can download ppt files as well (have no chance to test till now)
- Files after download then save to C:\downloads folder.

Manual:
1. Open mun online website, choose 1 course then click the Course Content section once you enter this course.
2. Copy the URL in Couse Content section, URL should be like https://online.mun.ca/d2l/le/content/473098/Home
3. Run this spider, paste the URL into the spider, then files could be downloaded automatically to C:\downloads folder.

Notice: 
- For some reason, the spider can only download the files shown in current page. Guess it's caused by the cookie since everytime spider gets the current page cookie to porcess the download function.
- In that case, if you want to download all files of this course, you'd better click Table of Contents in left side area under Course Content.

Update:
- A new function to download ZIP files has updated in the spider in Folder Scrapy XJP. You are encouraged to try this function in that more versatile spiders. 
- Now the function to download ZIP files has updated to the single spider - munD2LfileDownload.py
