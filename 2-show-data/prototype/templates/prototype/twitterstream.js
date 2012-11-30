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
									theTweets += '<li>' + tweet.text + '</li>';
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
		interval : 5000,
		number : 5,
		url : "http://search.twitter.com/search.json?q=fashion",
		elem : $('#tweets'),
		hijackTweet : true
	});
