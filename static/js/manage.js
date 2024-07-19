
// ロード後処理
jQuery(function($){

    $(document).ready(function(){

        pathname = location.pathname;
        console.log(pathname);

        if(pathname == "/grade"){

            console.log(student_id);
            console.log(score_list);
            console.log(s_score_list)

            $(".main-contents-part-title").find("p").text("生徒番号" + student_id + "さんの成績推移");

            // 実測値データ作成
            actual_score_list = []

            for(var i of Object.keys(score_list)){

                console.log(Number(i)+1);

                if(score_list[i] === null){
                    $("#individual-student-grade").find("tr").eq(Number(i)+1).append("<td>－</td>");
                    actual_score_list.push(null);
                }else{

                    if(typeof score_list[i] === "number"){
                        $("#individual-student-grade").find("tr").eq(Number(i)+1).append("<td>(" + score_list[i] + ")</td>");
                        actual_score_list.push(null);
                    }else{
                        $("#individual-student-grade").find("tr").eq(Number(i)+1).append("<td>" + score_list[i] + "</td>");
                        actual_score_list.push(score_list[i]);
                    }
                    
                }

                if(s_score_list[i] === null){
                    $("#individual-student-grade").find("tr").eq(Number(i)+1).append("<td>－</td>");
                }else{

                    if(typeof s_score_list[i] === "number"){
                        $("#individual-student-grade").find("tr").eq(Number(i)+1).append("<td>(" + s_score_list[i] + ")</td>");
                    }else{
                        $("#individual-student-grade").find("tr").eq(Number(i)+1).append("<td>" + s_score_list[i] + "</td>");
                    }
                    
                }

            }

            console.log(actual_score_list);

            // グラフ初期表示設定

            var ctx = document.getElementById('grade-chart');

            const aryMax = function (a, b) {return Math.max(a, b);}
            const aryMin = function (a, b) {return Math.min(a, b);}
            let score_max = actual_score_list.reduce(aryMax);
            let score_min = actual_score_list.reduce(aryMin);

            var line_options = {
                scales: {
                    yAxes: [{
                        ticks: {
                            min: Math.floor(score_min / 50) * 50,
                            max: 500
                        }
                    }]
                }
            };

            // var score = [,402,410,408,432,]
        
            line_datas = {
                    labels: ["第1回実力テスト","第2回実力テスト","第3回実力テスト","第4回実力テスト","第5回実力テスト","第6回実力テスト"],
                    datasets: [
                        {
                            label: "5教科合計点数",
                            data: actual_score_list,
                            borderColor: 'rgba(255, 100, 100, 1)',
                            lineTension: 0,
                            fill: false,
                            borderWidth: 3
                        },
                        {
                            label: "予測合計点数",
                            data: score_list,
                            borderColor: 'rgba(255, 100, 100, 1)',
                            lineTension: 0,
                            fill: false,
                            borderWidth: 3,
                            borderDash: [3, 3]
                        }
                        
                    ]
                };

            // dotted_line_datas = {
            //     labels: ["第1回実力テスト","第2回実力テスト","第3回実力テスト","第4回実力テスト","第5回実力テスト","第6回実力テスト"],
            //     datasets: [
            //         {
            //             label: "5教科合計点数",
            //             data: score_list,
            //             borderColor: 'rgba(255, 100, 100, 1)',
            //             lineTension: 0,
            //             fill: false,
            //             borderWidth: 3,
            //             borderDash: [3, 3]
            //         }
                    
            //     ]
            // };

            // var actual_grade_chart = new Chart(ctx, {
            //     type: 'line',
            //     data: line_datas,
            //     //   options: line_options
            // });   
        
            var grade_chart = new Chart(ctx, {
                type: 'line',
                data: line_datas,
                options: line_options
            });


        }else if(pathname == "/manage_grade"){

            console.log(grade_list);

            score = "－";
            s_score = "－";

            for(var i of Object.keys(grade_list)){

                $("#grade-table").append('<tr></tr');
                $("#grade-table tr").eq(-1).append("<td>" + ('000000' + grade_list[i][0][3]).slice(-6) + "</td>");
                
                console.log(i);
                console.log(grade_list[i]);

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

        }
    
        

        
  
    });
  });





  jQuery(function($){

    $(document).on('click', '#grade-table tr', reload)

  });

function reload(){
    student_id = $(this).find('td').eq(0).text();
    location.href = "/grade?student_id=" + Number(student_id);
  }