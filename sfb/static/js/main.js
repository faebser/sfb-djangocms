var sfb = {};
var m = Mustache;

sfb.paper = (function ($, Vue) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {},
		tagHeaders = null,
		tagHeadersList = null,
		tagList = null,
		tagListItems = null,
		articleList = $('.articles'),
		overlay = $('#container .paper'),
		message = $('#message'),
		messageOverlay = $('#paper-overlay'),
		c = {
			'active': 'active',
			'show': 'show'
		},
		urls = {
			'tag': 'tags/',
			'issue': 'issue/'
		};
	// private methods
	var parseTagList = function () {
		var headers = [];
		tagList = $('#tagList');
		$('.taglist').each(function(index, element) {
			var e = $(element);
			headers.push(e.find('h2').html());
			e.find('h2').remove();
			e.clone().appendTo(tagList).removeClass('taglist');
		});
		tagHeaders = new Vue({
			'el': '#tagHeader',
			'data': {
				'tags': headers
			},
			'methods': {
				'toggle': function(header) {
					$.each(tagListItems, function(index, e) {
						e.removeClass(c.active);
					});
					$.each(tagHeadersList, function(index, e) {
						e.removeClass(c.active);
					});
					tagHeadersList[header.$index].addClass(c.active);
					tagListItems[header.$index].addClass(c.active);
					tagList.find('li').removeClass(c.active);
				}
			}
		});

		tagHeadersList = $('#tagHeader').find('li').map(function(){
			return $(this);
		}).get();

		tagListItems = tagList.find('ul').map(function() {
			return $(this);
		}).get();

		$('.taglist').remove();
		if(tagHeadersList[0]) tagHeadersList[0].click();
	},
	clickHandler = function () {
		tagList.find('li').on('click', function(event) {
			var e = $(this);
			e.toggleClass(c.active);
			if(tagList.find('li.' + c.active).length != 0) {
				closeOverlay();
				var tagUrls = tagList.find('li.' + c.active).map(function() {
					return $(this).data('url')
				}).get().join('/');
				$.ajax({
				  url: urls.tag + tagUrls + '/',
				  dataType: 'html',
				  success: function(data) {
				  	articleList.html(data);
				  }
				});
			}
			else {
				articleList.html('');
			}
		});
		articleList.on('click', 'li article', function(event) {
			var e = $(this);
			$.ajax({
			  url: urls.issue + e.data('url') + '/',
			  dataType: 'html',
			  success: function(data) {
			  	openOverlay(data, e.attr('id'));
			  	$('html, body').animate({
			  		'scrollTop': $('#container').offset().top
			  	}, 500);
			  }
			});
		});
		overlay.on('click', '.close', function(event) {
			event.preventDefault();
			closeOverlay();
		});
		$('#paperParent h1').on('click', function(event) {
			var e = $(this);
			e.toggleClass(c.show);
			if(e.hasClass(c.show)) {
				$(this).parent().height('auto');
			}
			else {
				e.parent().height(e.outerHeight(true));
			}
			
		});
		$(document).on('click', '.pdf-download', function(event, letItSlide) {
			var e = $(this);
			if(!letItSlide || letItSlide === false) {
				event.preventDefault();
				if(!$.cookie('counter')) $.cookie('counter', 0);
				var counter = parseInt($.cookie('counter'));
				if(counter >= 5) {
					messageOverlay.html(message.html());
					messageOverlay.find('.overlayButtonWrapper a').attr('href', $(this).attr('href')).on('click', function(event) {
						messageOverlay.toggleClass(c.show);
					});
					messageOverlay.toggleClass(c.show);
					$.cookie('counter', 0);
				}
				else {
					$.cookie('counter', ++counter);
					e.trigger('click', [true]);
				}
			}
			else {
				window.open(e.attr('href'));
			}
		});
		$('#history').on('click', '.pagination', function(event) {
			event.preventDefault();
			var e = $(this);
			$.get(e.attr('href'), function(data) {
				var target = $('#history > ul');
				data = $(data);
				console.log(data.find('#history ul li.year'));
				target.append(data.find('#history li.year'));
				if(data.find('#history .pagination').length != 0) {
					$('#history .pagination').attr('href', data.find('#history .pagination').attr('href'));
				}
				else {
					$('#history .pagination').remove();
				}
			});
		});
	},
	openOverlay = function (html, articleId) {
		overlay.html(html);
	  	overlay.parent().height(overlay.height());
	  	overlay.addClass(c.show);
	  	showArticelById(articleId);
	  	
	},
	closeOverlay = function () {
		overlay.removeClass(c.show);
		window.setTimeout(function(){
			overlay.parent().height('auto');
		}, 770);
	},
	makeHeadlinesSmall = function () {
		$('#paperParent h1').each(function(index, element) {
			var e = $(element);
			e.parent().height(e.outerHeight(true));
		})
	},
	showArticelById = function (id) {
		var e =	overlay.find('#'+id).addClass(c.show);
		window.setTimeout(function(){
			e.removeClass(c.show);
		}, 2000);
	};
	// public methods
	module.init = function () {
		parseTagList();
		makeHeadlinesSmall();
		clickHandler();
	};
	//return the module
	return module;
}(jQuery, Vue));


