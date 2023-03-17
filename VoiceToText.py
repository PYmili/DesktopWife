import os
import subprocess
import json
import wave
from threading import Thread
import base64

import ProgramLog

import pyaudio
import requests

LOG = ProgramLog.ProgramLog()

_RETURNTEXT = ""

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

STTFORMAT = 'wav'
STTRATE = '16000'
STTCHANNEL = 1
STTCUID = '*******'

def GetBaseUrl() -> str:
    __url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="
    if os.path.isfile(".\\config.json"):
        with open(".\\config.json", "r") as rfp:
            __JSON = json.loads(rfp.read())
        __BasUrl = __url + f"{__JSON['APIKey']}&client_secret={__JSON['SecretKey']}"
        return __BasUrl
    else:
        return False


def record_and_recog(wave_out_path: str = ".\\audio\\test.wav", TIME: int =3) -> bytes:
    LOG.output(
        "正常运行",
        "录音 VoiceToText --> def record_and_recog start ..."
        )
    __audioP = pyaudio.PyAudio()
    __stream = __audioP.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
        )

    with wave.open(wave_out_path, 'wb') as wa_wfp:
        wa_wfp.setnchannels(CHANNELS)
        wa_wfp.setsampwidth(__audioP.get_sample_size(FORMAT))
        wa_wfp.setframerate(RATE)
        for _ in range(0, int(RATE / CHUNK * TIME)):
            wa_wfp.writeframes(__stream.read(CHUNK))

    __stream.stop_stream()
    __stream.close()
    __audioP.terminate()

    with open(wave_out_path, "rb") as rfp:
        __audioData = rfp.read()
    LOG.output(
        "正常运行",
        "录音结束 VoiceToText --> def record_and_recog end ..."
        )
    return __audioData


def getToken(host: str) -> str:
    __resPost = requests.post(host)
    try:
        __access_token = __resPost.json()['access_token']
        __resPost.close()
        return __access_token
    except KeyError:
        TTS("未识别到配置数据，请选择配置。否则无法正常使用哦!")
    return "..."

def Speech_To_Text(speech_data, token, dev_pid=1537):
    SPEECH = base64.b64encode(speech_data).decode('utf-8')

    __data = {
        'format': STTFORMAT,
        'rate': STTRATE,
        'channel': STTCHANNEL,
        'cuid': STTCUID,
        'len': len(speech_data),
        'speech': SPEECH,
        'token': token,
        'dev_pid': dev_pid
    }
    # r=requests.post(url,data=json.dumps(data),headers=headers)
    LOG.output(
        "正常运行",
        "执行STT中..."
        )
    with requests.post(
        'http://vop.baidu.com/server_api',
        json=__data,
        headers={'Content-Type': 'application/json'}
        ) as ReqPost:
        __Result = ReqPost.json()

    if 'result' in __Result:
        return __Result['result'][0]
    else:
        return __Result


# speech = record_and_recog(".\\audio\\test.wav", TIME=3)
# TOKEN = getToken(HOST)
# result = SpeechText(speech, TOKEN, int(1537))
# print(result)
# if type(result) == str:
#     openbrowser(result.strip('，'))


_conent = True
def TTS(Test: str) -> bool:
    global _RETURNTEXT
    _RETURNTEXT = Test
    LOG.output(
        "正常运行",
        f"GET URL:https://tts.youdao.com/fanyivoice?word={Test}&le=zh&keyfrom=speaker"
        )
    __ReqGET = requests.get(
        f"https://tts.youdao.com/fanyivoice?word={Test}&le=zh&keyfrom=speaker"
        )
    if __ReqGET.status_code == 200:
        __ReqGET.close()
        FFplay = subprocess.Popen(f"cd {os.getcwd()} && ffplay -i " \
            f"\"https://tts.youdao.com/fanyivoice?word={Test}&le=zh&keyfrom=speaker\"" \
            " -noborder -nodisp -autoexit",
            shell=True,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.STDOUT,
            # stdin=subprocess.PIPE
            )
        # FFplay.stdin.close()
        FFplay.wait()
        # result = FFplay.stdout.read()
        # FFplay.stdout.close()
        return True
    else:
        return False


