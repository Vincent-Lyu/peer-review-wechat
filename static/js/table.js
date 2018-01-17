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
    $.get('/post/'+scores);
    location.reload();
    alert('提交成功')
});
