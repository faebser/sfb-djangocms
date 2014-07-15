var sfb = {};
var m = Mustache;

sfb.shop = (function ($) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var c = {
			'hidden': 'hidden',
			'children': 'children',
			'show': 'show'
		},
		cart = $("#cart"),
		total = $('#total'),
		parentItems = $('#shop > .container'),
		overlay = $('#overlay ul'),
		win = $(window),
		urls = {
			'add': 'addToCart/',
			'checkout': 'checkout/'
		},
		templates = {
			'total': '{{amount}} CHF'
		},
		module = {};
	// private methods
	var showItemInOverlay = function (items, parentName) {
		items.clone().appendTo(overlay);
		overlay.parent().addClass(c.show);
		overlay.data('parentName', parentName);
	},
	closeOverlay = function () {
		overlay.parent().removeClass(c.show);
		overlay.find('li').remove();
		overlay.css('height', ''); 	
	},
	clickHandler = function () {
		parentItems.on('click.sfb.shop', function(event){
			showItemInOverlay($(this).find('.' + c.children + ' li'), $(this).find('h2').html());
		});

		overlay.parent().on('click.sfb.shop', closeOverlay);

		overlay.on('click.sfb.shop', 'li', function(event) {
			console.log("add to cart");
			var e = $(this);
			var settings = getAjaxSettings(urls.add, {
				'itemId': e.data('id'),
				'amount': 1,
				'type': e.data('type')
			});

			$.ajax(settings).done(function(data) {
				var context = {
					'parentName': overlay.data('parentName'),
					'name': e.find('h2').html(),
					'amount': data.amount,
					'price': data.price
				};
				addHtmlToCart($(m.render(data.template, context)));
			});
		});
	},
	addHtmlToCart = function (html) {
		cart.find('tr').last().before(html);
		updateCart();
	},
	updateCart = function () {
		var add = cart.find('td.right').not('#total'),
			amount = 0;
		add.each(function(index, element){
			var e = $(element);
			amount += parseFloat(e.html());
		});
		total.html(m.render(templates.total, {'amount': amount.toPrecision(3)}));
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
		if(main.find('#shop').lenght != 0) {
			sfb.shop.init();
		}
	};
	//return the module
	return module;
}(jQuery));

$(document).ready(sfb.main.init);