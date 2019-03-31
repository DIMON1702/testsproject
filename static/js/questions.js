var questionCount;

$(document).ready(function () {

    questionCount = $('#test_container').children().length;

    $('#test_container').children()
        .each(function (index, element) {
            var questionContainer = $(element);
            questionContainer.children(".button-remove").click(function () {
                removeQuestion(questionContainer);
            })
        });

    // add new question event handler
    $('#add_question_button')
        .click(function () {
            var testContainer = $('#test_container');
            addQuestionTemplateToTest(testContainer);
        });

    // submit crete test form event handler
    $('#save_test_button').click(function () {
        var form = $('#test_form');
        var data = {};
        fillTestName(form, data);
        fillTestDescription(form, data);
        fillQuestions(form, data);
        var token = $("input[name='csrfmiddlewaretoken']").val()
        var jsonObj = JSON.stringify(data);
        $.ajax({
            url: '/test_upload',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': token,
                jsonObj
            },
            dataType: 'json',
            success: function (data) {
                window.location.href = '/' + data['redirect_url'];
            },
            error: function (data, e) {}
        });
    });

    // ==== Begin get post form data section ====

    var fillTestName = function (element, data) {
        data.test_name = $(element).find('.test-name').val();
    }

    var fillTestDescription = function (element, data) {
        data.test_description = $(element).find('.test-description').val();
    }

    var fillQuestions = function (test, data) {
        var testQuestions = [];
        $(test).find('.question')
            .each(function (index, element) {
                var question = {};

                question['text'] = $(element).find('.question-text').val();
                fillAnswers(question, element);

                testQuestions.push(question);
            });

        data['questions'] = testQuestions;
    }

    var fillAnswers = function (question, data) {
        var questionAnswers = [];
        $(data).find('li')
            .each(function (index, element) {
                var answer = {};
                var answerText = $(element).find('.answer');
                var isCorrectAnswer = $(element).find('.radio-answer').is(':checked');

                answer['answer_text'] = $(answerText).val();
                answer['isCorrect'] = isCorrectAnswer;

                questionAnswers.push(answer);
            });

        question['answers'] = questionAnswers;
    }

    // ==== End get post form data section ====

    // ==== Begin generate question section ====

    var addQuestionTemplateToTest = function (container) {
        var newQuestion = getNewQuestionTemplate(container);
        container.append(newQuestion);
    }

    var getNewQuestionTemplate = function (container) {
        questionCount += 1;

        // clone first element
        var questionTemplate = container.children(':first')
            .clone();

        // reset question text
        questionTemplate.find('.question-text').val('');

        // reset answers
        questionTemplate.find('li')
            .each(function (index, element) {
                var answer = $(element);
                answer.find('.radio-answer')
                    .attr('name', 'correct_answer_' + questionCount)
                    .prop("checked", false)
                    .val('answer_' + questionCount + '_' + index);

                answer.find('.answer')
                    .attr('name', 'answer_' + questionCount + '_' + index)
                    .val('');
            });

        // set remove question event handler
        questionTemplate.find('.button-remove')
            .click(function () {
                removeQuestion(questionTemplate);
            });

        return questionTemplate;
    }

    var removeQuestion = function (question) {
        if (!isValidMinQuestionCount()) {
            alert('Test should contain at least 5 tests');

            return;
        }

        question.remove();
    }

    // ==== End generate question section ====

    // ==== Begin post form data validation section ====

    var isValidMinQuestionCount = function () {
        return $('#test_container').children().length <= 5 ? false : true;
    }
    // ==== End post form data validation section ====
})