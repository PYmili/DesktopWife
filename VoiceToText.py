import os
import subprocess
import json
import wave
from threading import Thread
import base64

import ProgramLog

import pyaudio
import requests
import pyttsx3

LOG = ProgramLog.ProgramLog()
CONTROLLER = True
RETURNTEXT = ""

TTS_ENGINE = pyttsx3.init()     # 初始化pyttsx3模块，为后面调用做准备
TTS_RATE: int = 150     # 语速
TTS_VOLUME: float = 1.0     # 音量:0-1


def GenerateRequestLink() -> str:
    """
    生成向百度云发送请求链接
    写入 APIKey SecretKey 两个参数值
    可更改当前目录下config.json文件中的值
    :return: str or False
    """
    __url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="
    if os.path.isfile(".\\config.json"):
        with open(".\\config.json", "r") as rfp:
            __JSON = json.loads(rfp.read())
        __BaseUrl = __url + f"{__JSON['APIKey']}&client_secret={__JSON['SecretKey']}"
        return __BaseUrl
    else:
        return False


def SoundRecording(
        _format: object = pyaudio.paInt16,
        _WaveOutPath: str = ".\\audio\\test.wav",
        _time: int = 3,
        _rate: int = 16000,
        _channels: int = 1,
        _chunk: int = 1024
) -> bytes:
    """
    使用pyaudio模块调用系统麦克风进行录音操作
    :param _format: pyaudio.paInt16
    :param _WaveOutPath: str
    :param _time: int = 3
    :param _rate: inr = 16000
    :param _channels: int = 1
    :param _chunk: int = 1024
    :return: bytes
    """
    LOG.output(
        "正常运行",
        "录音 VoiceToText --> def SoundRecording start ..."
        )
    __audioP = pyaudio.PyAudio()
    __stream = __audioP.open(
        format=_format,
        channels=_channels,
        rate=_rate,
        input=True,
        frames_per_buffer=_chunk
        )

    with wave.open(_WaveOutPath, 'wb') as wa_wfp:
        wa_wfp.setnchannels(_channels)
        wa_wfp.setsampwidth(__audioP.get_sample_size(_format))
        wa_wfp.setframerate(_rate)
        RangeEnd: int = int(_rate / _chunk * _time)
        for _ in range(RangeEnd):
            wa_wfp.writeframes(__stream.read(_chunk))

    __stream.stop_stream()
    __stream.close()
    __audioP.terminate()

    with open(_WaveOutPath, "rb") as rfp:
        __AudioData = rfp.read()
    LOG.output(
        "正常运行",
        "录音结束 VoiceToText --> def SoundRecording end ..."
        )
    return __AudioData


def getToken(host: str) -> str:
    """
    获取百度云API的Token值
    :param host: str
    :return: str or False
    """
    with requests.post(host) as post:
        try:
            __access_token = post.json()['access_token']
            post.close()
            return __access_token
        except KeyError:
            TTS("未识别到配置数据，请选择配置。否则无法正常使用哦!")

    return False


def SpeechToText(
        _SpeechData: bytes,
        _token: str,
        _dev_pid: int = 1537,
        _format: str = 'wav',
        _rate: str = '16000',
        _channel: int = 1,
        _cuid: str = '*******'
) -> str:
    """
    将音频数据传输到百度云API接口，再获取到API识别到的文本信息。
    :param _SpeechData: bytes
    :param _token: str
    :param _dev_pid: int = 1537
    :param _format: str = 'wav'
    :param _rate: str = '16000'
    :param _channel: int = 1
    :param _cuid: str = '*******'
    :return: str
    """

    __data = {
        'format': _format,
        'rate': _rate,
        'channel': _channel,
        'cuid': _cuid,
        'len': len(_SpeechData),
        'speech': base64.b64encode(
            _SpeechData
        ).decode('utf-8'),
        'token': _token,
        'dev_pid': _dev_pid
    }
    LOG.output(
        "正常运行",
        "执行STT中..."
        )
    with requests.post(
        'http://vop.baidu.com/server_api',
        json=__data,
        headers={'Content-Type': 'application/json'}
    ) as post:
        if 'result' in post.json():
            post.close()
            return post.json()['result'][0]
        else:
            post.close()
            return post.json()


def TTS(
        Test: str,
        rate: int = TTS_RATE,
        volume: float = TTS_VOLUME
) -> bool:
    """
    使用pyttsx3库，将Test的字符串内容转换为音频并播放
    :param Test: str
    :param rate: int = TTS_RATE
    :param volume: float = TTS_VOLUME
    :return: bool
    """
    global RETURNTEXT
    RETURNTEXT = Test
    LOG.output(
        "正常运行",
        f"TTS {Test}"
        )
    TTS_ENGINE.setProperty("rate", rate)
    TTS_ENGINE.setProperty("volume", volume)

    TTS_ENGINE.say(Test)
    TTS_ENGINE.runAndWait()
    TTS_ENGINE.stop()

    return True


def Scanning(
        Path: str = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\"
) -> list:
    """
    Windows系统下扫描桌面快捷方式
    :param Path:  str
    :return: list
    """
    LOG.output("正常运行", "扫描快捷方式 VoiceToText --> def Scanning")
    __DIRList = []
    __Files = []
    for paths, dirs, files in os.walk(Path):
        if dirs:
            for i in dirs:
                __DIRList.append(paths+"\\" + i)
        if files:
            for j in files:
                __Files.append(paths+"\\" + j)
    return __Files


