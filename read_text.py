f=open('tri5a/decode_test/scoring_kaldi/penalty_1.0/17.txt')
lines=f.readline()
result=''
for i in lines:
    if i>='\u4e00' and i<='\u9fa5':
        result=result+i
print(result)
