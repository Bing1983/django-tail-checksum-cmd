# How it works?

You have a base.raw.html  

``` html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Base</title>
    <link rel="stylesheet" href="${style.css}"/>
  </head>
  <body>
    <script src="${man.js}"></script>
  </body>
</html>
```

run  `manage.py tail_checksum`  to generate a new file named base.html in the same folder.

``` html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Base</title>
    <link rel="stylesheet" href="style.css?079779d38f7c6b03e02289edc59e5e30"/>
  </head>
  <body>
    <script src="man.js?67d75fe8d3877a5f5a12e0871f535f77"></script>
  </body>
</html>
```



1. Find templates which bear a middle name 'raw',  i.e. [filename].raw.html.
2. Search tokens in these templates, a token should look like ${path/filename} .
3. Find files are referenced by these tokens and calculating their checksums.
4. Replace tokens with their checksum-tailed URLs.
5. For each raw template [file name].raw.html, create a new template named [file name].html to save the changes.



# Installation

Put tail_checksum.py in commands folder of your app,  as  the structure presented below.

``` 
your app/
	__init__.py
	models.py
	management/
    	__init__.py
    	commands/
        	__init__.py
        	tail_checksum.py
	tests.py
	views.py
```



# Usage

 `manage.py tail_checksum`

It will search templates in all installed apps (app name starts with django are excluded.) by default, 

use --app to specify apps in which you want to search raw templates

`manage.py tail_checksum --app cms poll`



# Other things you need to know

## Define your own search path

Before you run the command, make sure it knows where to find static files which are referenced by tokens in templates. Because I'm using webpack and put all compiled static files into a folder named static,  the code below defines the my searching path, you can find it in tail_checksum.py and change it to suit your own project.

``` python
 __STATIC_DIR__ = os.path.join(settings.BASE_DIR,'static')
```

## Do not modify generated files manually

Every time you run the command, it overwrites previously generated files,  so in no case should you modify generated files manually.