(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
$.extend(KhanUtil,{expr:function(e,r){if("object"==typeof e){var t=e[0],n=e.slice(1),a=r?KhanUtil.computeOperators:KhanUtil.formatOperators;return a[t].apply(this,n)}return r?e:e.toString()},exprType:function(e){return"object"==typeof e?"color"===e[0]?KhanUtil.exprType(e[2]):e[0]:typeof e},exprIsNegated:function(e){switch(KhanUtil.exprType(e)){case"color":return KhanUtil.exprIsNegated(e[2]);case"/":return KhanUtil.exprIsNegated(e[1]);case"+":case"-":return!0;case"number":return 0>e;case"string":return"-"===e.charAt(0);default:return!1}},exprIsShort:function(e){switch(KhanUtil.exprType(e)){case"color":return KhanUtil.exprIsShort(e[2]);case"+":case"-":case"*":case"/":case"frac":return!1;case"^":return"number"!==KhanUtil.exprType(e[1])||e[1]<0;case"number":case"sqrt":return!0;default:return e.length<=1}},exprParenthesize:function(e){return KhanUtil.exprIsShort(e)?KhanUtil.expr(e):"("+KhanUtil.expr(e)+")"},formatOperators:{color:function(e,r){return"\\color{"+e+"}{"+KhanUtil.expr(r)+"}"},"+":function(){var e=[].slice.call(arguments,0),r=$.grep(e,function(e,r){return null!=e});r=_.filter(r,function(e){return""+KhanUtil.expr(e)!="0"}),r=$.map(r,function(e,r){var t;switch(KhanUtil.exprType(e)){case"+":t=!0;break;case"-":t=e.length>2;break;default:t=!1}return e=KhanUtil.expr(e),t&&(e="("+e+")"),("-"!==e.charAt(0)||t)&&(e="+"+e),e});var t=r.join("");return"+"===t.charAt(0)?t.slice(1):t},"-":function(){if(1===arguments.length)return KhanUtil.expr(["*",-1,arguments[0]]);var e=[].slice.call(arguments,0),r=$.map(e,function(e,r){var t,n=KhanUtil.exprIsNegated(e);switch(KhanUtil.exprType(e)){case"+":case"-":t=!0;break;default:t=!1}return e=KhanUtil.expr(e),(n&&r>0||t)&&(e="("+e+")"),e}),t=r.join("-");return t},"*":function(){var e=Array.prototype.slice.call(arguments,1);if(e.unshift("*"),0===arguments[0])return 0;if(1===arguments[0]&&e.length>1)return KhanUtil.expr(e);if(-1===arguments[0]&&e.length>1){var r=KhanUtil.expr(e);return KhanUtil.exprIsNegated(e[1])?"-("+r+")":"-"+r}if(arguments.length>1){var t=[].slice.call(arguments,0),n="number"===KhanUtil.exprType(arguments[0])&&"number"===KhanUtil.exprType(arguments[1]),a=$.map(t,function(e,r){var t;switch(KhanUtil.exprType(e)){case"number":r>0&&(t=!0);break;default:t=!KhanUtil.exprIsShort(e)}return n=n||t,e=KhanUtil.expr(e),n&&(e="("+e+")"),e});return a.join("")}return KhanUtil.expr(arguments[0])},times:function(e,r){var t=!KhanUtil.exprIsShort(e),n=!KhanUtil.exprIsShort(r);return e=KhanUtil.expr(e),r=KhanUtil.expr(r),e=t?"("+e+")":e,r=n?"("+r+")":r,e+" \\times "+r},dot:function(e,r){var t=!KhanUtil.exprIsShort(e),n=!KhanUtil.exprIsShort(r);return e=KhanUtil.expr(e),r=KhanUtil.expr(r),e=t?"("+e+")":e,r=n?"("+r+")":r,e+" \\cdot "+r},"/":function(e,r){var t=!KhanUtil.exprIsShort(e),n=!KhanUtil.exprIsShort(r);return e=KhanUtil.expr(e),r=KhanUtil.expr(r),e=t?"("+e+")":e,r=n?"("+r+")":r,e+"/"+r},frac:function(e,r){return"\\dfrac{"+KhanUtil.expr(e)+"}{"+KhanUtil.expr(r)+"}"},"^":function(e,r){if(0===r)return"";if(1===r)return KhanUtil.expr(e);var t,n;switch(KhanUtil.exprType(e)){case"+":case"-":case"*":case"/":case"^":case"ln":t=!0;break;case"number":t=0>e;break;case"sin":case"cos":case"tan":case"csc":case"sec":case"cot":t=!1,n=!0;break;default:t=!1,n=!1}return e=KhanUtil.expr(e),t&&(e="("+e+")"),r=KhanUtil.expr(r),n?e.replace(/\\(\S+?)\{/,function(e,t){return"\\"+t+"^{"+r+"} {"}):e+"^{"+r+"}"},sqrt:function(e){return"\\sqrt{"+KhanUtil.exprParenthesize(e)+"}"},sin:function(e){return"\\sin{"+KhanUtil.exprParenthesize(e)+"}"},cos:function(e){return"\\cos{"+KhanUtil.exprParenthesize(e)+"}"},tan:function(e){return"\\tan{"+KhanUtil.exprParenthesize(e)+"}"},sec:function(e){return"\\sec{"+KhanUtil.exprParenthesize(e)+"}"},csc:function(e){return"\\sec{"+KhanUtil.exprParenthesize(e)+"}"},cot:function(e){return"\\sec{"+KhanUtil.exprParenthesize(e)+"}"},ln:function(e){return"\\ln{"+KhanUtil.exprParenthesize(e)+"}"},"+-":function(){if(1===arguments.length)return"\\pm "+KhanUtil.exprParenthesize(arguments[0]);var e=[].slice.call(arguments,0);return $.map(e,function(e,r){return KhanUtil.expr(e)}).join(" \\pm ")}},computeOperators:{color:function(e,r){return KhanUtil.expr(r,!0)},"+":function(){var e=[].slice.call(arguments,0),r=0;return $.each(e,function(e,t){r+=KhanUtil.expr(t,!0)}),r},"-":function(){if(1===arguments.length)return-KhanUtil.expr(arguments[0],!0);var e=[].slice.call(arguments,0),r=0;return $.each(e,function(e,t){r+=(0===e?1:-1)*KhanUtil.expr(t,!0)}),r},"*":function(){var e=[].slice.call(arguments,0),r=1;return $.each(e,function(e,t){r*=KhanUtil.expr(t,!0)}),r},"/":function(){var e=[].slice.call(arguments,0),r=1;return $.each(e,function(e,t){var n=KhanUtil.expr(t,!0);r*=0===e?n:1/n}),r},"^":function(e,r){return Math.pow(KhanUtil.expr(e,!0),KhanUtil.expr(r,!0))},sqrt:function(e){return Math.sqrt(KhanUtil.expr(e,!0))},"+-":function(){return NaN}},exprStripColor:function(e){return"object"!=typeof e?e:"color"===e[0]?KhanUtil.exprStripColor(e[2]):$.map(e,function(e,r){return[0===r?e:KhanUtil.exprStripColor(e)]})},exprSimplifyAssociative:function(e){if("object"!=typeof e)return e;var r=$.map(e.slice(1),function(e){return[KhanUtil.exprSimplifyAssociative(e)]}),t=function(r){switch(e[0]){case"+":if("+"===r[0])return r.slice(1);break;case"*":if("*"===r[0])return r.slice(1)}return[r]},n=$.map(r,t);return n.unshift(e[0]),n}}),KhanUtil.computeOperators.frac=KhanUtil.computeOperators["/"];
},{}],2:[function(require,module,exports){
require("./expressions.js");var kmatrix=KhanUtil.kmatrix={deepZipWith:function(r,t){var i=[].slice.call(arguments,2),n=_.any(i,function(r){return null===r?!0:void 0});return n?null:0===r?t.apply(null,i):_.map(_.zip.apply(_,i),function(i){return kmatrix.deepZipWith.apply(this,[r-1,t].concat(i))})},matrixCopy:function(r){return $.extend(!0,[],r)},matrixMap:function(r,t){return _.map(t,function(t,i){return _.map(t,function(t,n){return r(t,i,n)})})},maskMatrix:function(r,t){var i=[];return _.times(r.r,function(n){var a=[];_.times(r.c,function(i){KhanUtil.contains(t,[n+1,i+1])?a.push(r[n][i]):a.push("?")}),i.push(a)}),i},printMatrix:function(r){var t=Array.prototype.slice.call(arguments),i=kmatrix.deepZipWith.apply(this,[2].concat(t));if(!i)return null;var n=_.map(i,function(r,t){return r.join(" & ")}).join(" \\\\ "),a="\\left[\\begin{array}",e="\\end{array}\\right]",u="{",m=i[0].length;return _(m).times(function(){u+="r"}),u+="}",a+u+n+e},printSimpleMatrix:function(r,t){return kmatrix.printMatrix(function(r){return t?KhanUtil.colorMarkup(r,t):r},r)},printFractionMatrix:function(r,t){return kmatrix.printMatrix(function(r){return r=KhanUtil.decimalFraction(r,!0),t?KhanUtil.colorMarkup(r,t):r},r)},printSimpleMatrixDet:function(r,t){return kmatrix.printSimpleMatrix(r,t).replace("left[","left|").replace("right]","right|")},printColoredDimMatrix:function(r,t,i){var n=kmatrix.matrixMap(function(r,n,a){var e=t[i?n:a];return KhanUtil.colorMarkup(r,e)},r);return kmatrix.printSimpleMatrix(n)},makeMultHintMatrix:function(r,t,i,n){var a=[];return _.times(r.r,function(){a.push([])}),_.times(r.r,function(e){var u=i[e];_.times(t.c,function(i){var m=n[i],c="";_.times(r.c,function(n){n>0&&(c+="+");var a=KhanUtil.colorMarkup(r[e][n],u),o=KhanUtil.colorMarkup(t[n][i],m);c+=a+"\\cdot"+o}),a[e][i]=c})}),kmatrix.makeMatrix(a)},makeMatrix:function(r){return r.r=r.length,r.c=r[0].length,r},cropMatrix:function(r,t,i){var n=kmatrix.matrixCopy(r);return n.splice(t,1),_.each(n,function(r){r.splice(i,1)}),n},matrix2x2DetHint:function(r){var t="string"==typeof r[0][0]?" \\times ":" \\cdot ",i="("+r[0][0]+t+r[1][1]+")",n="("+r[0][1]+t+r[1][0]+")";return i+"-"+n},matrix3x3DetHint:function(r,t){var i="";return _.times(r.c,function(n){var a=kmatrix.cropMatrix(r,0,n),e=n%2?"-":"+";e=0===n?"":e;var u,m=r[0][n];t?u=kmatrix.printSimpleMatrixDet(a):(u=kmatrix.matrix2x2DetHint(a),u=KhanUtil.exprParenthesize(u)),i+=e+m+u}),i},matrixMult:function(r,t){r=kmatrix.makeMatrix(r),t=kmatrix.makeMatrix(t);var i=[];return _.times(r.r,function(){i.push([])}),_.times(r.r,function(n){_.times(t.c,function(a){var e=0;_.times(r.c,function(i){e+=r[n][i]*t[i][a]}),i[n][a]=e})}),kmatrix.makeMatrix(i)},matrixMinors:function(r){if(r=kmatrix.makeMatrix(r),!r.r||!r.c)return null;var t=kmatrix.matrixMap(function(t,i,n){return kmatrix.cropMatrix(r,i,n)},r);return t},matrixTranspose:function(r){r=kmatrix.makeMatrix(r);var t=r.c,i=r.r;if(!t||!i)return null;var n=[];return _.times(t,function(t){var a=[];_.times(i,function(i){a.push(r[i][t])}),n.push(a)}),kmatrix.makeMatrix(n)},matrixDet:function(r){if(r=kmatrix.makeMatrix(r),r.r!==r.c)return null;var t,i,n,a,e,u,m,c,o,x;return 2===r.r?(t=r[0][0],i=r[0][1],n=r[1][0],a=r[1][1],x=t*a-i*n):3===r.r&&(t=r[0][0],i=r[0][1],n=r[0][2],a=r[1][0],e=r[1][1],u=r[1][2],m=r[2][0],c=r[2][1],o=r[2][2],x=t*(e*o-u*c)-i*(o*a-u*m)+n*(a*c-e*m)),x},matrixAdj:function(r){r=kmatrix.makeMatrix(r);var t,i,n,a,e,u,m,c,o,x;if(2===r.r)t=r[0][0],i=r[0][1],n=r[1][0],a=r[1][1],x=[[a,-i],[-n,t]];else if(3===r.r){t=r[0][0],i=r[0][1],n=r[0][2],a=r[1][0],e=r[1][1],u=r[1][2],m=r[2][0],c=r[2][1],o=r[2][2];var p=e*o-u*c,l=-(a*o-u*m),f=a*c-e*m,k=-(i*o-n*c),s=t*o-n*m,M=-(t*c-i*m),h=i*u-n*e,v=-(t*u-n*a),_=t*e-i*a;x=[[p,k,h],[l,s,v],[f,M,_]]}return x&&(x=kmatrix.makeMatrix(x)),x},matrixInverse:function(r,t){var i=kmatrix.matrixDet(r);if(!i)return null;var n=kmatrix.matrixAdj(r);if(!n)return null;var a=kmatrix.deepZipWith(2,function(r){return r/=i,t&&(r=KhanUtil.roundTo(t,r)),r},n);return a=kmatrix.makeMatrix(a)},matrixPad:function(r,t,i,n){if(!r)return null;r=kmatrix.makeMatrix(r);var a=kmatrix.matrixCopy(r),e=Math.max(i,r.c);void 0===n&&(n="");var u=i-a.c;u>0&&_.times(a.r,function(r){_.times(u,function(){a[r].push(n)})});var m=t-a.r;return m>0&&_.times(m,function(){var r=[];_.times(e,function(){r.push(n)}),a.push(r)}),kmatrix.makeMatrix(a)},arrayToColumn:function(r){var t=[];return _.each(r,function(r){t.push([r])}),kmatrix.makeMatrix(t)},columnToArray:function(r){var t=[];return _.each(r,function(r){t.push(r[0])}),t}};_.each(kmatrix,function(r,t){KhanUtil[t]=r}),module.exports=kmatrix;
},{"./expressions.js":1}]},{},[2]);
