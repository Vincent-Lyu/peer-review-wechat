$("input").click(function(){
    var scores = [];
    $("tbody tr.data").each(function(index){
        var row = [];
        var uid = $("tbody tr:nth-child("+(index+1)+") td:nth-child(2)").text();
        var score =$("tbody tr:nth-child("+(index+1)+") select").find(":selected").text(); 
        row.push(uid);
        row.push(score);
        scores.push(row);
    });
    var r = confirm("是否确认提交？\n提交后不能修改和查看分数");
    if(r == true) {
        $.get('/post/' + scores);
        alert("分数提交成功！");
    } else {
        alert("请重新打分");
    }
});
