from flask import Flask, render_template, request, jsonify
from module import edit_grade, make_grade_list, conditional_search_csv, search_csv, make_student, add_predict_grade

app = Flask(__name__)

# 関数定義

def convert_score(score):

    if score == "":
        score = -1

    return score

# ルーティング

@app.route('/', methods=["GET","POST"])
def config_grade():

    if request.method == "GET":

        grade_list, msg, is_result = make_grade_list()
        # grade_list = add_predict_grade(grade_list)

        return render_template("config_grade.html", grade_list=grade_list)
    
    else:

        student_id = request.form["student_id"]
        student_id = int(student_id[4:10])
        # print(student_id[4:10])
        # print(int(student_id[4:10]))

        score = ""
        s_score = ""
        score_list = []
        s_score_list = []

        for i in range(6):

            request_score_arg = "score_" + str(i+1)
            request_s_score_arg = "s_score_" + str(i+1)

            score = request.form[request_score_arg]
            s_score = request.form[request_s_score_arg]

            score = convert_score(score)
            s_score = convert_score(s_score)

            score_list.append(score)
            s_score_list.append(s_score)

        # print(student_id)
        print(score_list)
        print(s_score_list)

        msg, is_result = edit_grade(student_id, score_list, s_score_list)
        print(msg)
        print(is_result)

        grade_list, msg, is_result = make_grade_list()
        # grade_list = add_predict_grade(grade_list)

        return render_template("config_grade.html", grade_list=grade_list)
    

@app.route('/manage_grade', methods=["GET"])
def manage_grade():

    grade_list, msg, is_result = make_grade_list()
    # grade_list = add_predict_grade(grade_list)

    return render_template("manage_grade.html", grade_list=grade_list)


@app.route('/grade', methods=["GET"])
def grade():

    student_id = request.args.get("student_id")
    search_result, msg, is_result = conditional_search_csv("grade.csv", "student_id", str(student_id))

    grade_list = [] 
    grade_list.append(search_result)
    print(grade_list)

    grade_list = add_predict_grade(grade_list)

    score_list = []
    s_score_list = []

    for i in range(len(grade_list[0])):

        if grade_list[0][i][1] == "-1" :
            score_list.append(None)
        else:
            score_list.append(grade_list[0][i][1])

        if grade_list[0][i][2] == "-1" :
            s_score_list.append(None)
        else:
            s_score_list.append(grade_list[0][i][2])

    print(score_list)
    print(s_score_list)

    student_id = student_id.zfill(6)

    print(student_id)

    return render_template("grade.html", student_id=student_id, score_list=score_list, s_score_list=s_score_list)


@app.route('/config_student', methods=["GET","POST"])
def config_student():

    if request.method == "GET":

        student_list, msg, is_result = search_csv("student.csv")

        return render_template("config_student.html", student_list=student_list)
    
    else:

        make_student()
        student_list, msg, is_result = search_csv("student.csv")

        return render_template("config_student.html", student_list=student_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
    # app.run(host='0.0.0.0', threaded=True)

