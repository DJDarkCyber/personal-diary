$(document).ready(function() {

    $(".writeContentButton").click(function(){

        var currentDisplay = $(".writeYourDiaryContainer").css('display');
        if(currentDisplay == 'block'){
            // $('.writeYourDiaryContainer').css("display", "none");
            $('.writeYourDiaryContainer').slideUp();
            $('.writeContentButton').html("Write   <i class=\"bi bi-plus-square\" style=\"margin-left: 6px;\"></i>");
        }
        else if(currentDisplay == 'none'){
            // $(".writeYourDiaryContainer").css("display", "block");
            $('.writeYourDiaryContainer').slideDown();
            $('.writeContentButton').html("Close   <i class=\"bi bi-dash-square\" style=\"margin-left: 6px;\"></i>");
        }
        
    })

    



});