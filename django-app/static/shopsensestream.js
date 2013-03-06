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
						dataType : 'json',

						error : function() {},

						success : function(results) {
							var theTweets = '',
								 elem = UpdatePanel.options.elem.empty();



							$.each(results.trends, function(index, Trends) {
								/*if ( UpdatePanel.options.hijackTweet ) {
									tweet.text = tweet.text.replace(/fashion/ig, '<b>fashion</b>');
								}*/

                                //console.log(Trends);

								if ( index === UpdatePanel.options.number ) {
									return false;
								}
								else {

                                    var photo = '<img src="'+ Trends.product.images[0].url +'" style="float:left; padding-right:5px;">';

									theTweets += '<li class="trend">' + photo + Trends.brand + ', '
                                    + Trends.category + ', ' + Trends.product.priceLabel + '<br /><a href="' + Trends.url
                                    + '">' + Trends.product.name + '</a></li>';
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
		number : 18,
		url : "http://www.shopstyle.com/action/apiGetTrends?pid=uid3649-8767593-82&format=json",
		elem : $('#shopsense'),
		hijackTweet : true
	});
//&cat=109 //shoes