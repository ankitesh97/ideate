from flask import Flask , request , send_file , send_from_directory,redirect, session
from flask_cors import CORS
import json
import db
from operator import itemgetter
import pickle
import requests

DATABASE = 'rajasthan_hackathon'
USER = 'root'
PASSWORD = 'dharin'
HOST = '127.0.0.1'
PORT = '3306'
SERVER_IP = 'http://192.168.43.176:8000/'
DB = db.DB(HOST,USER,PASSWORD,DATABASE)

def getTopUser_db():
    data = DB.getTopUser()
    if data == 'Server Error':
        return data
    else:
        print data
        jsonData={}
        jsonData['users']=[]
        for indDat in data:
            jsonData['users'].append({"user_name":indDat[0],"earnings":str(int(indDat[1])),"questions_answered":str(int(indDat[2])),"user_image":indDat[3],"name":indDat[4]+' '+indDat[5]})
        return jsonData

def answerPost_db(question_id,user_token,abstract,solution,supp_file,is_relevant,is_plagiarized):
    user_name = str(DB.getNameFromToken(user_token)[0])
    data = DB.answerPost(question_id,user_name,abstract,solution,supp_file,is_relevant,is_plagiarized)
    return data

def getQuestionDetails_db(question_id):
    data = DB.getQuestionDetails(question_id)
    jsonData = {}
    dateTime = str(data[11].year)+'-'+str(data[11].month)+'-'+str(data[11].day)+' '+str(data[11].hour)+':'+str(data[11].minute)+':'+str(data[11].second)
    jsonData={"title":data[2],"description":data[3],"deliverables":data[5],"file_name":data[6],"first_prize":data[7],"second_prize":data[8],"third_prize":data[9],"total":data[10],"question_image":data[14],"category":data[4],"final_time":dateTime}
    return jsonData

def getQuestions_db():
    jsonData = {}
    jsonData["questions"]=[]
    data = DB.getQuestions()
    for indQue in data:
        dateTime = str(indQue[3].year)+'-'+str(indQue[3].month)+'-'+str(indQue[3].day)+' '+str(indQue[3].hour)+':'+str(indQue[3].minute)+':'+str(indQue[3].second)
        jsonData["questions"].append({"question_id":indQue[0],"title":indQue[1],"award":indQue[2],"image":indQue[4],"time":dateTime,"category":indQue[5]})
    return jsonData

def getUserPublicProfile_db(user_name):
    jsonData={}
    data = DB.getUserPublicProfile(user_name)
    jsonData["user_name"]=user_name
    jsonData["contact"]=data[0][4]
    jsonData["first_name"]=data[0][5]
    jsonData["last_name"]=data[0][6]
    jsonData["earnings"]=data[0][7]
    jsonData["questions_answered"]=data[0][8]
    jsonData["user_image"]=data[0][9]
    data = DB.getUserAnsweredQuestions(user_name)
    jsonData["questions"]=[]
    for indQue in data:
        jsonData["questions"].append({"question_id":indQue[1],"question_title":str(indQue[0])})
    return jsonData

def getUserPrivateProfile_db(user_token):
    jsonData = {}
    user_name = str(DB.getNameFromToken(user_token)[0])
    data = DB.getUserPublicProfile(user_name)
    jsonData["user_name"]=user_name
    jsonData["contact"]=data[0][4]
    jsonData["first_name"]=data[0][5]
    jsonData["last_name"]=data[0][6]
    jsonData["earnings"]=data[0][7]
    jsonData["questions_answered"]=data[0][8]
    jsonData["user_image"]=data[0][9]
    jsonData['questions']=[]
    data = DB.getUserPrivateProfile(user_token)
    for indQue in data:
        jsonData['questions'].append({"question_title":indQue[2],"answer_abstract":indQue[1],"question_id":indQue[0]})
    return jsonData

