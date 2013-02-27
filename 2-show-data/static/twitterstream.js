    (function() {
		var UpdatePanel = {
			init : function(options) {
				this.options = $.extend({
					interval : 5000,
					number : 3,
					hijackTweet : false
				}, options);

				this.updater();
			},

			updater : function() {
				(function updateBox() {
					this.timer = setTimeout(function() {
						updateIt();
						updateBox();
					}, UpdatePanel.options.interval);
				})();

				// get the ball rolling
				updateIt();

				function updateIt() {
					$.ajax({
						type : 'GET',
						url : UpdatePanel.options.url,
						dataType : 'jsonp',

						error : function() {},

						success : function(results) {
							var theTweets = '',
								 elem = UpdatePanel.options.elem.empty();

							$.each(results.results, function(index, tweet) {
								if ( UpdatePanel.options.hijackTweet ) {
									tweet.text = tweet.text.replace(/fashion/ig, '<b>fashion</b>');
								}

								if ( index === UpdatePanel.options.number ) {
									return false;
								}
								else {
                                    var c = tweet.created_at;
                                    var v=c.split(' ');

                                    var createdDate = '<span style="color:#F38094;float:right;">' + v[4] + '</span> ';
                                    var user = '<a href="http://twitter.com/' + tweet.from_user + '">' + tweet.from_user + '</a>';
									theTweets += '<li class="tweet"><img src="' + tweet.profile_image_url + '" style="float:left;padding-right:6px;"> '
                                    + createdDate + " " + user + ': '  + tweet.text + '</li>';
								}
							});
							elem.append(theTweets);
						}
					});
				}
			},

			clearUpdater : function() {
				clearTimeout(this.timer);
			}
		};
		window.UpdatePanel = UpdatePanel;
	})();

	UpdatePanel.init({
		interval : 15000,
		number : 15,
		url : "http://search.twitter.com/search.json?q=fashion",
		elem : $('#tweets'),
		hijackTweet : true


});

//$('#shopsense').
//http://www.shopstyle.com/action/apiGetTrends?pid=uid3649-8767593-82&format=json2&cat=109