# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 15:21:50 2018

@author: siddhanta.bhatta92@gmail.com
"""
""" Using VoiceIt API we will register an users voice and then authenticate it"""

"""
    steps to use :
        1 - create folder with %person and create folders train and test inside it
        2 - add >=3 utterances of same sentence from below list of sentences into a wav
        file with 44100 sampling rate and length between 1.3s - 5s,
        
            1 - Hello I am very happy today
            2 - Never forget tomorrow is a new day	
            3 - Eventually winter will turn into spring	
            4 - Remember to wash your hands before eating	
            
        a trained sentence is one where 3 utterences are successfully registered
            
        3 - add >=1 utterences for testing in test folder(with same config as train wav)
        note - test must be from the trained sentences only.
        4 - change the %workdir to where you store the folder
        5 - give user information in %user information section accordingly
"""
workdir = 'C:\\Users\\tYson\\Desktop\\voiceit-python'
#API credential
developerId = "270130c4020a4860bc31a7d2debb0011"
# importing helper class VoiceIt and json
from VoiceIt import VoiceIt
import json
from os import listdir
from os.path import isfile, join
import os
# creating an instance of VoiceIt passing the developer credentials
myVoiceIt = VoiceIt(developerId)

# user information
userid = "TheMeanSquares"
password = "d0CHipUXOk"
person = "sid"

# creating an user for VoiceIt
def creating_user(userid, password):
    response = json.loads(myVoiceIt.createUser(userid, password))
    if response["Result"] == "Success":
        return "created successfully"
    else:
        print(response)
        return "not created successfully"
# delete user
def delete_user(userid, password):
    response = json.loads(myVoiceIt.deleteUser(userid, password))
    if response["Result"] == "Success":
        return "deleted successfully"
    else:
        print(response)
        return "not deleted successfully"

# getting user
def check_user_exists(userid, password):
    response = json.loads(myVoiceIt.getUser("TheMeanSquares", "d0CHipUXOk"))
    if response["Responsecode"] == "SUC" and response["Exists"] == True:
        return "user exists"
    else:
        print(response)
        return "user doesnot exist"

# registering voice for the user
def enroll_voice(userid, password, wavfile):
    ''' creating an enrollment '''
    response = json.loads(myVoiceIt.createEnrollment(userid, password, wavfile, "en-IN"))
    if response["Result"] == "Success" :
        enrollmentid = response["EnrollmentID"]
        detected_text = response["DetectedVoiceprintText"]
        return (enrollmentid, detected_text)
    else:
        print(response)
        return ("not enrolled","not successful")

        
 # delete enrollment      
def delete_enrollment(userid, password, enrollmentid):
    response = json.loads(myVoiceIt.deleteEnrollment(userid, password, enrollmentid))
    if response["Result"] == "Success" :
        return str(enrollmentid) + " deleted successfully"
    else:
        print(response)
        return "deletion of enrollment unsuccessful"+str(enrollmentid)
    
# get all enrollments for a user
def get_all_enrollments(userid, password):
    response = json.loads(myVoiceIt.getEnrollments(userid, password))
    if response["ResponseCode"] == "SUC":
        return response["Result"]
    else:
        print(response)

#authenticate the voice of the user TheMeanSquares
def user_authentication(userid, password, wavfile):
    response = json.loads(myVoiceIt.authentication(userid, password, wavfile, "en-IN"))
    if response["ResponseCode"] == "SUC":
        return response["ResponseCode"], response["Result"]
    else: 
        return response["ResponseCode"], response["Result"]
    
# driver function
def main():
    # deleting the userid first(not necessary)
    delete_user(userid, password)
    # changing working directory
    os.chdir(workdir)
    # training data    
    train_path = "input_data"+ "/" + person + "/train"
    train_files = [f for f in listdir(train_path) if isfile(join(train_path, f))]
    test_path = "input_data" + "/" + person + "/test"
    test_files =  [f for f in listdir(test_path) if isfile(join(test_path, f))]
    # creating user
    print("User "+ userid+ " is " + creating_user(userid, password))
    # creating enrollments for voice
    enrollment_ids = []
    detected_text = ""
    for file in train_files:
        wavfile = train_path + '/' + file
        print(wavfile)
        enrollment_id, detected_text = enroll_voice(userid, password, wavfile)
        if enrollment_id != 'not enrolled':
            enrollment_ids.append(enrollment_id)        
    print("for user : ", userid, " enrollment ids are ", ','.join(enrollment_ids), " for text: ", detected_text)
    # authentication
    for file in test_files:
        wavfile = test_path + '/' + file
        status, response = user_authentication(userid, password, wavfile)
        if status == "SUC":
            print("file: "+file+" passed voice authentication")
        else:
            print("file: "+file+" does not pass voice authentication")
if __name__ == "__main__":
    main()