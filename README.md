Folder Scrapy XJP contains several spiders-- details could see READ ME in that folder

munD2LfileDownload is a spider Used to Download files (pdf , video ) from Memorial University online course wesite https://online.mun.ca/d2l/home
Maybe can download ppt files as well (have no chance to test till now)
Files after download then save to C:\downloads folder.

Manual:
Open mun online website, choose 1 course then click the Course Content section once you enter this course.
Copy the URL in Couse Content section, URL should be like https://online.mun.ca/d2l/le/content/473098/Home
Run this spider, paste the URL into the spider, then files could be downloaded automatically to C:\downloads folder.

Notice: for some reason, the spider can only download the files shown in current page. Guess it's caused by the cookie since everytime spider gets the current page cookie to porcess the download function.
In that case, if you want to download all files of this course, you'd better click Table of Contents in left side area under Course Content.
