(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
require("../third_party/jquery.mobile.vmouse.js"),$.extend(KhanUtil,{initUnitCircle:function(a){var e=KhanUtil.currentGraph,t={xpixels:514,ypixels:514,range:[[-1.2,1.2],[-1.2,1.2]]};t.scale=[t.xpixels/(t.range[0][1]-t.range[0][0]),t.ypixels/(t.range[1][1]-t.range[1][0])],e.init(t),e.xpixels=t.xpixels,e.ypixels=t.ypixels,e.range=t.range,e.scale=t.scale,e.angle=0,e.revolutions=0,e.quadrant=1,e.dragging=!1,e.highlight=!1,e.degrees=a,e.style({stroke:"#ddd",strokeWidth:1,arrows:"->"},function(){e.circle([0,0],1),e.line([-1.2,0],[1.2,0]),e.line([0,-1.2],[0,1.2]),e.line([1.2,0],[-1.2,0]),e.line([0,1.2],[0,-1.2])}),e.style({strokeWidth:2},function(){e.line([-1,-5/e.scale[0]],[-1,5/e.scale[0]]),e.line([1,-5/e.scale[0]],[1,5/e.scale[0]]),e.line([-5/e.scale[0],-1],[5/e.scale[0],-1]),e.line([-5/e.scale[0],1],[5/e.scale[0],1])}),e.triangle=KhanUtil.bogusShape,e.rightangle=KhanUtil.bogusShape,e.spiral=KhanUtil.bogusShape,e.arrow=KhanUtil.bogusShape,e.cosLabel=KhanUtil.bogusShape,e.sinLabel=KhanUtil.bogusShape,e.radiusLabel=KhanUtil.bogusShape,e.angleLabel=KhanUtil.bogusShape,e.angleLines=KhanUtil.bogusShape,KhanUtil.initMouseHandlers(),KhanUtil.setAngle(e.angle)},bogusShape:{animate:function(){},attr:function(){},remove:function(){}},initMouseHandlers:function(){var a=KhanUtil.currentGraph;a.mouselayer=Raphael("unitcircle",a.xpixels,a.ypixels),$(a.mouselayer.canvas).css("z-index",1),Khan.scratchpad.disable(),a.style({stroke:KhanUtil.ORANGE,fill:KhanUtil.ORANGE},function(){a.dragPoint=a.circle([1,0],4/a.scale[0])}),a.mouseTarget=a.mouselayer.circle((1-a.range[0][0])*a.scale[0],(a.range[1][1]-0)*a.scale[1],15),a.mouseTarget.attr({fill:"#000",opacity:0}),$(a.mouseTarget[0]).css("cursor","move"),$(a.mouseTarget[0]).bind("vmousedown vmouseover vmouseout",function(a){var e=KhanUtil.currentGraph;"vmouseover"===a.type?(e.highlight=!0,e.dragging||KhanUtil.highlightAngle()):"vmouseout"===a.type?(e.highlight=!1,e.dragging||KhanUtil.unhighlightAngle()):"vmousedown"!==a.type||1!==a.which&&0!==a.which||(a.preventDefault(),$(document).bind("vmousemove vmouseup",function(a){a.preventDefault(),e.dragging=!0;var t=a.pageY-$("#unitcircle").offset().top,l=a.pageX-$("#unitcircle").offset().left,n=l/e.scale[0]+e.range[0][0],i=e.range[1][1]-t/e.scale[1];if("vmousemove"===a.type){var r;r=n?Math.atan(i/n):i>0?-Math.PI/2:-Math.PI/2,r=Math.round(r/(Math.PI/36))*(Math.PI/36),n>0&&i>=0?(4===e.quadrant&&++e.revolutions,e.quadrant=1):0>=n&&i>0?(r+=Math.PI,e.quadrant=2):0>n&&0>=i?(r+=Math.PI,e.quadrant=3):n>=0&&0>i&&(r+=2*Math.PI,1===e.quadrant&&--e.revolutions,e.quadrant=4),e.revolutions<=-3?(e.revolutions=-3,r=2*Math.PI):e.revolutions>=2&&(e.revolutions=2,r=0),e.angle!==r+2*e.revolutions*Math.PI&&KhanUtil.setAngle(r+2*e.revolutions*Math.PI)}else"vmouseup"===a.type&&($(document).unbind("vmousemove vmouseup"),e.dragging=!1,e.highlight||KhanUtil.unhighlightAngle())}))})},highlightAngle:function(){var a=KhanUtil.currentGraph;a.dragPoint.animate({scale:2},50),a.angleLines.animate({stroke:KhanUtil.ORANGE},100),a.spiral.animate({stroke:KhanUtil.ORANGE},100),a.arrow.animate({fill:KhanUtil.ORANGE},100),$(a.angleLabel).animate({color:KhanUtil.ORANGE},100)},unhighlightAngle:function(){var a=KhanUtil.currentGraph;a.dragPoint.animate({scale:1},50),a.angleLines.animate({stroke:KhanUtil.BLUE},100),a.spiral.animate({stroke:KhanUtil.BLUE},100),a.arrow.animate({fill:KhanUtil.BLUE},100),$(a.angleLabel).animate({color:KhanUtil.BLUE},100)},setAngle:function(a){var e=KhanUtil.currentGraph;e.angle=a,e.quadrant=Math.floor((a+10*Math.PI)/(Math.PI/2))%4+1,e.revolutions=Math.floor(a/(2*Math.PI)),e.triangle.remove(),e.rightangle.remove(),e.spiral.remove(),e.arrow.remove(),e.cosLabel.remove(),e.sinLabel.remove(),e.radiusLabel.remove(),e.angleLabel.remove(),e.angleLines.remove();var t=KhanUtil.BLUE;(e.dragging||e.highlight)&&(t=KhanUtil.ORANGE),e.style({stroke:t,strokeWidth:3}),e.angleLines=e.path([[1,0],[0,0],[Math.cos(a),Math.sin(a)]]),e.style({stroke:KhanUtil.BLUE,strokeWidth:1}),e.triangle=e.path([[0,0],[Math.cos(a),0],[Math.cos(a),Math.sin(a)],[0,0]]);var l=KhanUtil.roundTo(3,Math.cos(a)),n=KhanUtil.roundTo(3,Math.sin(a)),i={.866:"\\frac{\\sqrt{3}}{2}\\;(0.866)","-0.866":"-\\frac{\\sqrt{3}}{2}\\;(-0.866)",.707:"\\frac{\\sqrt{2}}{2}\\;(0.707)","-0.707":"-\\frac{\\sqrt{2}}{2}\\;(-0.707)",.5:"\\frac{1}{2}\\;(0.5)","-0.5":"-\\frac{1}{2}\\;(-0.5)"};l=i[l]?i[l]:l,n=i[n]?i[n]:n,a%Math.PI===0?e.cosLabel=e.label([Math.cos(a)/2,0],l,"below"):a%(Math.PI/2)===0?e.sinLabel=e.label([Math.cos(a),Math.sin(a)/2],n,"right"):1===e.quadrant?(e.cosLabel=e.label([Math.cos(a)/2,0],l,"below"),e.sinLabel=e.label([Math.cos(a),Math.sin(a)/2],n,"right"),e.radiusLabel=e.label([Math.cos(a)/2,Math.sin(a)/2],1,"above left"),e.rightangle=e.path([[Math.cos(a)-.04,0],[Math.cos(a)-.04,.04],[Math.cos(a),.04]])):2===e.quadrant?(e.cosLabel=e.label([Math.cos(a)/2,0],l,"below"),e.sinLabel=e.label([Math.cos(a),Math.sin(a)/2],n,"left"),e.radiusLabel=e.label([Math.cos(a)/2,Math.sin(a)/2],1,"above right"),e.rightangle=e.path([[Math.cos(a)+.04,0],[Math.cos(a)+.04,.04],[Math.cos(a),.04]])):3===e.quadrant?(e.cosLabel=e.label([Math.cos(a)/2,0],l,"above"),e.sinLabel=e.label([Math.cos(a),Math.sin(a)/2],n,"left"),e.radiusLabel=e.label([Math.cos(a)/2,Math.sin(a)/2],1,"below right"),e.rightangle=e.path([[Math.cos(a)+.04,0],[Math.cos(a)+.04,-.04],[Math.cos(a),-.04]])):4===e.quadrant&&(e.cosLabel=e.label([Math.cos(a)/2,0],l,"above"),e.sinLabel=e.label([Math.cos(a),Math.sin(a)/2],n,"right"),e.radiusLabel=e.label([Math.cos(a)/2,Math.sin(a)/2],1,"below left"),e.rightangle=e.path([[Math.cos(a)-.04,0],[Math.cos(a)-.04,-.04],[Math.cos(a),-.04]]));for(var r=[],s=0;50>=s;++s)r.push([Math.cos(s*a/50)*(.1+s*Math.abs(a)/50/Math.PI*.02),Math.sin(s*a/50)*(.1+s*Math.abs(a)/50/Math.PI*.02)]);e.style({strokeWidth:2,stroke:t}),e.spiral=e.path(r);var o=r[50][0],h=r[50][1];e.style({stroke:!1,fill:t},function(){a>Math.PI/12?(e.arrow=e.path([[o,h-.005],[o-.02,h-.03],[o+.02,h-.03],[o,h-.005]]),e.arrow.rotate((a-Math.PI/20)*(-180/Math.PI),(o-e.range[0][0])*e.scale[0],(e.range[1][1]-h)*e.scale[1])):a<-Math.PI/12?(e.arrow=e.path([[o,h+.005],[o-.02,h+.03],[o+.02,h+.03],[o,h+.005]]),e.arrow.rotate((a+Math.PI/20)*(-180/Math.PI),(o-e.range[0][0])*e.scale[0],(e.range[1][1]-h)*e.scale[1])):e.arrow=KhanUtil.bogusShape});var c=a;e.degrees?(c*=180/Math.PI,c=Math.round(c),c+="^{\\circ}"):a>-15&&15>a&&0!==a&&(c=KhanUtil.piFraction(a)),a<-3.5*Math.PI?e.angleLabel=e.label([-.2,.2],c,"center"):a<-.15*Math.PI?e.angleLabel=e.label([Math.cos(a/2)/5,Math.sin(a/2)/5],c,"center"):a<.15*Math.PI?e.angleLabel=e.label([0,0],c,"left"):a<3.5*Math.PI?e.angleLabel=e.label([Math.cos(a/2)/5,Math.sin(a/2)/5],c,"center"):e.angleLabel=e.label([-.2,-.2],c,"center"),$(e.angleLabel).css("color",t),e.mouseTarget.attr("cx",(Math.cos(a)-e.range[0][0])*e.scale[0]),e.mouseTarget.attr("cy",(e.range[1][1]-Math.sin(a))*e.scale[1]),e.dragPoint.attr("cx",(Math.cos(a)-e.range[0][0])*e.scale[0]),e.dragPoint.attr("cy",(e.range[1][1]-Math.sin(a))*e.scale[1]),e.angleLines.toFront(),e.dragPoint.toFront()},goToAngle:function(a){var e=KhanUtil.currentGraph;e.degrees&&(a*=Math.PI/180);var t=1e3*Math.abs(a-e.angle)/Math.PI;$(e).animate({angle:a},{duration:t,easing:"linear",step:function(a,e){KhanUtil.setAngle(a)}})},showCoordinates:function(a,e){var t=KhanUtil.currentGraph;t.degrees&&(a*=Math.PI/180),t.style({stroke:0,fill:KhanUtil.BLUE},function(){t.circle([Math.cos(a),Math.sin(a)],4/t.scale[0])}),t.dragPoint.toFront();var l=KhanUtil.roundTo(3,Math.cos(a)),n=KhanUtil.roundTo(3,Math.sin(a));"x"===e&&(l="\\pink{"+l+"}"),"y"===e&&(n="\\pink{"+n+"}");var i="("+l+", "+n+")";Math.floor(a/Math.PI)%2?t.coordLabel=t.label([Math.cos(a),Math.sin(a)],i,"below"):t.coordLabel=t.label([Math.cos(a),Math.sin(a)],i,"above")}});
},{"../third_party/jquery.mobile.vmouse.js":2}],2:[function(require,module,exports){
!function(t,e,n,o){function a(t){for(;t&&"undefined"!=typeof t.originalEvent;)t=t.originalEvent;return t}function i(e,n){var i,r,u,s,c,h,v,d,l=e.type;if(e=t.Event(e),e.type=n,i=e.originalEvent,r=t.event.props,l.search(/mouse/)>-1&&(r=I),i)for(v=r.length,s;v;)s=r[--v],e[s]=i[s];if(l.search(/mouse(down|up)|click/)>-1&&!e.which&&(e.which=1),-1!==l.search(/^touch/)&&(u=a(i),l=u.touches,c=u.changedTouches,h=l&&l.length?l[0]:c&&c.length?c[0]:o))for(d=0,len=Y.length;d<len;d++)s=Y[d],e[s]=h[s];return e}function r(e){for(var n,o,a={};e;){n=t.data(e,y);for(o in n)n[o]&&(a[o]=a.hasVirtualBinding=!0);e=e.parentNode}return a}function u(e,n){for(var o;e;){if(o=t.data(e,y),o&&(!n||o[n]))return e;e=e.parentNode}return null}function s(){V=!1}function c(){V=!0}function h(){z=0,L.length=0,S=!1,c()}function v(){s()}function d(){l(),B=setTimeout(function(){B=0,h()},t.vmouse.resetTimerDuration)}function l(){B&&(clearTimeout(B),B=0)}function f(e,n,o){var a;return(o&&o[e]||!o&&u(n.target,e))&&(a=i(n,e),t(n.target).trigger(a)),a}function p(e){var n=t.data(e.target,P);if(!(S||z&&z===n)){var o=f("v"+e.type,e);o&&(o.isDefaultPrevented()&&e.preventDefault(),o.isPropagationStopped()&&e.stopPropagation(),o.isImmediatePropagationStopped()&&e.stopImmediatePropagation())}}function g(e){var n,o,i=a(e).touches;if(i&&1===i.length&&(n=e.target,o=r(n),o.hasVirtualBinding)){z=q++,t.data(n,P,z),l(),v(),H=!1;var u=a(e).touches[0];N=u.pageX,x=u.pageY,f("vmouseover",e,o),f("vmousedown",e,o)}}function m(t){V||(H||f("vmousecancel",t,r(t.target)),H=!0,d())}function b(e){if(!V){var n=a(e).touches[0],o=H,i=t.vmouse.moveDistanceThreshold;H=H||Math.abs(n.pageX-N)>i||Math.abs(n.pageY-x)>i,flags=r(e.target),H&&!o&&f("vmousecancel",e,flags),f("vmousemove",e,flags),d()}}function D(t){if(!V){c();var e,n=r(t.target);if(f("vmouseup",t,n),!H){var o=f("vclick",t,n);o&&o.isDefaultPrevented()&&(e=a(t).changedTouches[0],L.push({touchID:z,x:e.clientX,y:e.clientY}),S=!0)}f("vmouseout",t,n),H=!1,d()}}function T(e){var n,o=t.data(e,y);if(o)for(n in o)if(o[n])return!0;return!1}function k(){}function w(e){var n=e.substr(1);return{setup:function(o,a){T(this)||t.data(this,y,{});var i=t.data(this,y);i[e]=!0,M[e]=(M[e]||0)+1,1===M[e]&&Q.bind(n,p),t(this).bind(n,k),j&&(M.touchstart=(M.touchstart||0)+1,1===M.touchstart&&Q.bind("touchstart",g).bind("touchend",D).bind("touchmove",b).bind("scroll",m))},teardown:function(o,a){--M[e],M[e]||Q.unbind(n,p),j&&(--M.touchstart,M.touchstart||Q.unbind("touchstart",g).unbind("touchmove",b).unbind("touchend",D).unbind("scroll",m));var i=t(this),r=t.data(this,y);r&&(r[e]=!1),i.unbind(n,k),T(this)||i.removeData(y)}}}var y="virtualMouseBindings",P="virtualTouchID",X="vmouseover vmousedown vmousemove vmouseup vclick vmouseout vmousecancel".split(" "),Y="clientX clientY pageX pageY screenX screenY".split(" "),E=t.event.mouseHooks?t.event.mouseHooks.props:[],I=t.event.props.concat(E),M={},B=0,N=0,x=0,H=!1,L=[],S=!1,V=!1,j="addEventListener"in n,Q=t(n),q=1,z=0;t.vmouse={moveDistanceThreshold:10,clickDistanceThreshold:10,resetTimerDuration:1500};for(var A=0;A<X.length;A++)t.event.special[X[A]]=w(X[A]);j&&n.addEventListener("click",function(e){var n,o,a,i,r,u,s=L.length,c=e.target;if(s)for(n=e.clientX,o=e.clientY,threshold=t.vmouse.clickDistanceThreshold,a=c;a;){for(i=0;s>i;i++)if(r=L[i],u=0,a===c&&Math.abs(r.x-n)<threshold&&Math.abs(r.y-o)<threshold||t.data(a,P)===r.touchID)return e.preventDefault(),void e.stopPropagation();a=a.parentNode}},!0)}(jQuery,window,document);
},{}]},{},[1]);
