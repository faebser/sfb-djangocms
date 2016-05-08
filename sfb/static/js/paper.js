$(document).ready(function () {
	'use strict';
	// read all the tags

	var mapToData = function (item) {
		var e = $(item);

		return {
			url: e.data('url'),
			text: e.text(),
			active: false
		}
	}

	$('.taglist.chosen, .taglist.mostUsed').css('display', 'none');

	var headers = {};
	var chosen = $('.taglist.chosen li').toArray().map(mapToData);
	headers['chosen'] = $('.taglist.chosen h2').text();
	var mostUsed = $('.mostUsed.taglist li').toArray().map(mapToData);
	headers['mostUsed'] = $('.mostUsed.taglist h2').text();

	$('#container .paper').on('click', '.close', function(event) {
			event.preventDefault();
			tags.toggleIssue();
	});

	$('#history').on('click', '.pagination', function(event) {
			event.preventDefault();
			var e = $(this);
			$.get(e.attr('href'), function(data) {
				var target = $('#history > ul');
				data = $(data);
				target.append(data.find('#history li.year'));
				if(data.find('#history .pagination').length != 0) {
					$('#history .pagination').attr('href', data.find('#history .pagination').attr('href'));
				}
				else {
					$('#history .pagination').remove();
				}
			});
		});


	var tags = new Vue({
		el: '#keywords',
		data: {
			chosen: chosen,
			mostUsed: mostUsed,
			headers: headers,
			tags: chosen.slice(0),
			articles: [],
			
			html: '',
			overlayHtml: '123123',
			overlayParentStyleObject: {
				height: ''
			},
			showOverlay: false,
			urls: {
				tags: 'tags/',
				issue: 'issue/'
			}
		},
		methods: {
			toggleHeader: function (header) {
				if (header === this.headers.chosen) {
					this.tags = this.chosen.slice();
					return;
				}
				this.tags = this.mostUsed.slice();
			},
			toggle: function (tag) {
				var self = this;
				tag.active = !tag.active;
				var url = this.getUrlForActiveTags();
				if (url !== this.urls.tags) {
					$.ajax({
					  url: this.getUrlForActiveTags(),
					  dataType: 'json',
					  success: function(data) {
					  	self.articles = data;
					  }
					});
					return;
				}
				self.articles = [];
			},
			toggleIssue: function (id) {

				if (this.showOverlay) {
					this.showOverlay = false;
					this.overlayHtml = '';
					return;
				}

				var self = this;
				this.showOverlay = true;
				$.ajax({
				  url: self.urls.issue + id + '/',
				  dataType: 'html',
				  success: function(data) {
				  	self.showOverlay = true;
				  	self.overlayHtml = data;

				  	self.$nextTick(function fixHeight () {
				  		self.overlayParentStyleObject.height = $(self.$els.overlayElement).height() + 'px';
				  	});
				  	
				  	$('html, body').animate({
				  		'scrollTop': $('#container').offset().top
				  	}, 500);
				  }
				});
				return;
			},
			getUrlForActiveTags: function () {
				return this.tags.reduce(function reducer (url, item) {
					if (item.active) {
						return url + item.url + '/';
					}
					return url;
				}, this.urls.tags);
			}
		}
	});
});