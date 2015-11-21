function createPollChooser(id) {
	console.log('got here');
	var chooserElement = $('#' + id + '-chooser');
	var docTitle = chooserElement.find('.title');
	var input = $('#' + id);
	var editLink = chooserElement.find('.edit-link');
	console.log(editLink);
	var pollChooser = "/admin/polls/choose/";

	$('.action-choose', chooserElement).click(function() {
		console.log('whoop');
		ModalWorkflow({
			url: pollChooser,
			responses: {
				pollChosen: function(pollData) {
					input.val(pollData.id);
					docTitle.text(pollData.string);
					chooserElement.removeClass('blank');
					editLink.attr('href', pollData.edit_link);
				}
			}
		});
	});

	$('.action-clear', chooserElement).click(function() {
		input.val('');
		chooserElement.addClass('blank');
	});
}
