
import socket
import os
import sys
import struct



def socket_service_image(ui=None):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(('127.0.0.1', 6666))
        s.bind(('10.20.13.130', 9458))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Wait for Connection.....................")

    while True:
        sock, addr = s.accept()
        deal_image(sock, addr, ui)


def deal_image(sock, addr, ui=None):

    print("Accept connection from {0}".format(addr))

    fileinfo_size = struct.calcsize('128sq')
    buf = sock.recv(fileinfo_size)
    if buf:
        filename, filesize = struct.unpack('128sq', buf)
        fn = filename.decode().strip('\x00')
        new_filename = os.path.join('SUST11810417_001.wav')
        recvd_size = 0
        fp = open(new_filename, 'wb')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = sock.recv(1024)
                recvd_size += len(data)
            else:
                data = sock.recv(1024)
                recvd_size = filesize
            fp.write(data)
        print('{} saved.'.format(new_filename))
        fp.close()

        print("abcdefg")
        print('goo')
        print(os.system('sh ~/project/1.sh'))
        f = open('tri5a/decode_test/scoring_kaldi/penalty_1.0/17.txt', 'r', encoding='UTF-8')
        lines = f.readline()
        result = ''
        for i in lines:
            if i >= '\u4e00' and i <= '\u9fa5':
                result = result + i
        # print(result)

        import difflib
        def string_similar(s1, s2):
            return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

        lines = open('xiaohuangji.txt', 'r', encoding='UTF-8').readlines()
        count = 0
        max = 0.0
        max_biaoji = 0
        for i in lines:
            if string_similar(i, result) > max and count % 3 == 0:
                max = string_similar(i, result)
                max_biaoji = count
            count = count + 1
        #print(max_biaoji)
        #print(max)
        #print(lines[max_biaoji])
        question=lines[max_biaoji]
        #print(lines[max_biaoji + 1])
        from chatterbot import ChatBot
        from chatterbot.trainers import ChatterBotCorpusTrainer
        from chatterbot.trainers import ListTrainer
        bot = ChatBot('test',read_only=True)  # You can rename it whatever you want
        list_trainer = ListTrainer(bot)
        #trainer = ChatterBotCorpusTrainer(bot)
        #trainer.train('chatterbot.corpus.chinese')  # Load conversations
        lines = open('xiaohuangji.txt').readlines()
        #print(lines)
        list_trainer.train(lines)

        text=bot.get_response(question)

        print(result)
        print(max)
        print(question)
        print(text)
        am_path = "downloads/tts_train_fastspeech2_raw_phn_pypinyin_g2p_phone"
        vocoder_path = "downloads/csmsc.parallel_wavegan.v1/checkpoint-400000steps.pkl"

        import sys
        sys.path.append("espnet")  # "espnet" is the path of the repository you just pulled


        import time
        import torch
        from espnet2.bin.tts_inference import Text2Speech
        from parallel_wavegan.utils import load_model

        # Load the acoustic model, FastSpeech2
        device = "cpu"
        text2speech = Text2Speech(
            train_config=os.path.join(am_path, "config.yaml"),
            model_file=os.path.join(am_path, "train.loss.ave_5best.pth"),
            device=device,
            speed_control_alpha=1.0,
        )

        text2speech.spc2wav = None

        # Load the vocoder

        fs = 24000
        vocoder = load_model(vocoder_path).to(device).eval()
        vocoder.remove_weight_norm()
        # Decide the input sentence by yourself

        x = str(text)

        # Synthesis
        with torch.no_grad():
            start = time.time()
            wav, c, *_ = text2speech(x)
            wav = vocoder.inference(c)
        rtf = (time.time() - start) / (len(wav) / fs)
        print(f"RTF = {rtf:5f}")

        # Save the synthesized speech
        import numpy as np
        from scipy.io.wavfile import write
        wav = wav.view(-1).cpu().numpy()
        pad_len = int(0.15 * fs)
        wav = np.pad(wav, (pad_len, pad_len), 'constant', constant_values=(0, 0))
        scaled = np.int16(wav / np.max(np.abs(wav)) * 32767)
        write('test.wav', fs, scaled)


        '''result_path = imageprocess(data)'''

        result_path = 'test.wav'
        #
        fhead = struct.pack(b'128sq', bytes(os.path.basename(result_path), encoding='utf-8'),
                            os.stat(result_path).st_size)
        sock.send(fhead)

        fp = open(result_path, 'rb')
        while True:
            result_data = fp.read(1024)
            if not result_data:
                print('{0} send over...'.format(result_path))
                break
            sock.send(result_data)
    sock.close()
    return


if __name__ == '__main__':


    while True:
        socket_service_image()