def getAnswerOfUser_db(user_token,question_id):
    print user_token,question_id
    jsonData = {}
    user_name = str(DB.getNameFromToken(user_token)[0])
    data = DB.getAnswerOfUser(user_name,question_id)
    if len(data)!=0:
        data = data[0]
        jsonData['answer_id'] = str(int(data[0]))
        jsonData['abstract']=data[3]
        jsonData['solution']=data[4]
        jsonData['supp_file']=data[5]
        return jsonData
    else :
        return 'No Answer Exists'


def setUserBankDetails_db(user_token,bank_name,pancard_no,aadhar_no,bank_account_no,bank_ifsc_code):
    user_name = str(DB.getNameFromToken(user_token)[0])
    return DB.setUserBankDetails(user_name,bank_name,pancard_no,aadhar_no,bank_account_no,bank_ifsc_code)

def getUserBankDetails_db(user_token):
    user_name = str(DB.getNameFromToken(user_token)[0])
    jsonData = {}
    data = DB.getUserBankDetails(user_name)
    if data!='Details doesnt exist':
        jsonData['bank_name']= str(data[0])
        jsonData['pancard_no']=str(data[1])
        jsonData['aadhar_no']=str(data[2])
        jsonData['bank_account_no']=str(data[3])
        jsonData['bank_ifsc_code']=str(data[4])
        return jsonData
    else:
        return data

def login_db(username,password):
    return DB.userLogin(username,password)

def logout_db(user_token):
    return DB.userLogout(user_token)

def register_db(username,password,user_type,contact,first_name,last_name,first_initial):
    return DB.userRegister(username,password,user_type,contact,first_name,last_name,first_initial)

def getNextQID_db():
    data = DB.getNextQID()
    if len(data)!=0:
        return int(DB.getNextQID()[0][0])
    else:
        return 0

####################################################################################################


def getQuestionsTitles_db(user_token):
    user_type = str(DB.getTypeFromToken(user_token))
    if user_type == 'admin':
        user_name = str(DB.getNameFromToken(user_token)[0])
        data = DB.getQuestionsTitles()
        jsonData = {}
        jsonData['questions_title']=[]
        for indDat in data:
            jsonData['questions_title'].append({"question_id":indDat[0],"title":indDat[1]})
        return jsonData
    else:
        return 'Are you sure you are the admin?'

def getAnswersOfQuestion_db(user_token,question_id):
    user_type = str(DB.getTypeFromToken(user_token))
    if user_type == 'admin':
        data = DB.getAnswersOfQuestion(question_id)
        jsonData={}
        jsonData['answers']=[]
        for inData in data:
            jsonData['answers'].append({"abstract":inData[0],"solution":inData[1],"supp_file":inData[2],"starred":inData[3],"answer_id":inData[4]})
        return jsonData
    else:
        return 'Are you sure you are the admin?'


def getAbstractOfAnswers_db(question_id):
    data = DB.getAnswersOfQuestion(question_id)
    print data
    jsonData=[]
    for inData in data:
        jsonData.append(inData[0])
    return jsonData


def getStarredAnswersOfQuestion_db(user_token,question_id):
    user_type = str(DB.getTypeFromToken(user_token))
    if user_type == 'admin':
        data = DB.getStarredAnswersOfQuestion(question_id)
        jsonData={}
        jsonData['answers']=[]
        for inData in data:
            jsonData['answers'].append({"abstract":inData[0],"solution":inData[1],"supp_file":inData[2],"starred":inData[3],"answer_id":inData[4]})
        return jsonData
    else:
        return 'Are you sure you are the admin?'

def starAnswer_db(user_token,answer_id):
    user_type = str(DB.getTypeFromToken(user_token))
    if user_type == 'admin':
        return DB.starAnswer(answer_id)
    else:
        return 'Are you sure you are the admin?'

def deStarAnswer_db(user_token,answer_id):
    user_type = str(DB.getTypeFromToken(user_token))
    if user_type == 'admin':
        return DB.deStarAnswer(answer_id)
    else:
        return 'Are you sure you are the admin?'