def Scanning(Path="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\") -> list:
    LOG.output("正常运行", "扫描快捷方式 VoiceToText --> def Scanning")
    __DIRList = []
    __File = []
    for paths, dirs, files in os.walk(Path):
        if dirs:
            for dir in dirs:
                __DIRList.append(paths+"\\"+dir)
        if files:
            for file in files:
                __File.append(paths+"\\"+file)
    return __File


def GoogleTranslate() -> None:
    global _conent
    while _conent:
        speech = record_and_recog()
        __BaseUrl = GetBaseUrl()
        if __BaseUrl == False:
            LOG.output("错误", "配置文件未找到数据")
            break
        TOKEN = getToken(__BaseUrl)
        result = Speech_To_Text(speech, TOKEN, int(1537))
        if type(result) == dict:
            break
        LOG.output("正常运行", f"{result} VoiceToText --> def GoogleTranslate")
        if "小雨" in result or "小宇" in result:
            LOG.output("正常运行", "语音唤醒成功 VoiceToText --> def GoogleTranslate")
            TTS("主人我在")
            LOG.output("正常运行", "语音回复：主人我在")
            SpeechTWO = Speech_To_Text(record_and_recog(TIME=5), TOKEN, 1537)

            LOG.output("正常运行", f"{SpeechTWO} VoiceToText --> def GooleTranslate")

            if "打开百度" in SpeechTWO:
                TTS("好的, 主人")
                LOG.output("正常运行", "语音回复：好的，主人")
                os.popen("")
                startbaidu = subprocess.Popen(
                     "start https://www.baidu.com/",
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     stdin=subprocess.PIPE
                     )
                # startbaidu.stdin.close()
                # startbaidu.wait()
                # stdout.read()
                # startbaidu.stdout.close()
                TTS("已为您打开百度")
                LOG.output("正常运行", f"语音回复：已为您打开百度")

            elif "百度搜索" in SpeechTWO:
                TTS("好的, 主人")
                LOG.output("正常运行", "语音回复：好的，主人")
                popen = subprocess.Popen(
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
                popen = subprocess.Popen(
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
                ISSTART = False
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
                        ISSTART = True
                        break
                if ISSTART:
                    continue
                else:
                    TTS(f"主人未找到 {Text.strip('打开')}")
                    LOG.output("正常运行", f"语音回复：主人未找到 {Text.strip('打开')}")

            elif "关机" in SpeechTWO:
                TTS("主人是否确定要关机呢？")
                LOG.output("正常运行", f"语音回复：主人是否确定要关机呢？")
                ISSHOTDOWN = Speech_To_Text(record_and_recog(TIME=5), TOKEN, 1537)
                if ISSHOTDOWN in ["是", "是的", "没错", "要"]:
                    TTS("好的, 主人好好休息！")
                    LOG.output("正常运行", f"语音回复：好的, 主人好好休息！")
                    popen = subprocess.Popen(
                        f"shutdown -s -t 1",
                        shell=True,
                        )
                    # popen.stdin.close()
                    # popen.wait()
                    # stdout.read()
                    # popen.stdout.close()
                elif ISSHOTDOWN in ["否", "不", "不要", "不关机"]:
                    TTS("好的, 不进行关机")
                    LOG.output("正常运行", f"语音回复：好的, 不进行关机")
                else:
                    TTS("主人，我没听懂")
                    LOG.output("正常运行", f"语音回复：主人，我没听懂")
            else:
                GET = requests.get(f"http://www.liulongbin.top:3006/api/robot?spoken={SpeechTWO}")
                if GET.status_code == 200:
                    try:
                        TTS(str(GET.json()['data']['info']['text']).replace("小思", "小雨"))
                    except TypeError:
                        continue


def run() -> None:
    Start = Thread(target=GoogleTranslate)
    Start.start()

# GoogleTranslate()