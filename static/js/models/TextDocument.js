var TextDocument = function (name, text) {
	this.Name = name;
	this.Text = text;
}

TextDocument.prototype.getShortText = function () {
	if (this.Text.length > 25) {
		return this.Text.substring(0, 25) + '...';
	} else {
		return this.Text;
	}
} 