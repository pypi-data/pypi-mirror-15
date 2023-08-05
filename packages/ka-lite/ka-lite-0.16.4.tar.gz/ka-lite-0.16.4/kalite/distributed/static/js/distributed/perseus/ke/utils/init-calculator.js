(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
Calculator.init=function(){var e,t=["+","-","/","*","^"," "],n=$(".calculator"),a=n.children(".history"),o=$("#calc-output-content"),l=a.children(".calc-row.input"),c=l.children("input"),i=n.find("a"),r=[],s=-1,u=0,d=!1,f=icu.getDecimalFormatSymbols().decimal_separator,v=function(e){return e.replace(/pi/g,"π")+" ="},h=function(e){o.append(e),o.scrollTop(o[0].scrollHeight)},g=function(){var t;void 0!==e&&(t=$("<div>").addClass("output").text(e),e=void 0,h(t))},p=function(){var t,n,a,o=c.val(),l=!1,i=o;if(""!==$.trim(o)){r.unshift(o),t=$("<div>").addClass("input-history").text(v(o));try{"."!==f&&(o=o.split(f).join(".")),n=u=Calculator.calculate(o,u),"number"==typeof n?(a=Math.round(1e9*n)/1e9,"."!==f&&(a=(""+a).replace(".",f))):a=n,i=a}catch(p){if(p instanceof Calculator.CalculatorError)return a=p.message,i=o,l=!0,d=!1,void c.css({backgroundColor:"#ffcccc"});throw p}g(),h(t),e=a,l&&g()}d=!0,s=-1,c.val(i)},m=function(e){return"<span class='selected-anglemode'>"+e+"</span>"},w=function(e){return"<span class='unselected-anglemode'>"+e+"</span>"},C=function(){var e=i18n._("DEG"),t=i18n._("RAD");"DEG"===Calculator.settings.angleMode?$(".calculator-angle-mode").html(w(t)+"<br>"+m(e)):$(".calculator-angle-mode").html(m(t)+"<br>"+w(e))},y=8,b=37,D=39,k=38,x=40,E=[b,D];c.on("keydown",function(e){return _.contains(E,e.keyCode)&&(d=!1),e.which===y&&d?(c.val(""),g(),!1):e.which===k?(g(),s+=1,s>=r.length&&(s=r.length-1),c.val(r[s]),!1):e.which===x?(g(),s-=1,-1>s&&(s=-1),c.val(r[s]||u),!1):void 0});var A=function(e){var n=!_.contains(t,e)&&d;g(),d=!1,n&&c.val(""),c.css({backgroundColor:"white"})};a.on("click",function(e){c.focus()});var S=13,G=61;c.on("keypress",function(e){return e.which===S||e.which===G?(p(),!1):void A(String.fromCharCode(e.charCode))}),c.on("click",function(e){d=!1}),i.on("click",function(){var t=$(this),n=t.data("behavior");if(null!=n)if("bs"===n){var a=c.val();c.val(a.slice(0,a.length-1))}else if("clear"===n)c.val(""),u=void 0,e=void 0,r=[],s=-1,d=!1,o.empty();else if("angle-mode"===n){if(Calculator.settings.angleMode="DEG"===Calculator.settings.angleMode?"RAD":"DEG","undefined"!=typeof window.localStorage){var l=window.KA&&window.KA.getUserID&&window.KA.getUserID();window.localStorage["calculator_settings:"+l]=JSON.stringify(Calculator.settings)}C()}else"evaluate"===n&&p();else{var i=t.data("text")||t.text();A(i),c.val(c.val()+i)}return c.focus(),!1}),C(),"undefined"!=typeof Exercises&&$(Exercises).on("gotoNextProblem",function(){c.val(""),o.children().not(l).remove()}),$(".calculator-decimal").html(f)};
},{}]},{},[1]);
