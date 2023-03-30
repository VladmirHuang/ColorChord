# ColorChord
色彩和声理论计算程序；a python program for color hamony theory.

1. 不再采用枚举类，Chord类使用音符名称初始化，如
~~~javascript
a = Chord(["G","B","E"],name = "Em")
~~~
2. 内部不再使用角度值，只有呈现结果给用户的情况下转为角度。