def setWinner_db(user_token,question_id,first_prize,second_prize,third_prize):
    user_type = str(DB.getTypeFromToken(user_token))
    if user_type == 'admin':
        return DB.setWinner(question_id,first_prize,second_prize,third_prize)
    else:
        return 'Are you sure you are the admin?'

def questionPost_db(user_token,title,description,category,deliverables,supp_file_value,first_prize,second_prize,third_prize,total,final_date,image_file_value):
    user_type = str(DB.getTypeFromToken(user_token))
    if user_type == 'admin':
        return DB.questionPost('admin@admin.com',title,description,category,deliverables,supp_file_value,first_prize,second_prize,third_prize,total,final_date,image_file_value)
    else:
        return 'Are you sure you are the admin?'


def getDepartments_db():
    data = DB.getDepartments()
    jsonData={}
    jsonData["departments"]=[]
    for inData in data:
        jsonData["departments"].append({"department_id":inData[0],"department_name":inData[1]})
    return jsonData

def addUniqueSolution_db(user_token,solution_abstract,solution_solution,solution_department):
    user_name = str(DB.getNameFromToken(user_token)[0])
    return DB.addUniqueSolution(user_name,solution_abstract,solution_solution,solution_department)

def getUniqueSolutions_db():
    data = DB.getUniqueSolutions()
    jsonData={}
    jsonData['solutions']=[]
    for inData in data:
        jsonData['solutions'].append({"user_image":inData[0],"user_name":inData[6]+' '+inData[7],"solution_abstract":inData[2],"solution_solution":inData[3],"solution_upvotes":inData[4],"solution_id":inData[5]})
    return jsonData

def upvoteSolution_db(solution_id):
    return DB.upvoteSolution(solution_id)

def getBestUniqueSolutions_db():
    data = DB.getUniqueSolutions()
    jsonData={}
    jsonData['solutions']=[]
    for inData in data:
        jsonData['solutions'].append({"user_image":inData[0],"user_name":inData[6]+' '+inData[7],"solution_abstract":inData[2],"solution_solution":inData[3],"solution_upvotes":inData[4],"solution_id":inData[5]})
    return jsonData

def setAnswerRelevancy_db(answer_id,is_relevant):
    return DB.setAnswerRelevancy(answer_id,is_relevant)

def setAnswerPlagiarism_db(answer_id,is_plagiarized):
    return DB.setAnswerPlagiarism(answer_id,is_plagiarized)

#at_here


app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/login',methods=['POST'])
def login():
    username=request.form['user_name']
    password=request.form['password']
    ret_val = login_db(username,password)
    if 'Successfully Logged in' in ret_val:
        typeToken = ret_val.split(' ')[-1]
        userToken = ret_val.split(' ')[-2]
        return json.dumps({"message":"Successfully Logged in","token":str(userToken),"type":str(typeToken)})
    else:
        return json.dumps({"message":str(ret_val)})

@app.route('/logout',methods=['POST'])
def logout():
    user_token = request.form['user_token']
    ret_val = logout_db(user_token)
    return json.dumps({"message":ret_val})

@app.route('/register',methods=['POST'])
def register():
    username=request.form['user_name']
    password=request.form['password']
    user_type=0
    contact=request.form['contact']
    first_name=request.form['first_name']
    last_name=request.form['last_name']
    first_initial = first_name[0].upper()+'.png'
    ret_val = register_db(username,password,user_type,contact,first_name,last_name,first_initial)
    return json.dumps({"message":str(ret_val)})

@app.route('/getQuestions',methods=['POST'])
def getQuestions():
    ret_val = getQuestions_db()
    return json.dumps({"message":ret_val})

@app.route('/getQuestionDetails',methods=['POST'])
def getQuestionDetails():
    question_id = request.form['question_id']
    ret_val = getQuestionDetails_db(question_id)
    return json.dumps({"message":ret_val})

@app.route('/getUserPublicProfile',methods=['POST'])
def getUserPublicProfile():
    user_name = request.form['user_name']
    ret_val = getUserPublicProfile_db(user_name)
    return json.dumps({"message":ret_val})