sfb.shop = (function ($) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var c = {
			'hidden': 'hidden',
			'children': 'children',
			'show': 'show',
			'stay': 'stay'
		},
		tempCart = {},
		cart = $("#cart"),
		total = $('#total'),
		parentItems = $('#shop > .container'),
		overlay = $('#overlay ul'),
		stop = $('#stop'),
		go = $('#go'),
		win = $(window),
		currentTransaction = {},
		adressOverlay = $('#adressOverlay'),
		render_cart = {},
		buy = $('#buy'),
		buy2 = $('#buy2'),
		urls = {
			'add': 'addToCart/',
			'checkout': 'checkout/'
		},
		templates = {
			'total': '{{amount}} CHF',
			'priceModel': '{{amount}} à {{price}} CHF',
			'row': '{{#.}}<tr><td>{{name}}</td><td>{{amount}} à {{price}} CHF</td><td class="right">{{total}} CHF</td></tr>{{/.}}',
		},
		module = {};
	// private methods
	var showItemInOverlay = function (items, parentName) {
		items.clone().appendTo(overlay);
		items.each(function(index, element) {
			var e = $(element);
			var id = e.data('id');
			currentTransaction[id] = tempCart[id] || { 'amount': 0, 'price': 0, 'name': e.find('.itemData h2').html() };
			if(currentTransaction[id].amount != 0) {
				e.find('.tempPrice').html(m.render(templates.priceModel, currentTransaction[id]));
			} // it is not empty, so we render the template into the item
		});
		overlay.parent().addClass(c.show);
		overlay.data('parentName', parentName);
	},
	closeOverlay = function () {
		overlay.parent().removeClass(c.show);
		overlay.find('li').remove();
		overlay.css('height', '');
		
		for(var i in currentTransaction) {
			if(currentTransaction[i].amount != 0) tempCart[i] = currentTransaction[i];
		}
		currentTransaction = {};
		updateCart();
	},
	quitOverlay = function () {
		overlay.parent().removeClass(c.show);
		overlay.find('li').remove();
		overlay.css('height', '');
		
		currentTransaction = {};
		updateCart();
	},
	computePrice = function () {
		var return_float = (this.amount * this.price);
		if(return_float < 1) return return_float.toPrecision(2);
		return (this.amount * this.price).toPrecision(3);
	},
	clickHandler = function () {
		parentItems.on('click.sfb.shop', function(event){
			showItemInOverlay($(this).find('.' + c.children + ' li'), $(this).find('h2').html());
		});

		overlay.on('click.sfb.shop', 'li .icon-plus-circled', function(event) {
			event.stopPropagation();
			updateTempCart($(this), 1, $(this).parent().data('id'));
		});

		overlay.on('click.sfb.shop', 'li .icon-minus-circled', function(event) {
			event.stopPropagation();
			updateTempCart($(this), -1, $(this).parent().data('id'));
		});

		go.on('click.sfb.shop', function(event){
			event.preventDefault();
			closeOverlay();
		});

		stop.on('click.sfb.shop', function(event){
			event.preventDefault();
			quitOverlay();
		});

		buy.on('click.sfb.shop', function(){
			event.preventDefault();
			// get form and display overview
			$.get('form', function(data) {
				adressOverlay.append($(data));
			});
			adressOverlay.addClass(c.show);
		});

		adressOverlay.on('submit.sfb.shop', '#buy-form', function(){
			event.preventDefault();
			var form = $('#buy-form');
			var formData = {
				'cart': JSON.stringify(serializeCart(tempCart)),
				'csrfmiddlewaretoken': $.cookie('csrftoken')
			};

			form.find(":input").each(function(index, e){
				formData[e.name] = $(e).val();
			});
			
			$.ajax({
	            type: 'post',
	            url: form.attr('action'),
	            data: formData,
	            success: function (data) {
	            	if(data.status && data.status === 'success') {
	                	form.html('<h2 class="closeOverlay">Vielen Dank!</h2> <p class="closeOverlay">Sie werden in Kürze ein E-Mail als Bestätigung erhalten.</h2>');
	            	}
	            	else {
	            		form.remove();
	            		adressOverlay.html($(data));	
	            	}
	            },
	            error: function(data) {
	                console.error(data);
	            }
	        });
		});

		adressOverlay.on('click.sfb.shop', '.closeOverlay', function() {
			adressOverlay.removeClass(c.show);
			adressOverlay.find('*').remove();
			location.reload();
		});
	},
	serializeCart = function (cart) {
		var returnCart = jQuery.extend(true, {}, cart);
		
		for(var key in returnCart) {
			delete returnCart[key].computePrice;
			delete returnCart[key].total;
		};
		return returnCart;
	},
	addHtmlToCart = function (html) {
		cart.find('tr').last().before(html);
		updateCart();
	},
	cleanCart = function () {
		cart.find('tbody > tr').not("."+c.stay).remove();	
	},
	updateCart = function () {
		var total_price = 0;
		var flat_list = [];

		for(var id in tempCart) {
			var current = tempCart[id];
			current['total'] = computePrice;
			total_price += parseFloat(current['total']());
			flat_list.push(current);
		}

		cleanCart();
		cart.find('tr').last().before(m.render(templates.row, flat_list));

		total.html(m.render(templates.total, {'amount': parseFloat(total_price).toPrecision(3)}));
	},
	getAjaxSettings = function (url, data) {
		return {
			'url': url,
			'headers': {
				"X-CSRFToken": $.cookie('csrftoken')
			},
			'data' : data,
			'type': 'POST'
		};
	},
	getPriceModel = function (e) {
		return e.parent().data('price');
	},
	getPrice = function (priceModel, amount) {
		var diff;
		for (var key in priceModel) {
			diff = amount - key;
			if(diff < 0 || diff === 0) { // we found something
				return priceModel[key];
			}
		}
	},
	updateTempCart = function (e, amount, id) {
		var current = currentTransaction[id];
		current.amount += amount;
		current.price = getPrice(getPriceModel(e), current.amount);
		if(current.amount == 0 || current.amount < 0) {
			current.amount = 0;
			e.parent().find('.tempPrice').html('');
		}
		else {
			e.parent().find('.tempPrice').html(m.render(templates.priceModel, current));
		}
	};
	// public methods
	module.init = function () {
		$('#noJs').addClass(c.hidden);
		clickHandler();
	};
	//return the module
	return module;
}(jQuery));

