import os
import wave
import pyaudio
import speech_recognition
import speech_recognition as sr
from threading import Thread
import requests

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

_conent = True

def record_and_recog(wave_out_path, TIME=3):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    wf = wave.open(wave_out_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    for _ in range(0, int(RATE / CHUNK * TIME)):
        data = stream.read(CHUNK)
        wf.writeframes(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    return wave_out_path

def TTS(Test: str):
    GET = requests.get(f"https://tts.youdao.com/fanyivoice?word={Test}&le=zh&keyfrom=speaker-target")
    if GET.status_code == 200:
        with open(".\\out.mp3", "wb") as wfp:
            wfp.write(GET.content)
            wfp.close()
        FFplay = os.popen(f"cd {os.path.split(__file__)[0]} && ffplay out.mp3 -noborder -nodisp -autoexit")
        FFplay.readlines()
        return True
    else:
        return False

def Scanning(Path="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\"):
    _DIRList = []
    _File = []
    for paths, dirs, files in os.walk(Path):
        if dirs:
            for dir in dirs:
                _DIRList.append(paths+"\\"+dir)
        if files:
            for file in files:
                _File.append(paths+"\\"+file)
    return _File

def GoogleTranslate():
    global _conent
    while _conent:
        Rec = sr.Recognizer()
        with sr.AudioFile(record_and_recog(".\\test.wav")) as source:
            audio = Rec.record(source)

        try:
            GoogleTranslateText = Rec.recognize_google(audio, language="zh-CN")
        except speech_recognition.UnknownValueError:
            continue
        print(GoogleTranslateText)
        if "小雨" in GoogleTranslateText or "小宇" in GoogleTranslateText:
            TTS("主人我在听，请您下达命令")
            NewRec = sr.Recognizer()
            with sr.AudioFile(record_and_recog(".\\test.wav")) as Newsource:
                NewAudio = NewRec.record(Newsource)
            try:
                Text = Rec.recognize_google(NewAudio, language="zh-CN")
            except speech_recognition.UnknownValueError:
                continue
            print(Text)
            if "打开百度" in Text:
                TTS("好的, 主人")
                os.popen("start https://www.baidu.com/")
                TTS("已为您打开百度")
            elif "百度搜索" in Text:
                TTS("好的, 主人")
                os.popen(f"start https://www.baidu.com/s?wd={Text.strip('百度搜索')}")
                TTS(f"已为您搜索{Text.strip('百度搜索')}")
            elif "打开命令行" in Text:
                TTS("好的, 主人")
                os.popen(f"start cmd")
                TTS("已为您打开命令行")
            elif "关闭语音功能" in Text or "关闭语音" in Text:
                TTS("好的,主人 下次再见")
                break
            elif "打开" in Text:
                TTS("好的, 主人")
                ISSTART = False
                Text = str(Text).replace("元", "原")
                for _Path in Scanning():
                    if Text.strip("打开") == os.path.split(_Path)[-1].split(".")[0]:
                        os.popen(f'"{_Path}"')
                        print(_Path)
                        TTS(f"已为您打开 {Text.strip('打开')}")
                        ISSTART = True
                        break
                if ISSTART:
                    continue
                else:
                    TTS(f"主人未找到 {Text.strip('打开')}")
            elif "关机" in Text:
                TTS("主人是否确定要关机呢？")
                shotdownRrc = sr.Recognizer()
                with sr.AudioFile(record_and_recog(".\\out.mp3")) as shotdowndata:
                    shotdownAudio = shotdownRrc.record(shotdowndata)
                try:
                    ISSHOTDOWN = Rec.recognize_google(shotdownAudio, language="zh-CN")
                except speech_recognition.UnknownValueError:
                    continue
                if ISSHOTDOWN in ["是", "是的", "没错", "要"]:
                    TTS("好的, 主人好好学习呀！")
                    os.popen("shutdown -s -t 1")
                elif ISSHOTDOWN in ["否", "不", "不要", "不关机"]:
                    TTS("好的, 不进行关机")
                else:
                    TTS("主人，我没听懂")
            else:
                GET = requests.get(f"http://www.liulongbin.top:3006/api/robot?spoken={Text}")
                if GET.status_code == 200:
                    try:
                        TTS(str(GET.json()['data']['info']['text']).replace("小思", "小雨"))
                    except TypeError:
                        continue

def run():
    Start = Thread(target=GoogleTranslate)
    Start.start()
    # Start.join()
