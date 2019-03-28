var questionCount;

$(document).ready(function() {
    
    // ToDo: check that question count starts from 0 or 1
    questionCount = $("#test_container").children().length;
    
    $("#test_container").children()
        .each(function () {
            var questionContainer = $(this);
            questionContainer.children(":button").click(function () {
                removeQuestion(questionContainer);
        }) 
    });

    // add new question event handler
    $("#add_question_button")
        .click(function () {
            var testContainer = $("#test_container");
            addQuestionTemplateToTest(testContainer)
        });

    // validate and submit form event
    $("#save_test_button").click(function() {
        //validate and submit form
        if(!isFormValid()){
            alert ("fail");
            return;
        }

        // ToDo: add post form request Sasha
        alert("saved")
    })
});

function addQuestionTemplateToTest (container) {
    var newQuestion = getNewQuestionTemplate(container);
    container.append(newQuestion); 
}

function getNewQuestionTemplate (container) {
    questionCount += 1;
    
    // clone first element
    var questionTemplate = container.children(":first")
        .clone();

    // reset question text
    questionTemplate.find("textarea")
        .val('');

    // reset answers
    questionTemplate.find("li")
        .each(function(index) {
            var answer = $(this);
            answer.find(":input[type='radio']")
                .attr("name", "correct_answer_" + questionCount)
                .attr("checked", true)
                .val("answer_" + questionCount + "_" + index);

            answer.find(":input[type='text']")
                .attr("name", "answer_" + questionCount + "_" + index)
                .val('')
        });

    // set remove question event handler
    questionTemplate.find(":button")
        .click(function () {
            removeQuestion(questionTemplate)
        });

    return questionTemplate;
}

function removeQuestion(question) {
    if(!isValidMinQuestionCount()){
        alert("Test should contain at least 5 tests");  
        return;
    }
    question.remove();
}

// form validation 
function isValidMinQuestionCount () {
    return $("#test_container").children().length <= 5 ? false : true;
}

function isFormValid(){
    return isValidMinQuestionCount()  ? true : false;
}