@app.route('/getUserPrivateProfile',methods=['POST'])
def getUserPrivateProfile():
    user_token = request.form['user_token']
    # print user_token
    ret_val = getUserPrivateProfile_db(user_token)
    return json.dumps({"message":ret_val})


@app.route('/answerCheck',methods=['POST'])
def answerCheck():
    print request.form
    form = eval(request.form['data'])
    question_id = form['question_id']
    abstract = form['abstract']
    user_token = form['user_token']
    answers = getAbstractOfAnswers_db(question_id)
    data = {"answers":answers,"abstract":abstract}
    r = requests.post("http://192.168.43.23:8000/contentMatching", json=data)
    percentPopulation = float(r.text)
    # percentPopulation = contentMatching(model_content,glove_dict,abstract,answers,1)
    return json.dumps({"message":"Your answer is somewhat similar to about "+str(int(percentPopulation*100))+" % of the submitted answers."})



@app.route('/answerPost',methods=['POST'])
def answerPost():
    form = eval(request.form['data'])
    question_id = form['question_id']
    user_token = form['user_token']
    abstract = form['abstract']
    solution = form['solution']
    fileObj =  request.files['file']
    supp_file = question_id+'_'+user_token+'_'+fileObj.filename
    fileObj.save('uploaded_answer_pdf/'+supp_file)
    #Plagiarism
    data = {"abstract":abstract}
    r = requests.post("http://192.168.43.23:8000/checkPlagiarism", json=data)
    is_plagiarized = int(r.text)
    #relevant
    print getQuestionDetails_db(question_id)
    data = {"question":"a", "answer":abstract}
    r = requests.post("http://192.168.43.23:8000/checkRelevance", json=data)
    is_relevant = int(r.text)
    ret_val = answerPost_db(question_id,user_token,abstract,solution,supp_file,is_relevant,is_plagiarized)
    return json.dumps({"message":ret_val})

@app.route('/setUserBankDetails',methods=['POST'])
def setUserBankDetails():
    user_token = request.form['user_token']
    print user_token
    bank_name = request.form['bank_name']
    pancard_no = request.form['pancard_no']
    aadhar_no = request.form['aadhar_no']
    bank_account_no = request.form['bank_account_no']
    bank_ifsc_code = request.form['bank_ifsc_code']
    print bank_name,bank_ifsc_code,bank_account_no,aadhar_no,pancard_no
    ret_val = setUserBankDetails_db(user_token,bank_name,pancard_no,aadhar_no,bank_account_no,bank_ifsc_code)
    return json.dumps({"message":str(ret_val)})

@app.route('/getUserBankDetails',methods=['POST'])
def getUserBankDetails():
    user_token = request.form['user_token']
    ret_val = getUserBankDetails_db(user_token)
    return json.dumps({"message":ret_val})

@app.route('/getAnswerOfUser',methods=['POST'])
def getAnswerOfUser():
    user_token = request.form['user_token']
    question_id = request.form['question_id']
    ret_val = getAnswerOfUser_db(user_token,question_id)
    return json.dumps({"message":ret_val})

@app.route('/getTopUser',methods=['POST'])
def getTopUser():
    ret_val = getTopUser_db()
    return json.dumps({"message":ret_val})

@app.route('/uploaded_answer_pdf/<path:filename>')
def download_answer_pdf(filename):
    print filename
    return send_from_directory('uploaded_answer_pdf/',filename,as_attachment=True)

@app.route('/question_image/<path:filename>')
def download_file(filename):
    print filename
    return send_from_directory('question_image/', filename, as_attachment=True)

@app.route('/profile_images/<path:filename>')
def download_profile_file(filename):
    print filename
    return send_from_directory('profile_images/', filename, as_attachment=True)

##################################################################################
@app.route('/getQuestionsTitles',methods=['POST'])
def getQuestionsTitles():
    user_token = request.form['user_token']
    ret_val = getQuestionsTitles_db(user_token)
    return json.dumps({"message":ret_val})

