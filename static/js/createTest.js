$(document).ready(function () {
	$('#save_test').submit(function (event) {
		alert("asdasda")
	});


	$('#test_form').submit(function (event) {
		var data = {}
		fillTest(this, data)
		fillQuestions(this, data)
		var jsonObj = JSON.stringify(data)
		$.post("create_test", jsonObj);
	});

	var fillTest = function (element, data) {
		data.test_name = $(element).find('#test_name').val()
	}

	var fillQuestions = function (test, data) {
		var questions = $(test).find('.question')
		$.each(questions, function (index, element) {
			data['question' + index] = {}
			data['question' + index]['text'] = $(element).find('.question_text').val()
			var answer_block = $(element).find('li')
			fillAnswers(data['question' + index], answer_block)
		}, data);
	}

	var fillAnswers = function (question, answer_block) {
		answers = $(answer_block).find('.answer')
		$.each(answers, function (index, element) {
			var answer_number = 'answer' + index
			question[answer_number] = {}
			question[answer_number]['answer_text'] = $(element).val()
			var answer_name = $(element).attr('name')
			question[answer_number]['isCorrect'] = checkIsCorrect(answer_name)
		}, question);
	}

	var checkIsCorrect = function (answer_name) {
		return $('.radio_answer:input[value=' + answer_name + ']').attr('checked') == 'checked'
	}
})