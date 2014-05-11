$(document).ready(function(){
	$('.play').click(function(){
		embed_url = $(this).attr('data-embed')
		$.get('/embedcode?track=' + embed_url, function(data){
			var popup = $('<div />');
			popup.css({
				position : 'fixed',
				width : '500px',
				height : '400px',
				top : '50px',
				left : '50%',
				'margin-left' : '-250px',
				'z-index' : 100
			}).addClass('popup').html(data);
			var overlay = $('<div />').addClass('overlay')
			$('body').append(overlay);
			$('body').append(popup);
		});
	});
	$(document).on('click', '.overlay', function(e){
		$('.overlay, .popup').remove();
	})

	$('.vlc').click(function(){
		embed_url = $(this).attr('data-embed')
		$.get('/vlc/?track=' + embed_url);
	});

	$('.control-play').click(function(){
		if(embed_url = $(this).attr('data-embed')) {

		} else {
			embed_url = '';
		}
		$.get('/vlc/?track=' + embed_url);
	});

	$('.control-stop').click(function(){
		$.get('/stop_vlc/');
	});
	$('.control-pause').click(function(){
		$.get('/pause_vlc/');
	});

	var users = new Array()
	$('.user').each(function(){
		var text = $(this).text();
		if($.inArray(text, users) === -1) users.push(text)
	});

	users.sort();
	$(users).each(function(){
		$('.user_filter').append($('<option></option>').attr("value", this).text(this));
	});
	$(document).on('change', '.user_filter', function(){
		var user = $(this).val();
		$('.user').each(function(){
			$(this).parent().show();
			if($(this).text() != user){
				$(this).parent().hide();
			}
		});
	});
	$('.favourite h2').click(function(){
		$(this).next().slideToggle();
	});

});
