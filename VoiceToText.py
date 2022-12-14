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
        if "??????" in GoogleTranslateText or "??????" in GoogleTranslateText:
            TTS("????????????????????????????????????")
            NewRec = sr.Recognizer()
            with sr.AudioFile(record_and_recog(".\\test.wav")) as Newsource:
                NewAudio = NewRec.record(Newsource)
            try:
                Text = Rec.recognize_google(NewAudio, language="zh-CN")
            except speech_recognition.UnknownValueError:
                continue
            print(Text)
            if "????????????" in Text:
                TTS("??????, ??????")
                os.popen("start https://www.baidu.com/")
                TTS("?????????????????????")
            elif "????????????" in Text:
                TTS("??????, ??????")
                os.popen(f"start https://www.baidu.com/s?wd={Text.strip('????????????')}")
                TTS(f"???????????????{Text.strip('????????????')}")
            elif "???????????????" in Text:
                TTS("??????, ??????")
                os.popen(f"start cmd")
                TTS("????????????????????????")
            elif "??????????????????" in Text or "????????????" in Text:
                TTS("??????,?????? ????????????")
                break
            elif "??????" in Text:
                TTS("??????, ??????")
                ISSTART = False
                Text = str(Text).replace("???", "???")
                for _Path in Scanning():
                    if Text.strip("??????") == os.path.split(_Path)[-1].split(".")[0]:
                        os.popen(f'"{_Path}"')
                        print(_Path)
                        TTS(f"??????????????? {Text.strip('??????')}")
                        ISSTART = True
                        break
                if ISSTART:
                    continue
                else:
                    TTS(f"??????????????? {Text.strip('??????')}")
            elif "??????" in Text:
                TTS("?????????????????????????????????")
                shotdownRrc = sr.Recognizer()
                with sr.AudioFile(record_and_recog(".\\out.mp3")) as shotdowndata:
                    shotdownAudio = shotdownRrc.record(shotdowndata)
                try:
                    ISSHOTDOWN = Rec.recognize_google(shotdownAudio, language="zh-CN")
                except speech_recognition.UnknownValueError:
                    continue
                if ISSHOTDOWN in ["???", "??????", "??????", "???"]:
                    TTS("??????, ????????????????????????")
                    os.popen("shutdown -s -t 1")
                elif ISSHOTDOWN in ["???", "???", "??????", "?????????"]:
                    TTS("??????, ???????????????")
                else:
                    TTS("?????????????????????")
            else:
                GET = requests.get(f"http://www.liulongbin.top:3006/api/robot?spoken={Text}")
                if GET.status_code == 200:
                    try:
                        TTS(str(GET.json()['data']['info']['text']).replace("??????", "??????"))
                    except TypeError:
                        continue

def run():
    Start = Thread(target=GoogleTranslate)
    Start.start()
    # Start.join()
