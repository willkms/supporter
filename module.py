import csv
import operator
import itertools

import pandas as pd
import numpy as np
import lightgbm as lgb
from lightgbm import Dataset
from sklearn.model_selection import KFold
import pickle
import math

from pathlib import Path
THIS_FOLDER = Path(__file__).parent.resolve()

def search_csv(file_name):

    csv_path = THIS_FOLDER / "csv" / file_name
    search_result = ()
    is_result = 0
    msg = ""

    try:
        with open(csv_path, encoding="utf-8", mode="r") as f:
            reader = csv.reader(f)
            search_result = [row for row in reader]
            search_result = [row for row in search_result[1:]]
            is_result = 1

    except FileNotFoundError as e:
        msg = "CSVファイルが見つかりません。"
        is_result = 0

    except UnicodeDecodeError as e:
        msg = "文字コードエラー"
        is_result = 0

    except Exception as e:
        msg = "予期しないエラーが発生しました。"
        is_result = 0
        print(e.__class__.__name__) 
        print(e.args)
        print(e) 
        print(f"{e.__class__.__name__}: {e}") 

    return search_result, msg, is_result


def conditional_search_csv(file_name, condition_key, condition_value):

    csv_path = THIS_FOLDER / "csv" / file_name
    search_result = []
    all_search_result = []
    is_result = 0
    msg = ""

    column_num = -1
    column_list = []

    try:
        with open(csv_path, encoding="utf-8", mode="r") as f:
            reader = csv.reader(f)
            all_search_result = [row for row in reader]
            column_list = [x for row in all_search_result[:1] for x in row]
            all_search_result = [row for row in all_search_result[1:]]

            print(column_list)

            if condition_key != "" and condition_value != "":

                for i in range(len(column_list)):
                    if condition_key == column_list[i]:
                        column_num = i

                print("該当カラムの列番号：", column_num)

                if column_num != -1:

                    for i in range(len(all_search_result)):

                        if all_search_result[i][column_num] == condition_value:

                            search_result.append(all_search_result[i])

            is_result = 1

    except FileNotFoundError as e:
        msg = "CSVファイルが見つかりません。"
        is_result = 0

    except UnicodeDecodeError as e:
        msg = "文字コードエラー"
        is_result = 0

    except Exception as e:
        msg = "予期しないエラーが発生しました。"
        is_result = 0
        print(e.__class__.__name__) 
        print(e.args)
        print(e) 
        print(f"{e.__class__.__name__}: {e}") 

    return search_result, msg, is_result


def edit_grade(student_id, score_list, s_score_list):

    csv_path = THIS_FOLDER / "csv/grade.csv"
    test_num = -1

    try:

        with open(csv_path, encoding="utf-8", mode="r") as f:
            reader = csv.reader(f)
            data = list(reader)

            # print(data)

            for row in data:
                # print(row[3])
                # print(str(student_id))

                if row[3] == str(student_id):
                    test_num = int(row[4]) - 1
                    # print("変更前点数:", row[1])
                    # print("変更前偏差値:", row[2])
                    # print("test_id:", test_num)
                    row[1] = score_list[test_num]
                    row[2] = s_score_list[test_num]
                    # print("変更後点数:", row[1])
                    # print("変更後偏差値:", row[2])

            # print(data)

        try:

            with open(csv_path, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data)

                msg = "成績編集に成功しました。"
                is_result = 1

        except FileNotFoundError as e:
            msg = "CSVファイルが見つかりません。"
            is_result = 0

        except UnicodeDecodeError as e:
            msg = "文字コードエラー"
            is_result = 0

        except Exception as e:
            msg = "予期しないエラーが発生しました。"
            is_result = 0
            print(e.__class__.__name__) 
            print(e.args)
            print(e) 
            print(f"{e.__class__.__name__}: {e}") 
    
    except FileNotFoundError as e:
        msg = "CSVファイルが見つかりません。"
        is_result = 0

    except UnicodeDecodeError as e:
        msg = "文字コードエラー"
        is_result = 0

    except Exception as e:
        msg = "予期しないエラーが発生しました。"
        is_result = 0
        print(e.__class__.__name__) 
        print(e.args)
        print(e) 
        print(f"{e.__class__.__name__}: {e}") 

    return msg, is_result