sfb.main = (function ($) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var main = $('#main'),
		module = {};
	// private methods
	// public methods
	module.init = function () { // init all the other modules
		if(main.find('#shop').length != 0) {
			//sfb.shop.init();
		}
		$('#noJs').addClass('hidden');
		$('.articles li article').click(function(event) {
			var e = $('section.paper').addClass('active');
			e.find('section').addClass('active');
			e.find('article').first().addClass('active');
		});
		// if(sfb.paper) sfb.paper.init();
	};
	//return the module
	return module;
}(jQuery));

Vue.directive('shop-container', {
	cssClass: 'show',
	overlay: null,
	size: 0,
	small: 140,
	items: null,
	bind: function() {

		var self = this;
		var e = $(this.el);

		console.log(e);

		this.overlay = e.find('.overlay');
		this.size = e.height();
		//e.height(this.small);
		console.log(e.height());
		e.addClass('ready');
		this.items = e.find('ul > li');
		$.each(this.items, function(index, ele) {
			console.log($(ele).height());
		});

		e.find('.trigger').click(function() {
			self.overlay.toggleClass(self.cssClass);
			self.items.toggleClass(self.cssClass);
			e.toggleClass(self.cssClass);
			if(e.hasClass(self.cssClass)) {
				e.height('');
			}
			else {
				e.height(self.small);
			};
		});
	}
});

