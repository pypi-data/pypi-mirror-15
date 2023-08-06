![Alt text](x_monty.png)

|Use Reload option to back to your script|

---

#*Comments*

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
---
#*Python code*

###*Showing python code used in your script*
You can show multi-line python code from your *.py script as it show below

```
#%code
text = 'Python is cool'
for i in text:
    print i
#%
```

###*( !!NEW!! )*
or short syntax for one line code  

```
text = 'Python is cool' #%code
```
---
#*Images from file*

###*Showing image in report*
You can show any image file from directory where your *.py script is stored. 
Most image file format allowed (including SVG).

```
#%img image.jpg
```

---
#*Matplotlib*

###*Showing Matplotlib figure ( !!NEW!! )*
You can add to SeePy report Matplotlib figure - matplotlib.pyplot instance is needed

```
import matplotlib.pyplot as plt
import numpy as np
t = np.arange(-1.0, 2.0, 0.01)
s1 = np.cos(9*np.pi*t) + 3 * t ** 2
plt.plot(t, s1)#%plt
```
or you can use:
    
```
plt #%plt
```

---
#*LaTex*

###*Rendering LaTex syntax ( !!NEW!! )*

```
#%tex s(t) = \mathcal{A}\mathrm{sin}(2 \omega t)
```

you can call variables 

```
a = 23
#%tex f(x) = %(a)s * y
```

###*Rendering python code as LaTex syntax ( !!NEW!! )*

```
pi = 3.14 #! - pi value
r = 40 #! - circle radius
# from formula
Area = pi * r ** 2 #%tex

Area #! - what we get
```

---
#*SVG graphic*


###*Rendering SVG syntax from python string ( !!NEW!! )*

```
svgsyntaxstring='''
<svg>
    <circle cx="30" cy="30" r="20" fill="tan" /> 
</svg>
'''
svgsyntaxstring #%svg
```

###*Rendering SVG `svgwrite.drawing` instance from `svgwrite` package ( !!NEW!! )*

```
import svgwrite
svg_document = svgwrite.Drawing()
svg_document.add(svg_document.rect(size = (40, 40), fill = "tan"))
svg_document #%svg
```

---
#*Raport interaction*

###*Interactive python variable changing ( !!NEW!! )*

```
a = 120 #! - this is not interactive variable in your report
b = 30 #<< - this is interactive variable in your report click it to change it
#! the values are %(a)s and %(b)s
```

