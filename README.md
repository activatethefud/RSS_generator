# Python RSS feed generator 
#### (not aggregator)

This is a simple python script that generates RSS feeds from any site.  It
uses CSS selectors to identify titles, links and article descriptions.  When
called with no argument, it asks for information like: channel title, link and
description, then it goes to ask for the CSS selectors for article title, link
and description. If called with the argument - , it expects the same
information, line by line, from any standard input. Unchanged, it grabs only
the links and titles not previously archived.  This is useful because it can be
automated to make new feed entries for RSS readers.

### Dependencies
You will need the `selenium` module for python, as well as the necessary webdriver binary for your
chosen web browser. For firefox I used [geckodriver](https://github.com/mozilla/geckodriver/releases).

### Usage

Stdin file format: 
* Channel_Name 
* Channel_Link 
* Channel_Description (1 liner)
* Article_Title_CSS_Selector
* Article_Link_CSS_Selector
* Article_Description_CSS_Selector

CSS Selectors can be easily copied using the browser. I've used Firefox and in
it you do: Right click (On the element you need the CSS selector for) ->
Inspect element -> Once you've identified the correct element, by right
clicking on the element, you can find Copy -> CSS Selector.

**WARNING** By default the browser copies the CSS selector for that particular
element, ex.:

`div.listingResult:nth-child(2) > a:nth-child(1) > article:nth-child(1) >
div:nth-child(2) > header:nth-child(1) > h3:nth-child(1)`

This selector will then select this particular element every time. To make it
select all of the elements with the same CSS selector, you must change the
first number to N, ex.:

2 -> n

`div.listingResult:nth-child(n) > a:nth-child(1) > article:nth-child(1) >
div:nth-child(2) > header:nth-child(1) > h3:nth-child(1)`

This is how it should look. When all of the arguments are set, and the program
runs, it will create the .xml feed file, with no whitespaces in the name. 