def make_grade_list():

    csv_path = THIS_FOLDER / "csv/grade.csv"
    grade_list = [] #全体の3次元配列

    try:
        with open(csv_path, encoding="utf-8", mode="r") as f:
            reader = csv.reader(f)
            all_search_result = [row for row in reader]
            all_search_result = all_search_result[1:]

            # print(data)

            for row in all_search_result:
                row[3] = int(row[3])
            # print(all_search_result)
                    
            all_search_result = sorted(all_search_result, key=operator.itemgetter(3, 4))
            # print(all_search_result)

            for k, g in itertools.groupby(all_search_result, lambda x: x[3]):
                grade_list.append(list(g))

            # print(grade_list)

            msg = "成績情報を取得しました。"
            is_result = 1

    except FileNotFoundError as e:
        msg = "CSVファイルが見つかりません。"
        is_result = 0

    except UnicodeDecodeError as e:
        msg = "文字コードエラー"
        is_result = 0

    except Exception as e:
        msg = "予期しないエラーが発生しました。"
        is_result = 0
        print(e.__class__.__name__) 
        print(e.args)
        print(e) 
        print(f"{e.__class__.__name__}: {e}") 

    return grade_list, msg, is_result


def make_student():

    csv_path_student = THIS_FOLDER / "csv/student.csv"
    csv_path_grade = THIS_FOLDER / "csv/grade.csv"
    is_result = 0
    msg = ""

    student_id_list = search_csv("student.csv")[0]
    student_new_id = len(student_id_list) + 1
    print(student_new_id)

    grade_list = search_csv("grade.csv")[0]
    grade_new_id = len(grade_list) + 1
    print(grade_new_id)

    # data = [[student_new_id]]

    try:

        with open(csv_path_student, encoding="utf-8", mode="r") as f:
            reader = csv.reader(f)
            data = list(reader)
            print(data)
            data.append([student_new_id])

        try:

            with open(csv_path_student, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data)

            try:

                with open(csv_path_grade, encoding="utf-8", mode="r") as f:
                    reader = csv.reader(f)
                    data = list(reader)
                    print(data)

                    for i in range(1, 7):
                        data.append([grade_new_id + i - 1, -1, -1, student_new_id, i])

                    msg = "成績編集に成功しました。"
                    is_result = 1

                try:

                    with open(csv_path_grade, mode='w', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows(data)

                except FileNotFoundError as e:
                    msg = "CSVファイルが見つかりません。"
                    is_result = 0

                except UnicodeDecodeError as e:
                    msg = "文字コードエラー"
                    is_result = 0

                except Exception as e:
                    msg = "予期しないエラーが発生しました。"
                    is_result = 0
                    print(e.__class__.__name__) 
                    print(e.args)
                    print(e) 
                    print(f"{e.__class__.__name__}: {e}") 

            except FileNotFoundError as e:
                msg = "CSVファイルが見つかりません。"
                is_result = 0

            except UnicodeDecodeError as e:
                msg = "文字コードエラー"
                is_result = 0

            except Exception as e:
                msg = "予期しないエラーが発生しました。"
                is_result = 0
                print(e.__class__.__name__) 
                print(e.args)
                print(e) 
                print(f"{e.__class__.__name__}: {e}") 

        except FileNotFoundError as e:
            msg = "CSVファイルが見つかりません。"
            is_result = 0

        except UnicodeDecodeError as e:
            msg = "文字コードエラー"
            is_result = 0

        except Exception as e:
            msg = "予期しないエラーが発生しました。"
            is_result = 0
            print(e.__class__.__name__) 
            print(e.args)
            print(e) 
            print(f"{e.__class__.__name__}: {e}") 
    
    except FileNotFoundError as e:
        msg = "CSVファイルが見つかりません。"
        is_result = 0

    except UnicodeDecodeError as e:
        msg = "文字コードエラー"
        is_result = 0

    except Exception as e:
        msg = "予期しないエラーが発生しました。"
        is_result = 0
        print(e.__class__.__name__) 
        print(e.args)
        print(e) 
        print(f"{e.__class__.__name__}: {e}") 


def add_predict_grade(grade_list):

    # temp_test_id = 0
    predict_grade_list = []

    for i in range(len(grade_list)):

        temp_student_grade_list = []
        student_grade_df = pd.DataFrame(grade_list[i], columns=["grade_id", "score", "s_score", "student_id", "test_id"])
        student_grade_df = student_grade_df.astype({"student_id": "int64", "test_id": "int64"})        
        test_id = student_grade_df.loc[student_grade_df["score"] != "-1"]["test_id"].max() + 1
        predict_df = student_grade_df
        predict_df = predict_df.drop(columns=predict_df.columns[[0,1,2]]).reset_index(drop=True)
        predict_df = predict_df.astype({"test_id": "int64"})

        # print(student_grade_df.index.dtype)

        # print(student_grade_df)
        # print(predict_df)
        # print(test_id)
        # print()

        if not math.isnan(float(test_id)):

            if grade_list[i][-1][1] != "-1":
                pass

            else:

                test_id = int(test_id)

                for j in range(test_id, 7):

                    test_index = j - 2
                    student_id = int(grade_list[i][test_index][3])
                    name_list = ["second","third","fourth","fifth","sixth"]

                    score_model_path = "model/grade/score/predict_" + name_list[test_index] + "_score_model.pkl"
                    s_score_model_path = "model/grade/s_score/predict_" + name_list[test_index]  + "_s_score_model.pkl"
                    score_model_path = THIS_FOLDER / score_model_path
                    s_score_model_path = THIS_FOLDER / s_score_model_path

                    # print(j)
                    # print(test_index)

                    score_model = pickle.load(open(score_model_path, 'rb'))
                    s_score_model = pickle.load(open(s_score_model_path, 'rb'))

                    predict_score = score_model.predict(predict_df.loc[predict_df["test_id"] == j])
                    predict_s_score = s_score_model.predict(predict_df.loc[predict_df["test_id"] == j])
                    predict_score = predict_score.round()
                    predict_s_score = predict_s_score.round()

                    # print(student_grade_df)
                    # print(student_grade_df.loc[student_grade_df["test_id"] == test_id])
                    # print(predict_score)
                    # print(predict_s_score)

                    student_grade_df.loc[(student_grade_df["student_id"] == student_id) & (student_grade_df["test_id"] == test_id), "score"] = predict_score
                    student_grade_df.loc[(student_grade_df["student_id"] == student_id) & (student_grade_df["test_id"] == test_id), "s_score"] = predict_s_score

        # print(student_grade_df)
        temp_student_grade_list = student_grade_df.to_numpy().tolist()
        predict_grade_list.append(temp_student_grade_list)

    # print(predict_grade_list)

    return predict_grade_list

        

            


## CSV検索
# search_result, msg, is_result = search_csv("grade.csv")
# search_result, msg, is_result = search_csv("test.csv")
# search_result, msg, is_result = search_csv("sample.csv")
# search_result, msg, is_result = search_csv("student.csv")
# print(search_result)
# print(msg)
# print(is_result)

# # 条件付きCSV検索
# search_result, msg, is_result = conditional_search_csv("grade.csv", "student_id", "2")
# print(search_result)

# grade_list = []
# grade_list.append(search_result)
# print(grade_list)

# print(msg)
# print(is_result)

# # 成績編集
# student_id = 1
# score_list = [-1,-1,-1,-1,479,493]
# s_score_list = [-1,-1,-1,-1,74,75]
# # score_list = [-1,-1,-1,-1,-1,-1]
# # s_score_list = [-1,-1,-1,-1,-1,-1]

# edit_grade(student_id,score_list,s_score_list)

# # 成績データ取得
# grade_list, msg, is_result = make_grade_list()
# print(grade_list)

#生徒新規登録
# make_student()

# # 成績データ予測値補完
# # 実測値の型：str、予測値の型：float
# grade_list, msg, is_result = make_grade_list()
# # print(grade_list)
# predict_grade_list = add_predict_grade(grade_list)
# # print(predict_grade_list)

# # print(predict_grade_list[0][5][1])
# # print(type(predict_grade_list[0][5][1]))
# # print(predict_grade_list[0][5][2])
# # print(type(predict_grade_list[0][5][2]))
# # print(predict_grade_list[1][5][1])
# # print(type(predict_grade_list[1][5][1]))
# # print(predict_grade_list[1][5][2])
# # print(type(predict_grade_list[1][5][2]))