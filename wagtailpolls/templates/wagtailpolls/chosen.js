function(modal) {
    modal.respond('pollChosen', {{ snippet_json|safe }});
    modal.close();
}
