var sfb = {};
var m = Mustache;

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
		console.log(returnCart);
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
			sfb.shop.init();
		}
		$('#noJs').addClass('hidden');
		$('.articles li article').click(function(event) {
			var e = $('section.paper').addClass('active');
			e.find('section').addClass('active');
			e.find('article').first().addClass('active');
		});
	};
	//return the module
	return module;
}(jQuery));

$(document).ready(sfb.main.init);