def main() -> None:
    """
    主函数
    :return: None
    """
    global CONTROLLER
    while CONTROLLER:
        speech = SoundRecording()
        __Link = GenerateRequestLink()
        if not __Link:
            LOG.output("错误", "配置文件未找到数据")
            break
        TOKEN = getToken(__Link)
        result = SpeechToText(speech, TOKEN, int(1537))
        if type(result) == dict:
            break
        LOG.output("正常运行", f"{result} VoiceToText --> def GoogleTranslate")
        if "小雨" in result or "小宇" in result:
            LOG.output("正常运行", "语音唤醒成功 VoiceToText --> def GoogleTranslate")
            TTS("主人我在")
            LOG.output("正常运行", "语音回复：主人我在")
            SpeechTWO = SpeechToText(SoundRecording(_time=5), TOKEN, 1537)

            LOG.output("正常运行", f"{SpeechTWO} VoiceToText --> def main")

            if "打开百度" in SpeechTWO:
                TTS("好的, 主人")
                LOG.output("正常运行", "语音回复：好的，主人")
                os.popen("")
                subprocess.Popen(
                     "start https://www.baidu.com/",
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     stdin=subprocess.PIPE
                     )
                # .stdin.close()
                # .wait()
                # stdout.read()
                # .stdout.close()
                TTS("已为您打开百度")
                LOG.output("正常运行", f"语音回复：已为您打开百度")

            elif "百度搜索" in SpeechTWO:
                TTS("好的, 主人")
                LOG.output("正常运行", "语音回复：好的，主人")
                subprocess.Popen(
                     f"start https://www.baidu.com/s?wd={SpeechTWO.strip('百度搜索')}",
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     stdin=subprocess.PIPE
                     )
                # popen.stdin.close()
                # popen.wait()
                # stdout.read()
                # popen.stdout.close()
                TTS(f"已为您搜索{SpeechTWO.strip('百度搜索')}")
                LOG.output("正常运行", f"语音回复：已为您搜索{SpeechTWO.strip('百度搜索')}")

            elif "打开命令行" in SpeechTWO:
                TTS("好的, 主人")
                LOG.output("正常运行", "语音回复：好的，主人")
                subprocess.Popen(
                     f"start cmd",
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     stdin=subprocess.PIPE
                     )
                # popen.stdin.close()
                # popen.wait()
                # stdout.read()
                # popen.stdout.close()
                TTS("已为您打开命令行")
                LOG.output("正常运行", "语音回复：已为您打开命令行")

            elif "关闭语音功能" in SpeechTWO or "关闭语音" in SpeechTWO:
                TTS("好的,主人 下次再见")
                LOG.output("正常运行", "语音回复：好的，主人 下次再见")
                break

            elif "打开" in SpeechTWO:
                TTS("好的, 主人")
                LOG.output("正常运行", "语音回复：好的，主人")
                IsStart = False
                Text = str(SpeechTWO).strip("。").replace("元", "原")
                for _Path in Scanning():
                    if Text.strip("打开") == os.path.split(_Path)[-1].split(".")[0]:
                        popen = subprocess.Popen(
                            f"{_Path}",
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            stdin=subprocess.PIPE
                        )
                        popen.stdin.close()
                        # popen.wait()
                        # stdout.read()
                        # popen.stdout.close()
                        print(_Path)
                        TTS(f"已为您打开 {Text.strip('打开')}")
                        LOG.output("正常运行", f"语音回复：已为您打开 {Text.strip('打开')}")
                        IsStart = True
                        break
                if IsStart:
                    continue
                else:
                    TTS(f"主人未找到 {Text.strip('打开')}")
                    LOG.output("正常运行", f"语音回复：主人未找到 {Text.strip('打开')}")

            elif "关机" in SpeechTWO:
                TTS("主人是否确定要关机呢？")
                LOG.output("正常运行", f"语音回复：主人是否确定要关机呢？")
                IsShotDown = SpeechToText(SoundRecording(_time=5), TOKEN, 1537)
                if IsShotDown in ["是", "是的", "没错", "要"]:
                    TTS("好的, 主人好好休息！")
                    LOG.output("正常运行", f"语音回复：好的, 主人好好休息！")
                    subprocess.Popen(
                        f"shutdown -s -t 1",
                        shell=True,
                        )
                    # popen.stdin.close()
                    # popen.wait()
                    # stdout.read()
                    # popen.stdout.close()
                elif IsShotDown in ["否", "不", "不要", "不关机"]:
                    TTS("好的, 不进行关机")
                    LOG.output("正常运行", f"语音回复：好的, 不进行关机")
                else:
                    TTS("主人，我没听懂")
                    LOG.output("正常运行", f"语音回复：主人，我没听懂")
            else:
                with requests.get(f"http://www.liulongbin.top:3006/api/robot?spoken={SpeechTWO}") as get:
                    if get.status_code == 200:
                        try:
                            TTS(str(get.json()['data']['info']['text']).replace("小思", "小雨"))
                        except TypeError:
                            continue


def run() -> None:
    Start = Thread(target=main)
    Start.start()
