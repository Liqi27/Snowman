# Snowman
something old

这是两个雪人自动躲避障碍物并且拿旗子得分的python程序，游戏规则:
1.雪人会自动移动, 无需操作
2.撞到树-20分, 拿到旗子+10分
3.游戏时长1分钟

运行AI_snowman.exe演示文件开始游戏
1.打开文件后按任意一键开始游戏，或5秒后自动开始         
2.1分钟后游戏结束时按右上方‘x’退出

源代码在AI-snowman文件夹的AI_snowman.py文件内


程序介绍:

import的module:
1.pygame - 制作动画
2.random - 随机刷新障碍物的位置
4.time - 调试程序

Class：
1.SnowmanClass - 雪人class
  定义雪人的图片，尺寸...以及躲避障碍物的Function

  相关Function/method：
    1.calculate() - 计算怎样避开障碍物
    2.hit_move_stop() - 碰到障碍物后刷新图片并停顿 
    3.do_method() - 执行Class内method

2.ObstacleClass - 障碍物class
  定义树和旗子的图片，尺寸和移动速度

  相关Function/method：
    1.check_tree() - 检测有无障碍物会被雪人撞到

主要Function：
1.beginning()和ending() - 游戏开始和结束的界面
2.create map() - 刷新障碍物/制造背景
3.animate() - 显示/更新具体动画

Main Program - 主程序：
读取配置文件, 得到/修改 图片,字体... 等信息
用while loop持续运行，更新画面，调用function，直到按‘x’进行退出。

这个程序可以在配置文件里修改窗口大小，障碍物图片，雪人图片等。也可以改成AI雪人和玩家手动操作的滑雪人（SkierClass）比赛。


HAVE FUN!