Vue.directive('price-container', {
	cssClass: 'fixed',
	threshold: 0,
	win: $(window),
	bind: function() {
		var self = this;
		var e = $(this.el);
		var spacer = e.parent().find('.spacer-fixed');
		self.threshold = e.offset().top - $('.noJs').outerHeight(true);
		self.win.on('scroll', function() {
			var scrollTop = self.win.scrollTop();
			if(!e.hasClass(self.cssClass) && scrollTop > e.offset().top) {
				e.addClass(self.cssClass);
				var h = e.height();
				self.threshold = e.offset().top;
				spacer.height(h);
				return;
			}
			if(e.hasClass(self.cssClass) && scrollTop < self.threshold) {
				e.removeClass(self.cssClass);
				spacer.height(0);
				return;
			}
		});
	}
});

var newShop = (function ($, Vue, _) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {},
		cart = undefined,
		price = undefined,
		overlay = undefined,
		prices = Array(),
		app = undefined;
	// private methods
	var formatFloatForCHF = function(input) {
		if(input >= 10) return parseFloat(input).toPrecision(4);
		return parseFloat(input).toPrecision(3);
	};
	// public methods
	module.init = function () {
		"use strict";

		overlay = new Vue({
			el: '.image-overlay',
			data: {
				'imageSource': null,
				'isHidden': true
			},
			methods: {
				toggleOverlay: function (url) {					
					if(this.isHidden && url) {
						this.imageSource = url;
					}
					if(!this.isHidden && !url) {
						this.imageSource = null;
					}
					this.isHidden = !this.isHidden;
				}
			}
		});

		

		price = new Vue({
			el: '.money',
			data: {
				cartList: {},
				totalPrice: 0
			},
			methods: {
				updateItem: function(id, text, amount, price) {
					id = 'id-' + id;
					if(this.cartList[id] && amount === 0) {
						this.cartList.$delete(id);
						this.totalPrice = this.computeTotalPrice();
						return;
					}
					if(!this.cartList[id]) this.cartList.$add(id, {'text': '', 'amount':'', 'price': 0});
					this.cartList[id]['amount'] = amount;
					this.cartList[id]['text'] = text;
					this.cartList[id]['price'] = price;
					this.totalPrice = this.computeTotalPrice();
				},
				computeTotalPrice: function () {
					if(this.cartList.length === 0) return 0;
					var tempFloat = parseFloat(_.reduce(this.cartList, function getTheTotalFromList(result, value, key) {
						result += value.amount * value.price;
						return result;
					}, 0));
					return formatFloatForCHF(tempFloat);
				},
				formatFloatForCHF: function(input) {
					return formatFloatForCHF(input);
				}
			}
		});

		cart = Vue.extend ({
			data: function () { return {
				stuff: 'stuff',
				amounts: {},
				priceModel : null,
				prevPrice: 0,
				nextPrice: 0,
				prevAmount: 0,
				nextAmount: 0,
				currentPrice: 0,
				currentTotal: 0,
				hasPrice: true
			}},
			methods: {
				showBigPicture: function (url, event) {
					event.preventDefault();
					overlay.toggleOverlay(url);
				},
				addOneItem: function(e) {
					this.amounts['id-' + e].amount += 1;
					this.currentTotal = this.calculateCurrentTotal();
					this.hasPrice = this.currentTotal == 0;
					price.updateItem(e, this.amounts['id-' + e].text, this.amounts['id-' + e].amount, this.currentPrice);
				},
				removeOneItem: function(e) {
					if(this.amounts['id-' + e].amount != 0) this.amounts['id-' + e].amount -= 1;
					this.currentTotal = this.calculateCurrentTotal();
					this.hasPrice = this.currentTotal == 0;
					price.updateItem(e, this.amounts['id-' + e].text, this.amounts['id-' + e].amount, this.currentPrice);
				},
				calculateCurrentTotal: function() {
					var diff;
					if(this.totalAmount === 0) return 0;
					for (var i = 0; i < this.priceModel.length; i++) {
						var item = this.priceModel[i];
						diff = this.totalAmount - parseInt(item.amount);
						
						if (diff < 0 || diff === 0 || i + 1 == this.priceModel.length) { // we found something
							if (i >= 1) {
								this.prevPrice = this.priceModel[i - 1].price;
								this.prevAmount = this.priceModel[i - 1].amount;
							}
							else {
								this.prevPrice = 0;
								this.prevAmount = 0;
							}
							if (i + 1 < this.priceModel.length) {
								this.nextPrice = this.priceModel[i + 1].price
								this.nextAmount = this.priceModel[i + 1].amount;
							}
							else {
								this.nextPrice = 0;
								this.nextAmount = 0;
							}
							this.currentPrice = item.price.toPrecision(3);
							var returnPrice = parseFloat(item.price * this.totalAmount);
							if(returnPrice >= 10) return returnPrice.toPrecision(4);
							return returnPrice.toPrecision(3);
						}
					}
				}
			},
			computed: {
				totalAmount: function () {
					var sum = 0;
					$.each(this.amounts, function(index, element) {
						sum += element.amount;
					});
					return sum;
				}
			},
			events: {
				'hook:beforeCompile': function() {
					var self = this;
					// build the basis data
					var e = $(this.$el);
					e.find('ul > li').each(function(index, element) {
						var el = $(element);
						self.amounts.$add('id-'+ el.data('id'), {
							'id': e.attr('id'),
							'amount': 0,
							'text': el.find('h2').html()
						});
					});
					// we take the price from json
					this.priceModel = e.data('price');
					// we have to make sure they are sorted so we can do magic stuff to them
					this.priceModel.sort(function sortByPriceKey(a, b) {
						var aValue = parseInt(a.amount);
						var bValue = parseInt(b.amount);
						if (aValue === bValue) return 0;
						if (aValue > bValue) return 1;
						if (aValue < bValue) return -1;
					});
				}
			}
		});

		app = new Vue({
			el: '',
			data: {
				amounts: {}
			},
			methods: {
				addOneItem: function(category, name) {

				},
				removeOneItem: function(category, name) {

				}
			},
			components: {
				'sfb-price': price,
				'sfb-item': cart
			},
			created: function () {
				this.$on('add-item', function(category, name) {
					return this.addOneItem(category, name);
				});
				this.$on('remove-item', function(category, name) {
					return this.removeOneItem(category, name);
				});

				this.$on('test123', function() {
					console.log("fasdfasdf");
				});


			},
			events: {
				'test123': function() {
					console.log('123');
				}
			}
		});

		app.$dispatch('test123');
		app.$broadcast('test123');

		
	};
	//return the module
	return module;
}(jQuery, Vue, _));

$(document).ready(newShop.init);

$(document).ready(sfb.main.init);