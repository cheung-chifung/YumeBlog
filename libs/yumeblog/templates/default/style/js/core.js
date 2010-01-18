/**
 * @author hicro
 */

function show_reply(comment_id){
	el = $('comment-'+comment_id);
	quote = el.getFirst('p').get('text');
	user_name = el.getFirst('h4').getFirst('a').get('text');
	$('id_parent').value = comment_id;
	$('id_comment').value = '@'+user_name+'\n'+$('id_comment').value;
	$("id_comment").focus();
}
 
