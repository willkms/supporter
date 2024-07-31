
// ロード後処理
jQuery(function($){

    $(document).ready(function(){

        pathname = location.pathname;
        console.log(pathname);

        $(".sidebar-menu-list").find("li").eq(2).addClass("clicked");
        $(".sidebar-menu-list ul").slideToggle();

        if(pathname == "/config_grade" || pathname == "/"){

            $(".sidebar-menu-list").find("ul").find("li").eq(1).addClass("current");
    
            console.log(grade_list);

            score = "－";
            s_score = "－";

            for(var i of Object.keys(grade_list)){

                $("#grade-table").append('<tr></tr');
                $("#grade-table tr").eq(-1).append("<td>" + ('000000' + grade_list[i][0][3]).slice(-6) + "</td>");
                
                console.log(i);
                console.log(grade_list[i]);
                // console.log(grade_list[i][j][1]);
                // console.log(typeof grade_list[i][j][1]);
                // console.log(grade_list[i][j][2]);
                // console.log(typeof grade_list[i][j][2]);

                for(var j=0;j<6;j++){
                    
                    if( j+1 ==  grade_list[i][j][4]){

                        if( grade_list[i][j][1] == -1 ){

                            score = "－";

                        }else if( typeof grade_list[i][j][1] === "number" ){

                            score = "(" + String(grade_list[i][j][1]) + ")";

                        }else{

                            score = String(grade_list[i][j][1]);

                        }

                        if( grade_list[i][j][2] == -1 ){

                            s_score = "－";

                        }else if( typeof grade_list[i][j][2] === "number" ){

                            s_score = "(" + String(grade_list[i][j][2]) + ")";

                        }else{

                            s_score = String(grade_list[i][j][2]);

                        }

                        $("#grade-table tr").eq(-1).append("<td><ul><li>" + score + "</li><li>" + s_score + "</li></ul></td>");

                    }else{

                        $("#grade-table tr").eq(-1).append("<td><ul><li>－</li><li>－</li></ul></td>");

                    }


                    
                }
                

            }

        }else if(pathname == "/config_student"){

            // console.log(student_list);

            $(".sidebar-menu-list").find("ul").find("li").eq(0).addClass("current");

            for(var i of Object.keys(student_list)){

                // console.log(i);

                $("#student-table").append('<tr></tr');
                // $("#student-table tr").eq(-1).append("<td>" + ('000000' + student_list[i][0]).slice(-6) + "</td>",
                //                                      "<td><button type='button' class='edit-button' id='student-edit-button'><img src='../static/img/edit.svg' alt='編集'></button></td>",
                //                                      "<td><button class='delete-button' type='button' id='student-delete-button'><img src='../static/img/delete.svg' alt='削除'></button></td>");
                $("#student-table tr").eq(-1).append("<td>" + ('000000' + student_list[i][0]).slice(-6) + "</td>",
                                                     "<td><button type='button' class='edit-button' id='student-edit-button'><div></div></button></td>",
                                                     "<td><button class='delete-button' type='button' id='student-delete-button'><div></div></button></td>");
            }

        }
  
    });
  });



// 編集、削除、テスト追加、戻る、登録(編集、削除)ボタン

jQuery(function($){

    $(document).on('click', '#grade-table tr', function (e) {

        student_num = $(this).find('td').eq(0).text();
        student_num = "生徒番号" + String(student_num) + "さん";

        $(".modal").addClass("show");
        $(".modal-title").find("p").text("成績編集");
        $(".modal-contents").find(".modal-form-row").eq(0).find("input").val(student_num);

        for(var i=0;i<7;i++){

            score = $(this).find('td').eq(i).find("li").eq(0).text();
            s_score = $(this).find('td').eq(i).find("li").eq(1).text();

            if(score == "－"){

                $(".modal-contents").find(".modal-form-list > li").eq(i-1).find("ul li").eq(-1).find(".modal-form-input").eq(0).find("input").val("");

            }else{

                $(".modal-contents").find(".modal-form-list > li").eq(i-1).find("ul li").eq(-1).find(".modal-form-input").eq(0).find("input").val(score);

            }

            if(s_score == "－"){

                $(".modal-contents").find(".modal-form-list > li").eq(i-1).find("ul li").eq(-1).find(".modal-form-input").eq(1).find("input").val("");

            }else{

                $(".modal-contents").find(".modal-form-list > li").eq(i-1).find("ul li").eq(-1).find(".modal-form-input").eq(1).find("input").val(s_score);

            }

            

        }

        // alert(student_num + "編集");
    
    });

    $(document).on('click', '.modal-form-cancel-button', function (e) {

        $(".modal").removeClass("show");

    });

    $(document).on('click', '#student-add-button', function (e) {

        form = $('<form></form>',{action:'/config_student',method:'POST'}).hide();

        form.append($('<input></input>',{type: 'hidden', name: 'mode', value: 0}));

        body = $('body');
        body.append(form);

        form.submit();
        return false;

    });

    $(document).on('click', '#student-delete-button', function (e) {

        var student_id = $(this).closest('tr').find('td').eq(0).text();

        form = $('<form></form>',{action:'/config_student',method:'POST'}).hide();

        form.append($('<input></input>',{type: 'hidden', name: 'mode', value: 2}));
        form.append($('<input></input>',{type: 'hidden', name: 'id', value: student_id}));

        body = $('body');
        body.append(form);

        form.submit();
        return false;

    });

    // $(document).on('click', '.modal-form-exe-button', function (e) {

    //     list_size = $('.modal-form-list').find("li").length;
    //     test_array = [];

    //     for(var i=0; i<list_size; i+=2){

    //         let test_val = $('.modal-form-list').find("li").eq(i).find("select").val();
    //         // console.log(list_size);
    //         // console.log(test_val);
    //         console.log(test_array);
            
    //         if(test_val == 0){

    //             alert("名前が選択されていないテストがあります");
    //             return false;

    //         } else{

    //             if($.inArray(test_val, test_array) !== -1){
    //                 alert("テスト名が重複しています");
    //                 return false;
    //             }

    //             test_array.push(test_val);
    //             console.log(test_array);
    //         }

    //     }

    // });

});

