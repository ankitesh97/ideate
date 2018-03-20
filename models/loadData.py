# import pickle
# with open('glove.6B/glove.6B.100d.txt') as inp:
#     line = ' '
#     gloveDict={}
#     while line:
#         line = inp.readline()
#         indValues = line.split()
#         try:
#             keyWord = indValues[0]
#             repList = []
#             for x in range(1,len(indValues)):
#                 repList.append(float(indValues[x]))
#             gloveDict[keyWord]=repList
#         except :
#             pass
# with open('gloveDict.pkl',"wb") as outPut:
#     pickle.dump(gloveDict,outPut)
def getSimilarityOfQuestionAndAnswer(question,answer):
    questionWords = question.split()
    ctr = 0
    totalQuestion = np.zeros([1,100])
    for indWord in questionWords:
        try:
            gloveDict[indWord]
            totalQuestion+=np.array(gloveDict[indWord])
            ctr+=1
        except:
            pass
    questionVector = totalQuestion/ctr
    print questionVector
    answerWords = answer.split()
    ctr = 0
    totalAnswer = np.zeros([1,100])
    for indWord in answerWords:
        try:
            gloveDict[indWord]
            totalAnswer+=np.array(gloveDict[indWord])
            ctr+=1
        except:
            pass
    answerVector = totalQuestion/ctr
    print answerVector
    print cosine_similarity(questionVector,answerVector)


getSimilarityOfQuestionAndAnswer('this is a question','this is the answer')
