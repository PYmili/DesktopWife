# DesktopWife

![ICON](https://github.com/PYmili/DesktopWife/blob/master/image/bg.png)

使用Python和PyQt5制作的桌面老婆程序，可以语音聊天，或许还有女仆管理电脑功能

# 功能介绍
- 语音功能

  ![Button](https://github.com/PYmili/DesktopWife/blob/master/image/Button.png)

  > 程序使用Python和谷歌api实现的语音识别功能，再使用网络API实现的tts功能，当用户说出：“小雨”，这个名字时，程序会触发语音唤醒（音频录取时间为3秒，过三秒后从新录取）

- 天气查询功能

  ![Button](https://github.com/PYmili/DesktopWife/blob/master/image/Button.png)

  > 程序中右键宠物可以看到此功能，查看天气情况
 
- 播放音乐功能

  ![Button](https://github.com/PYmili/DesktopWife/blob/master/image/Button.png)

  > 程序中右键宠物可以看到此功能，播放指定音乐

### B站演示地址：https://www.bilibili.com/video/BV1sV4y1g74K?spm_id_from=333.999.0.0


# 文件介绍
- DesktopWife.py

  > 是主界面文件里面使用PyQt5开发的界面，可掉其他界面，属于主界面范畴，关闭主界面其他界面自动关闭。

- MusicPlayer.py
  
  > 是音乐播放功能的界面。也是用PyQt5开发，属于子窗口，关闭此窗口不影响其他窗口。

- WeatherGui.py
  
  > 是天气查询功能的窗口。用PyQt5开发，属于子窗口，关闭此窗口不影响其他窗口。

- Tray.py
  
  > 是系统托盘功能的实现程序

- VoiceToText.py
  
  > 是程序的后台语音识别，语音转换文字(tts)的实现程序。