@app.route('/getAnswersOfQuestion',methods=['POST'])
def getAnswersOfQuestion():
    user_token = request.form['user_token']
    question_id = request.form['question_id']
    ret_val = getAnswersOfQuestion_db(user_token,question_id)
    return json.dumps({"message":ret_val})

@app.route('/starAnswer',methods=['POST'])
def starAnswer():
    user_token = request.form['user_token']
    answer_id = request.form['answer_id']
    ret_val = starAnswer_db(user_token,answer_id)
    return json.dumps({"message":str(ret_val)})

@app.route('/deStarAnswer',methods=['POST'])
def deStarAnswer():
    user_token = request.form['user_token']
    answer_id = request.form['answer_id']
    ret_val = deStarAnswer_db(user_token,answer_id)
    return json.dumps({"message":str(ret_val)})

@app.route('/getStarredAnswersOfQuestion',methods=['POST'])
def getStarredAnswersOfQuestion():
    user_token = request.form['user_token']
    question_id = request.form['question_id']
    ret_val = getStarredAnswersOfQuestion_db(user_token,question_id)
    return json.dumps({"message":ret_val})

@app.route('/setWinner',methods=['POST'])
def setWinner():
    user_token = request.form['user_token']
    question_id = request.form['question_id']
    first_prize = request.form['first_prize']
    second_prize = request.form['second_prize']
    third_prize = request.form['third_prize']
    ret_val = setWinner_db(user_token,question_id,first_prize,second_prize,third_prize)
    return json.dumps({"message":str(ret_val)})

@app.route('/questionPost',methods=['POST'])
def questionPost():
    print request.files
    print request.form
    qid = str(int(getNextQID_db())+1)
    image_file = request.files['image_file']
    form = eval(request.form['data'])
    if 'file' not in form:
        supp_file =  request.files['file']
    else:
        supp_file = 'None'
    user_token = form['user_token']
    title = form['title']
    final_date = form['final_date']
    final_date = final_date + ' 00:00:00'
    description = form['description']
    category = form['category']
    deliverables = form['deliverables']
    first_prize = form['first_prize']
    second_prize = form['second_prize']
    third_prize = form['third_prize']
    total = form['total_prize']
    image_file_value = qid+"_"+image_file.filename
    if supp_file!='None':
        supp_file_value = qid+'_'+supp_file.filename
        supp_file.save('question_pdf/'+supp_file_value)
    else:
        supp_file_value = 'None'
    image_file.save('question_image/'+image_file_value)
    ret_val = questionPost_db(user_token,title,description,category,deliverables,supp_file_value,first_prize,second_prize,third_prize,total,final_date,image_file_value)
    return json.dumps({"message":ret_val})

@app.route('/getDepartments',methods=['POST'])
def getDepartments():
    ret_val = getDepartments_db()
    return json.dumps({"message":ret_val})

@app.route('/addUniqueSolution',methods=['POST'])
def addUniqueSolution():
    user_token = request.form["user_token"]
    solution_abstract = request.form["solution_abstract"]
    solution_solution = request.form["solution_solution"]
    solution_department = request.form["solution_department"]
    ret_val = addUniqueSolution_db(user_token,solution_abstract,solution_solution,solution_department)
    return json.dumps({"message":str(ret_val)})

@app.route('/getUniqueSolutions',methods=['POST'])
def getUniqueSolutions():
    ret_val = getUniqueSolutions_db()
    return json.dumps({"message":ret_val})

@app.route('/upvoteSolution',methods=['POST'])
def upvoteSolution():
    solution_id = request.form['solution_id']
    ret_val = upvoteSolution_db(solution_id)
    return json.dumps({"message":ret_val})

@app.route('/getBestUniqueSolutions',methods=['POST'])
def getBestUniqueSolutions():
    ret_val = getBestUniqueSolutions_db()
    return json.dumps({"message":ret_val})

app.run(host='192.168.43.176',port=8000,debug=True)
