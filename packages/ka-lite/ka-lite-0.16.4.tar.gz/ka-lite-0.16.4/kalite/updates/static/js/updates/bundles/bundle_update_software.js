require=(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({"update_software":[function(require,module,exports){
(function (global){
function software_check_callback(e,t){e&&!e.completed||(messsages.clear_messages(),refresh_countdown_dialog_box(15))}function refresh_countdown_dialog_box(e){$("#refresh-page-dialog").dialog({modal:!0,title:gettext("Installation finished."),width:"auto",resizable:!1});var t=1e3*e,s=1e3,a="";a=sprintf(gettext("Installation finished! Refreshing the page in %(sec)s seconds"),{sec:e}),$("#dialog-content").html(a),setInterval(function(){if(t>0){var e=Math.floor(t/1e3);a=sprintf(gettext("Installation finished! Refreshing the page in %(sec)s seconds"),{sec:e}),$("#dialog-content").html(a),t-=s}else window.location.reload()},s)}function version_callback(e){var t="{{ software_version }}",s=e.version;if(s){if(t!=s){$("#update_info").show(),$("#internet_update").show(),version_info=e.version_info,$("#remote_version").text(s),version_info.hasOwnProperty(s)&&$("#remote_release_date").text(version_info[s].release_date);for(var a in version_info){if(version_info[a].new_features)for(var i in version_info[a].new_features)$("#new_features").append("<li>"+version_info[a].new_features[i]+"</li>");else $("#new_features").append(sprintf("<li>(%s)</li>",gettext("None")));if(version_info[a].bugs_fixed)for(var n in version_info[a].bugs_fixed)$("#bugs_fixed").append("<li>"+version_info[a].bugs_fixed[n]+"</li>");else $("#bugs_fixed").append(gettext("<li>(%s)</li>",gettext("None")))}}}else show_message("error",gettext("Remote version information unavailable."))}function download_urls_callback(e){locale="en",$("#software_available").append(sprintf("<option value='%s'>%s (%s MB)</option>",e[locale].url,locale,e[locale].size))}function download_initiate_callback_generator(e){return function(){var t={};t[gettext("Yes")]=function(){api.doRequest(global.UPDATE_SOFTWARE_URL,{mechanism:$(e).attr("mechanism")}).success(function(){base.updatesStart_callback("update")}).fail(function(e){messages.show_message("error",sprintf(gettext("Error starting update process %(status)s: %(responseText)s"),e))}),$(this).remove()},t[gettext("No")]=function(){$(this).remove()},$("<div></div>").appendTo("body").html("<div>"+gettext("Are you sure you want to update your installation of KA Lite? This process is irreversible!")+"</div>").dialog({modal:!0,title:gettext("Confirm update"),width:"auto",resizable:!1,buttons:t})}}function update_server_status(){connectivity.with_online_status("server",function(e){e?base.updatesStart("update",1e3,software_callbacks):(messages.clear_messages(),messages.show_message("error",gettext("Could not connect to the central server; software cannot be updated at this time.")))})}var api=require("utils/api"),$=require("base/jQuery"),messages=require("utils/messages"),base=require("updates/base"),connectivity=require("utils/connectivity"),sprintf=require("sprintf-js").sprintf,software_callbacks={check:software_check_callback};$(function(){$("#refresh-page-dialog").hide(),setTimeout(function(){connectivity.get_server_status({path:GET_SERVER_INFO_URL},["online"],function(e){$("#software_available").removeAttr("disabled"),$("#download-update-kalite").removeAttr("disabled"),$("#git-update-kalite").removeAttr("disabled"),messages.clear_messages("id_offline_message")})},200),$("#download-update-kalite").click(download_initiate_callback_generator("#download-update-kalite")),$("#git-update-kalite").click(download_initiate_callback_generator("#git-update-kalite"))}),$(function(){api.doRequest(CENTRAL_KALITE_VERSION_URL,null,{dataType:"jsonp"}).success(function(e){version_callback(e),update_server_status()}).fail(update_server_status),api.doRequest(CENTRAL_KALITE_DOWNLOAD_URL,null,{dataType:"jsonp"}).success(function(e){download_urls_callback(e),update_server_status()}).fail(update_server_status)});
}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})

},{"base/jQuery":45,"sprintf-js":660,"updates/base":129,"utils/api":115,"utils/connectivity":116,"utils/messages":119}]},{},["update_software"])
//# sourceMappingURL=data:application/json;charset:utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9mYWN0b3ItYnVuZGxlL25vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJrYWxpdGUvdXBkYXRlcy9zdGF0aWMvanMvdXBkYXRlcy9idW5kbGVfbW9kdWxlcy91cGRhdGVfc29mdHdhcmUuanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7O0FDQUEiLCJmaWxlIjoiZ2VuZXJhdGVkLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiBlKHQsbixyKXtmdW5jdGlvbiBzKG8sdSl7aWYoIW5bb10pe2lmKCF0W29dKXt2YXIgYT10eXBlb2YgcmVxdWlyZT09XCJmdW5jdGlvblwiJiZyZXF1aXJlO2lmKCF1JiZhKXJldHVybiBhKG8sITApO2lmKGkpcmV0dXJuIGkobywhMCk7dmFyIGY9bmV3IEVycm9yKFwiQ2Fubm90IGZpbmQgbW9kdWxlICdcIitvK1wiJ1wiKTt0aHJvdyBmLmNvZGU9XCJNT0RVTEVfTk9UX0ZPVU5EXCIsZn12YXIgbD1uW29dPXtleHBvcnRzOnt9fTt0W29dWzBdLmNhbGwobC5leHBvcnRzLGZ1bmN0aW9uKGUpe3ZhciBuPXRbb11bMV1bZV07cmV0dXJuIHMobj9uOmUpfSxsLGwuZXhwb3J0cyxlLHQsbixyKX1yZXR1cm4gbltvXS5leHBvcnRzfXZhciBpPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7Zm9yKHZhciBvPTA7bzxyLmxlbmd0aDtvKyspcyhyW29dKTtyZXR1cm4gc30pIiwiZnVuY3Rpb24gc29mdHdhcmVfY2hlY2tfY2FsbGJhY2soZSx0KXtlJiYhZS5jb21wbGV0ZWR8fChtZXNzc2FnZXMuY2xlYXJfbWVzc2FnZXMoKSxyZWZyZXNoX2NvdW50ZG93bl9kaWFsb2dfYm94KDE1KSl9ZnVuY3Rpb24gcmVmcmVzaF9jb3VudGRvd25fZGlhbG9nX2JveChlKXskKFwiI3JlZnJlc2gtcGFnZS1kaWFsb2dcIikuZGlhbG9nKHttb2RhbDohMCx0aXRsZTpnZXR0ZXh0KFwiSW5zdGFsbGF0aW9uIGZpbmlzaGVkLlwiKSx3aWR0aDpcImF1dG9cIixyZXNpemFibGU6ITF9KTt2YXIgdD0xZTMqZSxzPTFlMyxhPVwiXCI7YT1zcHJpbnRmKGdldHRleHQoXCJJbnN0YWxsYXRpb24gZmluaXNoZWQhIFJlZnJlc2hpbmcgdGhlIHBhZ2UgaW4gJShzZWMpcyBzZWNvbmRzXCIpLHtzZWM6ZX0pLCQoXCIjZGlhbG9nLWNvbnRlbnRcIikuaHRtbChhKSxzZXRJbnRlcnZhbChmdW5jdGlvbigpe2lmKHQ+MCl7dmFyIGU9TWF0aC5mbG9vcih0LzFlMyk7YT1zcHJpbnRmKGdldHRleHQoXCJJbnN0YWxsYXRpb24gZmluaXNoZWQhIFJlZnJlc2hpbmcgdGhlIHBhZ2UgaW4gJShzZWMpcyBzZWNvbmRzXCIpLHtzZWM6ZX0pLCQoXCIjZGlhbG9nLWNvbnRlbnRcIikuaHRtbChhKSx0LT1zfWVsc2Ugd2luZG93LmxvY2F0aW9uLnJlbG9hZCgpfSxzKX1mdW5jdGlvbiB2ZXJzaW9uX2NhbGxiYWNrKGUpe3ZhciB0PVwie3sgc29mdHdhcmVfdmVyc2lvbiB9fVwiLHM9ZS52ZXJzaW9uO2lmKHMpe2lmKHQhPXMpeyQoXCIjdXBkYXRlX2luZm9cIikuc2hvdygpLCQoXCIjaW50ZXJuZXRfdXBkYXRlXCIpLnNob3coKSx2ZXJzaW9uX2luZm89ZS52ZXJzaW9uX2luZm8sJChcIiNyZW1vdGVfdmVyc2lvblwiKS50ZXh0KHMpLHZlcnNpb25faW5mby5oYXNPd25Qcm9wZXJ0eShzKSYmJChcIiNyZW1vdGVfcmVsZWFzZV9kYXRlXCIpLnRleHQodmVyc2lvbl9pbmZvW3NdLnJlbGVhc2VfZGF0ZSk7Zm9yKHZhciBhIGluIHZlcnNpb25faW5mbyl7aWYodmVyc2lvbl9pbmZvW2FdLm5ld19mZWF0dXJlcylmb3IodmFyIGkgaW4gdmVyc2lvbl9pbmZvW2FdLm5ld19mZWF0dXJlcykkKFwiI25ld19mZWF0dXJlc1wiKS5hcHBlbmQoXCI8bGk+XCIrdmVyc2lvbl9pbmZvW2FdLm5ld19mZWF0dXJlc1tpXStcIjwvbGk+XCIpO2Vsc2UgJChcIiNuZXdfZmVhdHVyZXNcIikuYXBwZW5kKHNwcmludGYoXCI8bGk+KCVzKTwvbGk+XCIsZ2V0dGV4dChcIk5vbmVcIikpKTtpZih2ZXJzaW9uX2luZm9bYV0uYnVnc19maXhlZClmb3IodmFyIG4gaW4gdmVyc2lvbl9pbmZvW2FdLmJ1Z3NfZml4ZWQpJChcIiNidWdzX2ZpeGVkXCIpLmFwcGVuZChcIjxsaT5cIit2ZXJzaW9uX2luZm9bYV0uYnVnc19maXhlZFtuXStcIjwvbGk+XCIpO2Vsc2UgJChcIiNidWdzX2ZpeGVkXCIpLmFwcGVuZChnZXR0ZXh0KFwiPGxpPiglcyk8L2xpPlwiLGdldHRleHQoXCJOb25lXCIpKSl9fX1lbHNlIHNob3dfbWVzc2FnZShcImVycm9yXCIsZ2V0dGV4dChcIlJlbW90ZSB2ZXJzaW9uIGluZm9ybWF0aW9uIHVuYXZhaWxhYmxlLlwiKSl9ZnVuY3Rpb24gZG93bmxvYWRfdXJsc19jYWxsYmFjayhlKXtsb2NhbGU9XCJlblwiLCQoXCIjc29mdHdhcmVfYXZhaWxhYmxlXCIpLmFwcGVuZChzcHJpbnRmKFwiPG9wdGlvbiB2YWx1ZT0nJXMnPiVzICglcyBNQik8L29wdGlvbj5cIixlW2xvY2FsZV0udXJsLGxvY2FsZSxlW2xvY2FsZV0uc2l6ZSkpfWZ1bmN0aW9uIGRvd25sb2FkX2luaXRpYXRlX2NhbGxiYWNrX2dlbmVyYXRvcihlKXtyZXR1cm4gZnVuY3Rpb24oKXt2YXIgdD17fTt0W2dldHRleHQoXCJZZXNcIildPWZ1bmN0aW9uKCl7YXBpLmRvUmVxdWVzdChnbG9iYWwuVVBEQVRFX1NPRlRXQVJFX1VSTCx7bWVjaGFuaXNtOiQoZSkuYXR0cihcIm1lY2hhbmlzbVwiKX0pLnN1Y2Nlc3MoZnVuY3Rpb24oKXtiYXNlLnVwZGF0ZXNTdGFydF9jYWxsYmFjayhcInVwZGF0ZVwiKX0pLmZhaWwoZnVuY3Rpb24oZSl7bWVzc2FnZXMuc2hvd19tZXNzYWdlKFwiZXJyb3JcIixzcHJpbnRmKGdldHRleHQoXCJFcnJvciBzdGFydGluZyB1cGRhdGUgcHJvY2VzcyAlKHN0YXR1cylzOiAlKHJlc3BvbnNlVGV4dClzXCIpLGUpKX0pLCQodGhpcykucmVtb3ZlKCl9LHRbZ2V0dGV4dChcIk5vXCIpXT1mdW5jdGlvbigpeyQodGhpcykucmVtb3ZlKCl9LCQoXCI8ZGl2PjwvZGl2PlwiKS5hcHBlbmRUbyhcImJvZHlcIikuaHRtbChcIjxkaXY+XCIrZ2V0dGV4dChcIkFyZSB5b3Ugc3VyZSB5b3Ugd2FudCB0byB1cGRhdGUgeW91ciBpbnN0YWxsYXRpb24gb2YgS0EgTGl0ZT8gVGhpcyBwcm9jZXNzIGlzIGlycmV2ZXJzaWJsZSFcIikrXCI8L2Rpdj5cIikuZGlhbG9nKHttb2RhbDohMCx0aXRsZTpnZXR0ZXh0KFwiQ29uZmlybSB1cGRhdGVcIiksd2lkdGg6XCJhdXRvXCIscmVzaXphYmxlOiExLGJ1dHRvbnM6dH0pfX1mdW5jdGlvbiB1cGRhdGVfc2VydmVyX3N0YXR1cygpe2Nvbm5lY3Rpdml0eS53aXRoX29ubGluZV9zdGF0dXMoXCJzZXJ2ZXJcIixmdW5jdGlvbihlKXtlP2Jhc2UudXBkYXRlc1N0YXJ0KFwidXBkYXRlXCIsMWUzLHNvZnR3YXJlX2NhbGxiYWNrcyk6KG1lc3NhZ2VzLmNsZWFyX21lc3NhZ2VzKCksbWVzc2FnZXMuc2hvd19tZXNzYWdlKFwiZXJyb3JcIixnZXR0ZXh0KFwiQ291bGQgbm90IGNvbm5lY3QgdG8gdGhlIGNlbnRyYWwgc2VydmVyOyBzb2Z0d2FyZSBjYW5ub3QgYmUgdXBkYXRlZCBhdCB0aGlzIHRpbWUuXCIpKSl9KX12YXIgYXBpPXJlcXVpcmUoXCJ1dGlscy9hcGlcIiksJD1yZXF1aXJlKFwiYmFzZS9qUXVlcnlcIiksbWVzc2FnZXM9cmVxdWlyZShcInV0aWxzL21lc3NhZ2VzXCIpLGJhc2U9cmVxdWlyZShcInVwZGF0ZXMvYmFzZVwiKSxjb25uZWN0aXZpdHk9cmVxdWlyZShcInV0aWxzL2Nvbm5lY3Rpdml0eVwiKSxzcHJpbnRmPXJlcXVpcmUoXCJzcHJpbnRmLWpzXCIpLnNwcmludGYsc29mdHdhcmVfY2FsbGJhY2tzPXtjaGVjazpzb2Z0d2FyZV9jaGVja19jYWxsYmFja307JChmdW5jdGlvbigpeyQoXCIjcmVmcmVzaC1wYWdlLWRpYWxvZ1wiKS5oaWRlKCksc2V0VGltZW91dChmdW5jdGlvbigpe2Nvbm5lY3Rpdml0eS5nZXRfc2VydmVyX3N0YXR1cyh7cGF0aDpHRVRfU0VSVkVSX0lORk9fVVJMfSxbXCJvbmxpbmVcIl0sZnVuY3Rpb24oZSl7JChcIiNzb2Z0d2FyZV9hdmFpbGFibGVcIikucmVtb3ZlQXR0cihcImRpc2FibGVkXCIpLCQoXCIjZG93bmxvYWQtdXBkYXRlLWthbGl0ZVwiKS5yZW1vdmVBdHRyKFwiZGlzYWJsZWRcIiksJChcIiNnaXQtdXBkYXRlLWthbGl0ZVwiKS5yZW1vdmVBdHRyKFwiZGlzYWJsZWRcIiksbWVzc2FnZXMuY2xlYXJfbWVzc2FnZXMoXCJpZF9vZmZsaW5lX21lc3NhZ2VcIil9KX0sMjAwKSwkKFwiI2Rvd25sb2FkLXVwZGF0ZS1rYWxpdGVcIikuY2xpY2soZG93bmxvYWRfaW5pdGlhdGVfY2FsbGJhY2tfZ2VuZXJhdG9yKFwiI2Rvd25sb2FkLXVwZGF0ZS1rYWxpdGVcIikpLCQoXCIjZ2l0LXVwZGF0ZS1rYWxpdGVcIikuY2xpY2soZG93bmxvYWRfaW5pdGlhdGVfY2FsbGJhY2tfZ2VuZXJhdG9yKFwiI2dpdC11cGRhdGUta2FsaXRlXCIpKX0pLCQoZnVuY3Rpb24oKXthcGkuZG9SZXF1ZXN0KENFTlRSQUxfS0FMSVRFX1ZFUlNJT05fVVJMLG51bGwse2RhdGFUeXBlOlwianNvbnBcIn0pLnN1Y2Nlc3MoZnVuY3Rpb24oZSl7dmVyc2lvbl9jYWxsYmFjayhlKSx1cGRhdGVfc2VydmVyX3N0YXR1cygpfSkuZmFpbCh1cGRhdGVfc2VydmVyX3N0YXR1cyksYXBpLmRvUmVxdWVzdChDRU5UUkFMX0tBTElURV9ET1dOTE9BRF9VUkwsbnVsbCx7ZGF0YVR5cGU6XCJqc29ucFwifSkuc3VjY2VzcyhmdW5jdGlvbihlKXtkb3dubG9hZF91cmxzX2NhbGxiYWNrKGUpLHVwZGF0ZV9zZXJ2ZXJfc3RhdHVzKCl9KS5mYWlsKHVwZGF0ZV9zZXJ2ZXJfc3RhdHVzKX0pOyJdfQ==
