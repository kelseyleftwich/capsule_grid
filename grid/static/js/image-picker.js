
	var hashtable = {
	{% for article in articles%}
		{{article.0}} : '{{article.1}}',
	{% endfor %}
	} 


	$(":checkbox").each(function() {
	id = $(this).val();
		console.log($(this).attr('id'));
		$(this).wrap('<div class="photo-image">');
		/*$("#span_" + $(this).attr('id')).appendTo($(this).parent());*/

		{% if user.profile.profile_type == 'P' %}
		if(hashtable[id] == ''){
				$(this).parent().attr('style',
					'background-image:url(\'{% static "images/hanger.gif" %}\')');
				$("#p_" + $(this).attr('id')).removeAttr('hidden').appendTo($(this).parent());

			}
			else{
			$(this).parent().attr('style','background-image:url(\'' + '/media/'+hashtable[id] + '\')');
		}
		{% else %}
		if(hashtable[id] == ''){
				$(this).parent().attr('style',
					'background-image:url(\'{% static "images/hanger.gif" %}\')');
				$("#p_" + $(this).attr('id')).removeAttr('hidden').appendTo($(this).parent());

			}
			else{
			$(this).parent().attr('style','background-image:url(\'' + hashtable[id] + '\')');
		}
		{% endif %}
		$(this).parent().wrap('<div class="photo outfit_new">');
		$(this).parent().wrap('<label for="' + $(this).attr('id') + '">');

		if($(this).is(':checked')){
			$(this).parent().parent().parent().toggleClass("photo-selected");
			/*$("#span_" + $(this).attr('id')).removeClass('hidden');*/
		}
	});

		$(':checkbox').click(function() {
			$(this).parent().parent().parent().toggleClass("photo-selected");
			/*$("#span_" + $(this).attr('id')).toggleClass('hidden');*/
			

		});
	
