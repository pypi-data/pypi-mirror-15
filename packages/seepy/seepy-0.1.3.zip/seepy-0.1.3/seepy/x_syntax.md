![Alt text](x_monty.png)

|Use Reload option to back to your script|

####*Here is extra syntax you can use in your python script to get SeePy report*

###*One line comment*
```
#! Your Markdown comment
```


###*Multi line comment*
```
#!
'''
Your miltiline Markdown comment

you can write long text
'''
```


###*Variable with line comment*
```
a = 30 #! Comment
```
or if `a` value defined use
```
a #! Comment
```


###*Calling variable value in SeePy comment*
You can call variable value in comments using `%(name)s` as it show below
```
a = 1
b = 2 
#! Values are %(a)s and %(b)s
```

###*Showing python code used in your script*
You can show python code from your *.py script as it show below
```
#%code
text = 'Python is cool'
for i in text:
    print i
#%
```

###*Showing image in report*
You can show any image file from directory where your *.py script is stored

```
#%img image.jpg
```