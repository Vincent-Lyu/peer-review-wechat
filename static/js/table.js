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
    alert('你已提交成功，若重复提交，以最后一次提交的分数为准')
});
