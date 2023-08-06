	(function () {
		var fabric = __init__ (__world__.com.fabricjs).fabric;
		var orthoWidth = 1000;
		var orthoHeight = 750;
		var fieldHeight = 650;
		var __left0__ = tuple ([13, 27, 32]);
		var enter = __left0__ [0];
		var esc = __left0__ [1];
		var space = __left0__ [2];
		window.onkeydown = (function __lambda__ (event) {
			return event.keyCode != space;});
		var Attribute = __class__ ('Attribute', [object], {
			get __init__ () {return __get__ (this, function (self, game) {
				self.game = game;
				self.game.attributes.append (self);
				self.install ();
				self.reset ();
			}, '__init__');},
			get reset () {return __get__ (this, function (self) {
				self.commit ();
			}, 'reset');},
			get predict () {return __get__ (this, function (self) {
				// pass;
			}, 'predict');},
			get interact () {return __get__ (this, function (self) {
				// pass;
			}, 'interact');},
			get commit () {return __get__ (this, function (self) {
				// pass;
			}, 'commit');}
		});
		var Sprite = __class__ ('Sprite', [Attribute], {
			get __init__ () {return __get__ (this, function (self, game, width, height) {
				self.width = width;
				self.height = height;
				Attribute.__init__ (self, game);
			}, '__init__');},
			get install () {return __get__ (this, function (self) {
				self.image = new fabric.Rect (dict ({'width': self.game.scaleX (self.width), 'height': self.game.scaleY (self.height), 'originX': 'center', 'originY': 'center', 'fill': 'white'}));
			}, 'install');},
			get reset () {return __get__ (this, function (self, vX, vY, x, y) {
				if (typeof vX == 'undefined' || (vX != null && vX .__class__ == __kwargdict__)) {;
					var vX = 0;
				};
				if (typeof vY == 'undefined' || (vY != null && vY .__class__ == __kwargdict__)) {;
					var vY = 0;
				};
				if (typeof x == 'undefined' || (x != null && x .__class__ == __kwargdict__)) {;
					var x = 0;
				};
				if (typeof y == 'undefined' || (y != null && y .__class__ == __kwargdict__)) {;
					var y = 0;
				};
				if (arguments.length) {
					var __ilastarg0__ = arguments.length - 1;
					if (arguments [__ilastarg0__] && arguments [__ilastarg0__].__class__ == __kwargdict__) {
						var __allkwargs0__ = arguments [__ilastarg0__--];
						for (var __attrib0__ in __allkwargs0__) {
							switch (__attrib0__) {
								case 'self': var self = __allkwargs0__ [__attrib0__]; break;
								case 'vX': var vX = __allkwargs0__ [__attrib0__]; break;
								case 'vY': var vY = __allkwargs0__ [__attrib0__]; break;
								case 'x': var x = __allkwargs0__ [__attrib0__]; break;
								case 'y': var y = __allkwargs0__ [__attrib0__]; break;
							}
						}
					}
				}
				self.vX = vX;
				self.vY = vY;
				self.x = x;
				self.y = y;
				Attribute.reset (self);
			}, 'reset');},
			get predict () {return __get__ (this, function (self) {
				self.x += self.vX * self.game.deltaT;
				self.y += self.vY * self.game.deltaT;
			}, 'predict');},
			get commit () {return __get__ (this, function (self) {
				self.image.left = self.game.orthoX (self.x);
				self.image.top = self.game.orthoY (self.y);
			}, 'commit');},
			get draw () {return __get__ (this, function (self) {
				self.game.canvas.add (self.image);
			}, 'draw');}
		});
		var Paddle = __class__ ('Paddle', [Sprite], {
			get __init__ () {return __get__ (this, function (self, game, index) {
				self.index = index;
				Sprite.__init__ (self, game, self.width, self.height);
			}, '__init__');},
			get reset () {return __get__ (this, function (self) {
				Sprite.reset (self, __kwargdict__ ({x: (self.index ? Math.floor (orthoWidth / 2) - self.margin : Math.floor (-(orthoWidth) / 2) + self.margin), y: 0}));
			}, 'reset');},
			get predict () {return __get__ (this, function (self) {
				self.vY = 0;
				if (self.index) {
					if (self.game.keyCode == ord ('K')) {
						self.vY = self.speed;
					}
					else {
						if (self.game.keyCode == ord ('M')) {
							self.vY = -(self.speed);
						}
					}
				}
				else {
					if (self.game.keyCode == ord ('A')) {
						self.vY = self.speed;
					}
					else {
						if (self.game.keyCode == ord ('Z')) {
							self.vY = -(self.speed);
						}
					}
				}
				Sprite.predict (self);
			}, 'predict');},
			get interact () {return __get__ (this, function (self) {
				self.y = Math.max (Math.floor (self.height / 2) - Math.floor (fieldHeight / 2), Math.min (self.y, Math.floor (fieldHeight / 2) - Math.floor (self.height / 2)));
				if ((self.y - Math.floor (self.height / 2) < self.game.ball.y && self.game.ball.y < self.y + Math.floor (self.height / 2)) && (self.index == 0 && self.game.ball.x < self.x || self.index == 1 && self.game.ball.x > self.x)) {
					self.game.ball.x = self.x;
					self.game.ball.vX = -(self.game.ball.vX);
					self.game.ball.speedUp (self);
				}
			}, 'interact');}
		});
		Paddle.margin = 30;
		Paddle.width = 10;
		Paddle.height = 100;
		Paddle.speed = 400;
		var Ball = __class__ ('Ball', [Sprite], {
			get __init__ () {return __get__ (this, function (self, game) {
				Sprite.__init__ (self, game, self.side, self.side);
			}, '__init__');},
			get reset () {return __get__ (this, function (self) {
				var angle = self.game.serviceIndex * Math.PI + ((Math.random () > 0.5 ? 1 : -(1)) * Math.random ()) * Math.atan (fieldHeight / orthoWidth);
				Sprite.reset (self, __kwargdict__ ({vX: self.speed * Math.cos (angle), vY: self.speed * Math.sin (angle)}));
			}, 'reset');},
			get predict () {return __get__ (this, function (self) {
				Sprite.predict (self);
				if (self.x < Math.floor (-(orthoWidth) / 2)) {
					self.game.scored (1);
				}
				else {
					if (self.x > Math.floor (orthoWidth / 2)) {
						self.game.scored (0);
					}
				}
				if (self.y > Math.floor (fieldHeight / 2)) {
					self.y = Math.floor (fieldHeight / 2);
					self.vY = -(self.vY);
				}
				else {
					if (self.y < Math.floor (-(fieldHeight) / 2)) {
						self.y = Math.floor (-(fieldHeight) / 2);
						self.vY = -(self.vY);
					}
				}
			}, 'predict');},
			get speedUp () {return __get__ (this, function (self, bat) {
				var factor = 1 + 0.15 * Math.pow (1 - Math.abs (self.y - bat.y) / (Math.floor (bat.height / 2)), 2);
				if (Math.abs (self.vX) < 3 * self.speed) {
					self.vX *= factor;
					self.vY *= factor;
				}
			}, 'speedUp');}
		});
		Ball.side = 8;
		Ball.speed = 300;
		var Scoreboard = __class__ ('Scoreboard', [Attribute], {
			get install () {return __get__ (this, function (self) {
				self.playerLabels = function () {
					var __accu0__ = [];
					var __iter0__ = tuple ([tuple (['AZ keys:', -(7) / 16]), tuple (['KM keys:', 1 / 16])]);
					for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
						var __left0__ = __iter0__ [__index0__];
						var py_name = __left0__ [0];
						var position = __left0__ [1];
						__accu0__.append (new fabric.Text ('Player {}'.format (py_name), dict ({'fill': 'white', 'fontFamily': 'arial', 'fontSize': '{}'.format (self.game.canvas.width / 30), 'left': self.game.orthoX (position * orthoWidth), 'top': self.game.orthoY (Math.floor (fieldHeight / 2) + self.nameShift)})));
					}
					return __accu0__;
				} ();
				self.hintLabel = new fabric.Text ('[spacebar] starts game, [enter] resets score', dict ({'fill': 'white', 'fontFamily': 'arial', 'fontSize': '{}'.format (self.game.canvas.width / 70), 'left': self.game.orthoX ((-(7) / 16) * orthoWidth), 'top': self.game.orthoY (Math.floor (fieldHeight / 2) + self.hintShift)}));
				self.image = new fabric.Line (list ([self.game.orthoX (Math.floor (-(orthoWidth) / 2)), self.game.orthoY (Math.floor (fieldHeight / 2)), self.game.orthoX (Math.floor (orthoWidth / 2)), self.game.orthoY (Math.floor (fieldHeight / 2))]), dict ({'stroke': 'white'}));
			}, 'install');},
			get increment () {return __get__ (this, function (self, playerIndex) {
				self.scores [playerIndex]++;
			}, 'increment');},
			get reset () {return __get__ (this, function (self) {
				self.scores = list ([0, 0]);
				Attribute.reset (self);
			}, 'reset');},
			get commit () {return __get__ (this, function (self) {
				self.scoreLabels = function () {
					var __accu0__ = [];
					var __iter0__ = zip (self.scores, tuple ([-(2) / 16, 6 / 16]));
					for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
						var __left0__ = __iter0__ [__index0__];
						var score = __left0__ [0];
						var position = __left0__ [1];
						__accu0__.append (new fabric.Text ('{}'.format (score), dict ({'fill': 'white', 'fontFamily': 'arial', 'fontSize': '{}'.format (self.game.canvas.width / 30), 'left': self.game.orthoX (position * orthoWidth), 'top': self.game.orthoY (Math.floor (fieldHeight / 2) + self.nameShift)})));
					}
					return __accu0__;
				} ();
			}, 'commit');},
			get draw () {return __get__ (this, function (self) {
				var __iter0__ = zip (self.playerLabels, self.scoreLabels);
				for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
					var __left0__ = __iter0__ [__index0__];
					var playerLabel = __left0__ [0];
					var scoreLabel = __left0__ [1];
					self.game.canvas.add (playerLabel);
					self.game.canvas.add (scoreLabel);
					self.game.canvas.add (self.hintLabel);
				}
				self.game.canvas.add (self.image);
			}, 'draw');}
		});
		Scoreboard.nameShift = 75;
		Scoreboard.hintShift = 25;
		var Game = __class__ ('Game', [object], {
			get __init__ () {return __get__ (this, function (self) {
				self.serviceIndex = (Math.random () > 0.5 ? 1 : 0);
				self.pause = true;
				self.keyCode = null;
				self.textFrame = document.getElementById ('text_frame');
				self.canvasFrame = document.getElementById ('canvas_frame');
				self.buttonsFrame = document.getElementById ('buttons_frame');
				self.canvas = new fabric.Canvas ('canvas', dict ({'backgroundColor': 'black', 'originX': 'center', 'originY': 'center'}));
				self.canvas.onWindowDraw = self.draw;
				self.canvas.lineWidth = 2;
				self.canvas.clear ();
				self.attributes = list ([]);
				self.paddles = function () {
					var __accu0__ = [];
					for (var index = 0; index < 2; index++) {
						__accu0__.append (Paddle (self, index));
					}
					return __accu0__;
				} ();
				self.ball = Ball (self);
				self.scoreboard = Scoreboard (self);
				window.setInterval (self.update, 10);
				window.setInterval (self.draw, 20);
				window.addEventListener ('keydown', self.keydown);
				window.addEventListener ('keyup', self.keyup);
				self.buttons = list ([]);
				var __iter0__ = tuple (['A', 'Z', 'K', 'M', 'space', 'enter']);
				for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
					var key = __iter0__ [__index0__];
					var button = document.getElementById (key);
					button.addEventListener ('mousedown', (function __lambda__ (aKey) {
						return (function __lambda__ () {
							return self.mouseOrTouch (aKey, true);});}) (key));
					button.addEventListener ('touchstart', (function __lambda__ (aKey) {
						return (function __lambda__ () {
							return self.mouseOrTouch (aKey, true);});}) (key));
					button.addEventListener ('mouseup', (function __lambda__ (aKey) {
						return (function __lambda__ () {
							return self.mouseOrTouch (aKey, false);});}) (key));
					button.addEventListener ('touchend', (function __lambda__ (aKey) {
						return (function __lambda__ () {
							return self.mouseOrTouch (aKey, false);});}) (key));
					button.style.cursor = 'pointer';
					button.style.userSelect = 'none';
					self.buttons.append (button);
				}
				self.time = +(new Date);
				window.onresize = self.resize;
				self.resize ();
			}, '__init__');},
			get install () {return __get__ (this, function (self) {
				var __iter0__ = self.attributes;
				for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
					var attribute = __iter0__ [__index0__];
					attribute.install ();
				}
			}, 'install');},
			get mouseOrTouch () {return __get__ (this, function (self, key, down) {
				if (down) {
					if (key == 'space') {
						self.keyCode = space;
					}
					else {
						if (key == 'enter') {
							self.keyCode = enter;
						}
						else {
							self.keyCode = ord (key);
						}
					}
				}
				else {
					self.keyCode = null;
				}
			}, 'mouseOrTouch');},
			get update () {return __get__ (this, function (self) {
				var oldTime = self.time;
				self.time = +(new Date);
				self.deltaT = (self.time - oldTime) / 1000.0;
				if (self.pause) {
					if (self.keyCode == space) {
						self.pause = false;
					}
					else {
						if (self.keyCode == enter) {
							self.scoreboard.reset ();
						}
					}
				}
				else {
					var __iter0__ = self.attributes;
					for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
						var attribute = __iter0__ [__index0__];
						attribute.predict ();
					}
					var __iter0__ = self.attributes;
					for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
						var attribute = __iter0__ [__index0__];
						attribute.interact ();
					}
					var __iter0__ = self.attributes;
					for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
						var attribute = __iter0__ [__index0__];
						attribute.commit ();
					}
				}
			}, 'update');},
			get scored () {return __get__ (this, function (self, playerIndex) {
				self.scoreboard.increment (playerIndex);
				self.serviceIndex = 1 - playerIndex;
				var __iter0__ = self.paddles;
				for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
					var paddle = __iter0__ [__index0__];
					paddle.reset ();
				}
				self.ball.reset ();
				self.pause = true;
			}, 'scored');},
			get commit () {return __get__ (this, function (self) {
				var __iter0__ = self.attributes;
				for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
					var attribute = __iter0__ [__index0__];
					attribute.commit ();
				}
			}, 'commit');},
			get draw () {return __get__ (this, function (self) {
				self.canvas.clear ();
				var __iter0__ = self.attributes;
				for (var __index0__ = 0; __index0__ < __iter0__.length; __index0__++) {
					var attribute = __iter0__ [__index0__];
					attribute.draw ();
				}
			}, 'draw');},
			get resize () {return __get__ (this, function (self) {
				self.pageWidth = window.innerWidth;
				self.pageHeight = window.innerHeight;
				self.textTop = 0;
				if (self.pageHeight > 1.2 * self.pageWidth) {
					self.canvasWidth = self.pageWidth;
					self.canvasTop = self.textTop + 300;
				}
				else {
					self.canvasWidth = 0.6 * self.pageWidth;
					self.canvasTop = self.textTop + 200;
				}
				self.canvasLeft = 0.5 * (self.pageWidth - self.canvasWidth);
				self.canvasHeight = 0.6 * self.canvasWidth;
				self.buttonsTop = (self.canvasTop + self.canvasHeight) + 50;
				self.buttonsWidth = 500;
				self.textFrame.style.top = self.textTop;
				self.textFrame.style.left = self.canvasLeft + 0.05 * self.canvasWidth;
				self.textFrame.style.width = 0.9 * self.canvasWidth;
				self.canvasFrame.style.top = self.canvasTop;
				self.canvasFrame.style.left = self.canvasLeft;
				self.canvas.setDimensions (dict ({'width': self.canvasWidth, 'height': self.canvasHeight}));
				self.buttonsFrame.style.top = self.buttonsTop;
				self.buttonsFrame.style.left = 0.5 * (self.pageWidth - self.buttonsWidth);
				self.buttonsFrame.style.width = self.canvasWidth;
				self.install ();
				self.commit ();
				self.draw ();
			}, 'resize');},
			get scaleX () {return __get__ (this, function (self, x) {
				return x * (self.canvas.width / orthoWidth);
			}, 'scaleX');},
			get scaleY () {return __get__ (this, function (self, y) {
				return y * (self.canvas.height / orthoHeight);
			}, 'scaleY');},
			get orthoX () {return __get__ (this, function (self, x) {
				return self.scaleX (x + Math.floor (orthoWidth / 2));
			}, 'orthoX');},
			get orthoY () {return __get__ (this, function (self, y) {
				return self.scaleY ((orthoHeight - Math.floor (fieldHeight / 2)) - y);
			}, 'orthoY');},
			get keydown () {return __get__ (this, function (self, event) {
				self.keyCode = event.keyCode;
			}, 'keydown');},
			get keyup () {return __get__ (this, function (self, event) {
				self.keyCode = null;
			}, 'keyup');}
		});
		var game = Game ();
		__pragma__ ('<use>' +
			'com.fabricjs' +
		'</use>')
		__pragma__ ('<all>')
			__all__.Attribute = Attribute;
			__all__.Ball = Ball;
			__all__.Game = Game;
			__all__.Paddle = Paddle;
			__all__.Scoreboard = Scoreboard;
			__all__.Sprite = Sprite;
			__all__.enter = enter;
			__all__.esc = esc;
			__all__.fieldHeight = fieldHeight;
			__all__.game = game;
			__all__.orthoHeight = orthoHeight;
			__all__.orthoWidth = orthoWidth;
			__all__.space = space;
		__pragma__ ('</all>')
	}) ();
