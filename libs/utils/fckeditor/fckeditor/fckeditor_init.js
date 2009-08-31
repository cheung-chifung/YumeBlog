window.onload = function () {
	var allPageTags = document.getElementsByTagName("textarea");
	var editors = new Array();
	for (i = 0; i < allPageTags.length; i++) {
		if (allPageTags[i].className == "vRichTextField") {
			el = allPageTags[i];
			var oFCKeditor = new FCKeditor(el.id);
			oFCKeditor.BasePath = el.attributes['dir'].nodeValue + '/fckeditor/'; // FCKeditor's base path
			oFCKeditor.Height = "400";
			oFCKeditor.Width = "800"
			oFCKeditor.ReplaceTextarea();
			editors.push(oFCKeditor);
		}
	}
};