# encoding=utf-8
import difflib
def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()



from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

bot = ChatBot('test')  # You can rename it whatever you want
trainer = ChatterBotCorpusTrainer(bot)
list_trainer = ListTrainer(bot)
# trainer.train('chatterbot.corpus.chinese') # Load conversations
lines = open('xiaohuangji.txt').readlines()
# print(lines)
list_trainer.train(lines)

while True:
    result = input('You:')
    lines = open('xiaohuangji.txt', 'r', encoding='UTF-8').readlines()
    count = 0
    max = 0.0
    max_biaoji = 0
    for i in lines:
        if string_similar(i, result) > max and count % 3 == 0:
            max = string_similar(i, result)
            max_biaoji = count
        count = count + 1
    # print(max_biaoji)
    # print(max)
    # print(lines[max_biaoji])
    question = lines[max_biaoji]
    print('Bot: %s' % bot.get_response(question))
