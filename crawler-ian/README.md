Web Crawler

TODO: UPDATE ME!

This crawler needs a subdirectory "files". If it dose not exist it will attempt
to create one. If it exists it will run normally. Page limit and seed can be specified
via prompt. If prompt is left empty of is < 1 the crawler will run for a default of 5000 
pages. If the default seed prompt is not 'n' the crawler will use the default seed. If 
a new seed is provided the program will not test it before hand. If it isn't the main page
the robots.txt file may be missed. The program will record pages it visits in a file:
visited-domains.json, delete this file if you want the crawler to start from scratch. 
Visited pages will be recorded even if the program ends early via ^c or for some
other reason. Raw page data will be recorded in the files directory under the name:
<pageName>.txt where pageName is the page's URL with all / and : removed. 

