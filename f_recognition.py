import face_recognition
import json
import numpy as np
import os


def update_db():
    
    tp = input("Please give your tp number?(All small letter) ")
    amount = input("Please enter the balance of your account: ")

    with open('people.json') as json_file:
        jason_dic = json.load(json_file)
        
        # * Create the dictionary
        jason_dic[tp] = {}
    
        image_of_person = face_recognition.load_image_file("frame-"+tp+".jpg")
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
        jason_dic[tp]["face_id"] = person_face_encoding.tolist()
        jason_dic[tp]["balance"] = float(amount)

        os.remove("temp-"+tp+".jpg")

    # * Upadte the dictionary
    with open('people.json', 'w') as w_json_file:
        json.dump(jason_dic, w_json_file)



def compare_faces(student_id, input_amount):
    with open('people.json') as json_file:
        jason_dic = json.load(json_file)
    
    tp_number = "tp"+student_id
    if tp_number in jason_dic:
        # * Change the array to the numpy so we can use the compare function.
        known_face_encodings = np.array(jason_dic[tp_number]["face_id"])
        acount_credits = jason_dic[tp_number]["balance"] - float(input_amount)

        if acount_credits >= 0:
            unknown_image = face_recognition.load_image_file("temp-"+student_id+".jpg")
            # unknown_image = face_recognition.load_image_file("person_3.jpg")
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)
            result = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding, tolerance=0.5)
            
            if result[0]:
                jason_dic[tp_number]["balance"]=acount_credits
                with open('people.json', 'w') as w_json_file:
                    json.dump(jason_dic, w_json_file)
                print("face detected & amount deducted !!)")
            else:
                print("face not detected !!")   
        else:
            print("Please enter the right amount. ")
            print("Current balance is {}. ".format(jason_dic[tp_number]["balance"]))

if __name__ == "__main__":
    # known_face_save()
    # original_algorithms()
    update_db()
    # compare_faces("tp038733")

