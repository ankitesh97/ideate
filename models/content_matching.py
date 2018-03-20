import numpy as np
from seq2seq.models import SimpleSeq2Seq,Seq2Seq
import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.optimizers import RMSprop
from sklearn.metrics.pairwise import cosine_similarity
import dill as pickle
from keras import losses
import math
from flask_cors import CORS
from flask import Flask,request
from googlesearch.googlesearch import GoogleSearch

def getOnlineContentVector(search_string):
    response=GoogleSearch().search("anki")
    return_words=[]
    for resp in response:
        text=resp.getText()
        text.replace('\n'," ")
        words=text.split(" ")
        return_words.append(' '.join(words[:20]))
    return return_words
    # return ["ankitesh is a good boy","ankitesh is a bad boy","ankitesh is a funny boy","ankitesh is a boy","ankitesh is not a good boy",
    # "ankitesh is not a boy","ankitesh is a good boy"]

app=Flask(__name__)
CORS(app)

def loadGloveModel(gloveFile):
    print "Loading Glove Model"
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print "Done.",len(model)," words loaded!"
    return model

np.random.seed(1)
DEFAULT=np.random.rand(100)

def getGloveEmbedding(model,word):
    if word in model:
        return model[word]
    else:
        return DEFAULT

def getContextVector(model,glove_dict,sentences):
    get_context_vector=K.function([model.layers[0].input, K.learning_phase()],[model.layers[3].output])
    inputs=np.zeros((len(sentences),20,100))
    for sentenceIndex in range(len(sentences)):
        splitSent=sentences[sentenceIndex].lower().split(" ")
        for wordIndex in range(min(len(splitSent),20)):
            inputs[sentenceIndex,wordIndex]=getGloveEmbedding(glove_dict,splitSent[wordIndex])
    print model.test_on_batch(inputs,inputs)
    context_vector_output = get_context_vector([inputs, 0])[0]
    return context_vector_output

def load_seq2seq():
    word_emb_dim=100
    hidden_dimension=256
    output_len=20
    output_dimen=word_emb_dim
    from seq2seq.models import SimpleSeq2Seq
    model = SimpleSeq2Seq(input_dim=word_emb_dim, hidden_dim=hidden_dimension, output_length=output_len, output_dim=output_dimen)
    model.compile(loss='mse',optimizer=RMSprop(lr=0.0000000000001, rho=0.9))
    model.load_weights('model-7-epochs-63.h5')
    return model

def contentMatching(model,glove_dict,useranswer,answers,threshold):
    THRESHOLD=threshold
    count=0
    answers.append(useranswer)
    context_vectors=getContextVector(model,glove_dict,answers)
    user_answer_context=context_vectors[-1]
    other_answer_contexts=context_vectors[:-1]
    cosine_similarities=[]
    for other_answer_context in other_answer_contexts:
        value=cosine_similarity([user_answer_context],[other_answer_context])
        print "Similarity: "+str(value)
        cosine_similarities.append(value)
        if value>=THRESHOLD:
            count=count+1
    cosine_similarities.sort()
    percent=70
    cosine_similarities=cosine_similarities[max(0,int(math.floor(percent*1.0/100*len(other_answer_contexts)))-1):]
    if len(other_answer_contexts)==0:
        return str(0)
    similar_answer=len(cosine_similarities)*1.0/len(other_answer_contexts)
    return str(similar_answer)


model=None
glove_dict=loadGloveModel("glove.6B.100d.txt")
@app.route('/contentMatching',methods=["POST"])
def content():
    global model
    if model==None:
        model=load_seq2seq()
    print request.json
    answers=request.json["answers"]
    abstract=request.json["abstract"]
    print answers
    print abstract
    return contentMatching(model,glove_dict,abstract,answers,0)

@app.route('/checkPlagiarism',methods=["POST"])
def plagiarism():
    print "plagiarism"
    global model
    if model==None:
        model=load_seq2seq()
    my_abstract="indian premier league"
    my_abstract=request.json["abstract"]
    others=getOnlineContentVector(my_abstract)
    ret= contentMatching(model,glove_dict,my_abstract,others,0)
    return str(ret)

def getSimilarityOfQuestionAndAnswer(question,answer):
    questionWords = question.split()
    ctr = 0
    totalQuestion = np.zeros([1,100])
    for indWord in questionWords:
        try:
            glove_dict[indWord]
            totalQuestion+=np.array(glove_dict[indWord])
            ctr+=1
        except:
            pass
    questionVector = totalQuestion*1.0/ctr
    print questionVector
    answerWords = answer.split()
    ctr = 0
    totalAnswer = np.zeros([1,100])
    for indWord in answerWords:
        try:
            glove_dict[indWord]
            totalAnswer+=np.array(glove_dict[indWord])
            ctr+=1
        except:
            pass
    answerVector = totalAnswer*1.0/ctr
    #print answerVector
    #print np.multiply(questionVector,answerVector)
    #print np.linalg.norm(questionVector)*np.linalg.norm(answerVector)
    if np.sum(np.multiply(questionVector,answerVector))/(np.linalg.norm(questionVector)*np.linalg.norm(answerVector))>0.6:
        return '1'
    return '0'
    #return cosine_similarity(questionVector,answerVector)

#getSimilarityOfQuestionAndAnswer('this is a question','this is the answer')

@app.route('/checkRelevance',methods=["POST"])
def relevance():
    question=request.json["question"]
    answer=request.json["answer"]
    return str(getSimilarityOfQuestionAndAnswer(question,answer))

app.run(host="192.168.43.23", port=8000, debug=True)

# if __name__=="__main__":
    # word_emb_dim=100
    # hidden_dimension=100
    # output_len=20
    # output_dimen=word_emb_dim
    # #glove_dict=loadGloveModel("glove.6B.100d.txt")
    #model=load_seq2seq()
    #print contentMatching(model,glove_dict,"the deer was killed by the tiger",["cricket is a great sport","cricket is a great sport","technology has advantages as well as disadvantages","cricket is a great sport","technology has advantages as well as disadvantages"],0.95)
    # print getSimilarityOfQuestionAndAnswer('ok','give me my water bottle')
    #print getOnlineContentVector('ankitesh')
