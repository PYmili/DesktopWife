# DesktopWife

使用Python和PyQt5制作的桌面老婆程序，可以进行语音聊天
---

![icon](.\image\bs.png "icon")

___

# <font color="red">特别提醒</font>

程序使用 [百度云](https://cloud.baidu.com/?from=console) 的语音技术接口，并且接口中有普通话的短音频识别

![短语言识别-中文普通话](./image/wave-chinese.png)

创建好api后在项目当前目录下的 [config.json](./config.json) 文件配置

```json
{
    "APIKey": "Your Api Key",
    "SecretKey": "Your Secret Key"
}
```

## [DesktopWife.py](./DesktopWife.py)

程序主界面

## [VoiceToText](./VoiceToText.py)

程序的 tts/stt 以及 对话功能等。