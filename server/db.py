import MySQLdb
import time
import md5
import json
import random
import string
import hashlib

class DB :
    def __init__ (self,host,user,password,database):
        self.N = 20
        self.userType = 'b2b57bd11b4438cb060753bd6acd06a5'
        self.adminType = '8f564c11846a64f94a2d4931d372cc8b'
        self.SERVER_IP = 'http://192.168.43.176:8000/'
        self.conn = MySQLdb.connect(host,user,password,database)
        self.curr = self.conn.cursor()

    ##############user table related#######################################
    def userExists(self,user_name):
        query = 'select * from user where user_name = %s'
        try:
            self.curr.execute(query,[user_name])
        except Exception as e:
            print str(e)
        data = self.curr.fetchall()
        if len(data)==0:
            return False
        else:
            return True

    def userRegister(self,user_name,password,user_type,contact,first_name,last_name,first_initial):
        if not self.userExists(user_name):
            query = 'insert into user(user_name,password,user_type,contact,first_name,last_name,user_image) values (%s,%s,%s,%s,%s,%s,%s)'
            try:
                self.curr.execute(query,[user_name,password,user_type,contact,first_name,last_name,self.SERVER_IP+'profile_images/'+first_initial])
                self.conn.commit()
                return 'User Inserted'
            except Exception as e:
                self.conn.rollback()
                print str(e)
                return 'Internal Server Error'
        else:
            return 'User already exists'

    def userLogin(self,user_name,password):
        query = 'select * from user Where user_name=%s and password=%s'
        try:
            self.curr.execute(query,[user_name,password])
        except Exception as e:
            print str(e)
        data = self.curr.fetchall()
        if len(data)==0:
            return 'Username / Password seems to be incorrect'
        else:
            if str(data[0][3])=='0':
                typeToken  = self.userType
            else:
                typeToken = self.adminType
            randomString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(self.N))
            userToken = str(hashlib.md5(randomString).hexdigest())
            query = 'insert into tokens(token,user_name,user_type) values (%s,%s,%s)'
            try:
                self.curr.execute(query,[userToken,user_name,typeToken])
            except Exception as e:
                print str(e)
                return 'Token couldnt be generated'
            self.conn.commit()
            return 'Successfully Logged in '+userToken+" "+typeToken

    def userLogout(self,user_token):
        query = 'delete from tokens where token = %s'
        try:
            self.curr.execute(query,[user_token])
            self.conn.commit()
            return 'Logged Out'
        except Exception as e:
            print str(e)
            return 'Server Error'

    def getUserId(self,user_name):
        if not self.userExists(user_name):
            return 'User doesnt exist'
        query = 'select user_id from user where user_name = %s'
        try:
            self.curr.execute(query,[user_name])
        except Exception as e:
            print str(e)
        data = self.curr.fetchall()
        if len(data)>1:
            return 'Internal Server Error'
        else:
            return data

    def getUserAnsweredQuestions(self,user_name):
        query = 'select questions.title,questions.question_id from user inner join answers on user.user_name = answers.user_name inner join questions on answers.question_id = questions.question_id where user.user_name = %s'
        try:
            self.curr.execute(query,[user_name])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        return data

    def getUserPublicProfile(self,user_name):
        if not self.userExists(user_name):
            return "User doesn't exist"
        query = 'select * from user where user_name = %s'
        try:
            self.curr.execute(query,[user_name])
        except Exception as e:
            print str(e)
        data = self.curr.fetchall()
        if len(data)>1:
            return 'Internal Server Error'
        else:
            return data

    def getUserPrivateProfile(self,user_token):
        user_name = str(self.getNameFromToken(user_token)[0])
        query = 'select answers.question_id,answers.abstract,questions.title from answers inner join questions where answers.question_id = questions.question_id and answers.user_name = %s'
        try:
            self.curr.execute(query,[user_name])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        print data
        return data

    def setUserBankDetails(self,user_name,bank_name,pancard_no,aadhar_no,bank_account_no,bank_ifsc_code):
        query = 'select * from user_transfer_details where user_name = %s'
        try:
            self.curr.execute(query,[user_name])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        if len(data)>0:
            query = 'update user_transfer_details set bank_name = %s,pancard_no = %s,aadhar_no = %s,bank_account_no= %s,bank_ifsc_code=%s where user_name = %s'
            try:
                self.curr.execute(query,[bank_name,pancard_no,aadhar_no,bank_account_no,bank_ifsc_code,user_name])
                self.conn.commit()
                return 'User Details Inserted'
            except Exception as e:
                print str(e)
                return 'Server Error'
        else:
            query = 'insert into user_transfer_details (user_name,bank_name,pancard_no,aadhar_no,bank_account_no,bank_ifsc_code) values(%s,%s,%s,%s,%s,%s)'
            try:
                self.curr.execute(query,[user_name,bank_name,pancard_no,aadhar_no,bank_account_no,bank_ifsc_code])
                self.conn.commit()
                return 'User Details Inserted'
            except Exception as e:
                print str(e)
                return 'Server Error'

    def getUserBankDetails(self,user_name):
        query = 'select bank_name,pancard_no,aadhar_no,bank_account_no,bank_ifsc_code from user_transfer_details where user_name = %s'
        try:
            self.curr.execute(query,[user_name])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchone()
        if data==None:
            return 'Details doesnt exist'
        else:
            return data

    def getTopUser(self):
        query = 'select user_name,earnings,questions_answered,user_image,first_name,last_name from user where user_type = 0 order by earnings desc limit 3'
        try:
            self.curr.execute(query)
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        return data

    def getWinsOfUser(self,user_name):
        query = 'select no_of_times_won from user where user_name = %s'
        try:
            self.curr.execute(query,[user_name])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchone()
        return data

    def getEarningsOfUser(self,user_name):
        query = 'select earnings from user where user_name = %s'
        try:
            self.curr.execute(query,[user_name])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchone()
        return data

    #############################questions table related functions #########################
    def questionPost(self,userId,title,description,category,award):
        query = 'insert into questions(user_id,question_title,question_description,question_category,question_award) values (%s,%s,%s,%s,%s)'
        try:
            self.curr.execute(query,[userId,title,description,category,award])
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print str(e)
            return False

    def getQuestions(self):
        query = 'select question_id,title,total,final_date,question_image,category_name from questions inner join questions_categories on questions.category = questions_categories.category_id order by ts DESC'
        try:
            self.curr.execute(query)
        except Exception as e:
            print str(e)
        data = self.curr.fetchall()
        return data

    def getQuestionDetails(self,question_id):
        query = 'select * from questions where question_id = %s'
        try:
            self.curr.execute(query,[question_id])
        except Exception as e:
            print str(e)
        data = self.curr.fetchone()
        return data

    def getNextQID(self):
        query = 'select question_id from questions order by ts desc limit 1'
        try:
            self.curr.execute(query)
        except Exception as e:
            print str(e)
        data = self.curr.fetchall()
        return data

    def getQuestionsTitles(self):
        query = 'select question_id,title from questions'
        try:
            self.curr.execute(query)
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        return data

    def returnPrizesOfQuestion(self,question_id):
        query = 'select first_prize,second_prize,third_prize from questions where question_id = %s'
        try:
            self.curr.execute(query,[question_id])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchone()
        return data

    def questionPost(self,user_name,title,description,category,deliverables,supp_file_value,first_prize,second_prize,third_prize,total,final_date,image_file_value):
        query = 'insert into questions (user_name,title,description,category,deliverables,file_name,first_prize,second_prize,third_prize,total,final_date,question_image) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            if supp_file_value != 'None':
                final_file_name = self.SERVER_IP+'question_pdf/'+supp_file_value
            else :
                final_file_name = 'None'
            final_question_image = self.SERVER_IP+'question_image/'+image_file_value
            self.curr.execute(query,[user_name,title,description,category,deliverables,final_file_name,first_prize,second_prize,third_prize,total,final_date,final_question_image])
            self.conn.commit()
            return 'Question Inserted'
        except Exception as e:
            print str(e)
            return 'Server Error'

    ###########################token table related############################
    def getNameFromToken(self,token):
        query= 'select user_name from tokens where token = %s'
        try:
            self.curr.execute(query,[token])
        except Exception as e:
            print str(e)
        data = self.curr.fetchone()
        return data

    def getTypeFromToken(self,token):
        query = 'select user_type from tokens where token = %s'
        try:
            self.curr.execute(query,[token])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        user_type = str(data[0][0])
        if user_type == self.adminType:
            return "admin"
        else:
            return "admin"
    ###########################answer table related functions ##############################
    def answerPost(self,question_id,user_name,abstract,solution,supp_file,is_relevant,is_plagiarized):
        query = 'select * from answers where question_id = %s and user_name =%s'
        try:
            self.curr.execute(query,[question_id,user_name])
        except Exception as e:
            print str(e)
        data = self.curr.fetchall()
        if len(data)!=0:
            supp_file_value = self.SERVER_IP+'uploaded_answer_pdf/'+supp_file
            query = 'update answers set abstract = %s, solution = %s ,supp_file = %s,is_relevant = %s,is_plagiarized = %s where question_id = %s and user_name = %s'
            try:
                self.curr.execute(query,[abstract,solution,supp_file_value,is_relevant,is_plagiarized,question_id,user_name])
                self.conn.commit()
                return 'Answer Inserted'
            except Exception as e:
                print str(e)
                return 'Server Error'
        else:
            supp_file_value = self.SERVER_IP+'uploaded_answer_pdf/'+supp_file
            query = 'insert into answers(question_id,user_name,abstract,solution,supp_file,is_relevant,is_plagiarized) values (%s,%s,%s,%s,%s,%s,%s)'
            try:
                self.curr.execute(query,[question_id,user_name,abstract,solution,supp_file_value,is_relevant,is_plagiarized])
                self.conn.commit()
                query = 'select questions_answered from user where user_name = %s'
                try:
                    self.curr.execute(query,[user_name])
                except Exception as e:
                    print str(e)
                    return 'Server Error'
                data = self.curr.fetchall()
                currentValueOfQuestions = int(data[0][0])
                query = 'update user set questions_answered = %s where user_name = %s'
                try:
                    self.curr.execute(query,[currentValueOfQuestions+1,user_name])
                except Exception as e:
                    print str(e)
                    return 'Server Error'
                self.conn.commit()
                return 'Answer Inserted'
            except Exception as e:
                print str(e)
                return 'Couldnt insert answer'

    def getAnswerOfUser(self,user_name,question_id):
            query = 'select * from answers where user_name = %s and question_id = %s'
            try:
                self.curr.execute(query,[user_name,question_id])
            except Exception as e:
                print str(e)
                return 'Server Error'
            data = self.curr.fetchall()
            return data

    def getAnswersOfQuestion(self,question_id):
        query = 'select abstract,solution,supp_file,starred,answer_id from answers where question_id = %s'
        try:
            self.curr.execute(query,[question_id])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        return data

    def getStarredAnswersOfQuestion(self,question_id):
        query = 'select abstract,solution,supp_file,starred,answer_id from answers where question_id = %s and starred = %s'
        try:
            self.curr.execute(query,[question_id,'1'])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        return data

    def starAnswer(self,answer_id):
        query = 'update answers set starred = %s where answer_id = %s'
        try:
            self.curr.execute(query,['1',answer_id])
            self.conn.commit()
            return 'Answer Starred'
        except Exception as e:
            print str(e)
            return 'Server Error'

    def deStarAnswer(self,answer_id):
        query = 'update answers set starred = %s where answer_id = %s'
        try:
            self.curr.execute(query,['0',answer_id])
            self.conn.commit()
            return 'Answer Destarred'
        except Exception as e:
            print str(e)
            return 'Server Error'

    def getUserIdOfAnswerId(self,answer_id):
        query = 'select user_name from answers where answer_id = %s'
        try:
            self.curr.execute(query,[answer_id])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchone()
        return data

    def setAnswerRelevancy(self,answer_id,is_relevant):
        query = 'update answers set is_relevant = %s where answer_id = %s'
        try:
            self.curr.execute(query,[is_relevant,answer_id])
            self.conn.commit()
            return 'Relevancy Updated'
        except Exception as e:
            print str(e)
            return 'Server Error'

    def setAnswerPlagiarism(self,answer_id,is_plagiarized):
        query = 'update answers set is_plagiarized = %s where answer_id = %s'
        try:
            self.curr.execute(query,[is_plagiarized,answer_id])
            self.conn.commit()
            return 'Plagiarism Updated'
        except Exception as e:
            print str(e)
            return 'Server Error'

    ###########################################winner table############################
    def setWinner(self,question_id,first_prize,second_prize,third_prize):
        query = 'update questions set has_winner = %s where question_id = %s'
        try:
            self.curr.execute(query,['1',question_id])
            self.conn.commit()
        except Exception as e:
            print str(e)
            return 'Server Error'
        prizes = self.returnPrizesOfQuestion(question_id)

        first_uname = str(self.getUserIdOfAnswerId(first_prize)[0])
        first_prize_value = int(prizes[0])
        first_uname_noOfWins = int(self.getWinsOfUser(first_uname)[0])
        first_uname_earnings = int(self.getEarningsOfUser(first_uname)[0])
        query = 'update user set earnings = %s , no_of_times_won = %s where user_name = %s'
        try:
            self.curr.execute(query,[first_uname_earnings+first_prize_value,first_uname_noOfWins+1,first_uname])
            self.conn.commit()
        except Exception as e:
            print str(e)
            return 'Server Error'

        second_uname = str(self.getUserIdOfAnswerId(second_prize)[0])
        second_prize_value = int(prizes[1])
        second_uname_noOfWins = int(self.getWinsOfUser(second_uname)[0])
        second_uname_earnings = int(self.getEarningsOfUser(second_uname)[0])
        query = 'update user set earnings = %s , no_of_times_won = %s where user_name = %s'
        try:
            self.curr.execute(query,[second_uname_earnings+second_prize_value,second_uname_noOfWins+1,second_uname])
            self.conn.commit()
        except Exception as e:
            print str(e)
            return 'Server Error'

        third_uname = str(self.getUserIdOfAnswerId(third_prize)[0])
        third_prize_value = int(prizes[2])
        third_uname_noOfWins = int(self.getWinsOfUser(third_uname)[0])
        third_uname_earnings = int(self.getEarningsOfUser(third_uname)[0])
        query = 'update user set earnings = %s , no_of_times_won = %s where user_name = %s'
        try:
            self.curr.execute(query,[third_uname_earnings+third_prize_value,third_uname_noOfWins+1,third_uname])
            self.conn.commit()
        except Exception as e:
            print str(e)
            return 'Server Error'

        query = 'insert into winners(question_id,first_prize,second_prize,third_prize) values (%s,%s,%s,%s)'
        try:
            self.curr.execute(query,[question_id,first_prize,second_prize,third_prize])
            self.conn.commit()
            return 'Winners Inserted'
        except Exception as e:
            print str(e)
            return 'Server Error'

    #######################################departments table##############################################
    def getDepartments(self):
        query = 'select * from government_departments'
        try:
            self.curr.execute(query)
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        return data

    ###################################unique solutions table###########################################
    def addUniqueSolution(self,user_name,solution_abstract,solution_solution,solution_department):
        query = 'insert into unique_solutions (user_name,solution_abstract,solution_solution,solution_department) values (%s,%s,%s,%s)'
        try:
            self.curr.execute(query,[user_name,solution_abstract,solution_solution,solution_department])
            self.conn.commit()
            return 'Solution Inserted'
        except Exception as e:
            print str(e)
            return 'Server Error'

    def getUniqueSolutions(self):
        query = 'select user.user_image,unique_solutions.user_name,unique_solutions.solution_abstract,unique_solutions.solution_solution,unique_solutions.solution_upvotes,unique_solutions.solution_id,user.first_name,user.last_name from unique_solutions inner join user where user.user_name = unique_solutions.user_name'
        try:
            self.curr.execute(query)
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        return data

    def getUpvotesOfSolution(self,solution_id):
        query = 'select solution_upvotes from unique_solutions where solution_id = %s'
        try:
            self.curr.execute(query,[solution_id])
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchone()
        return data

    def upvoteSolution(self,solution_id):
        upvotes = str(int(self.getUpvotesOfSolution(solution_id)[0])+1)
        query = 'update unique_solutions set solution_upvotes = %s where solution_id = %s'
        try:
            self.curr.execute(query,[upvotes,solution_id])
            self.conn.commit()
            return 'Upvoted Successfully'
        except Exception as e:
            print str(e)
            return 'Server Error'

    def getBestUniqueSolutions(self):
        query = 'select user.user_image,unique_solutions.user_name,unique_solutions.solution_abstract,unique_solutions.solution_solution,unique_solutions.solution_upvotes,unique_solutions.solution_id,user.first_name,user.last_name from unique_solutions inner join user where user.user_name = unique_solutions.user_name'
        try:
            self.curr.execute(query)
        except Exception as e:
            print str(e)
            return 'Server Error'
        data = self.curr.fetchall()
        return data

if __name__ == "__main__":
    DATABASE = 'rajasthan_hackathon'
    USER = 'root'
    PASSWORD = 'dharin'
    HOST = '127.0.0.1'
    PORT = '3306'
    dbObj = DB(HOST,USER,PASSWORD,DATABASE)
    # print dbObj.userRegister('sharnam','sharnam',0,'730314007','sharnam','chatpar')
    # print dbObj.userLogin('dharin','dharin')
    # print dbObj.getUserId('sharnam')
    # print dbObj.questionPost('1','hello','description','1','100')
    # print dbObj.answerPost('1','1','Hello this is an answer')
    # print dbObj.getAnswerOfQuestion('1')
    dbObj.getQuestions()
