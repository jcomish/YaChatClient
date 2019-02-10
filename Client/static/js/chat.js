$(".messages").animate({ scrollTop: $(document).height() }, "fast");

$("#profile-img").click(function() {
	$("#status-options").toggleClass("active");
});

$(".expand-button").click(function() {
  $("#profile").toggleClass("expanded");
	$("#contacts").toggleClass("expanded");
});

$("#status-options ul li").click(function() {
	$("#profile-img").removeClass();
	$("#status-online").removeClass("active");
	$("#status-away").removeClass("active");
	$("#status-busy").removeClass("active");
	$("#status-offline").removeClass("active");
	$(this).addClass("active");

	if($("#status-online").hasClass("active")) {
		$("#profile-img").addClass("online");
	} else if ($("#status-away").hasClass("active")) {
		$("#profile-img").addClass("away");
	} else if ($("#status-busy").hasClass("active")) {
		$("#profile-img").addClass("busy");
	} else if ($("#status-offline").hasClass("active")) {
		$("#profile-img").addClass("offline");
	} else {
		$("#profile-img").removeClass();
	};

	$("#status-options").removeClass("active");
});

//NOTE: Update this to send a message to everyone else in the chat room using a backend function.
function newMessage() {
	message = $(".message-input input").val();
	if($.trim(message) == '') {
		return false;
	}

	var today = new Date();
	var date = (today.getMonth() + 1) +'/' + today.getDate() + '/' + today.getFullYear();
    var hours = today.getHours() + ":";
    var minutes = today.getMinutes();
    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    var dateTime = date + ' ' + hours + minutes;
    var name = document.getElementById("screen_name").textContent;

	$('<li class="sent"><div><img src="' + LetterAvatar(name, 25) + '"><p>' + message + '</p></li>' +
	'<p class="subtext-left">' + dateTime + '</p>' +
	'</div>').appendTo($('.messages ul'));
	$('.message-input input').val(null);
	$('.contact.active .preview').html('<span>You: </span>' + message);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

//NOTE: Update this to send a message to everyone else in the chat room using a backend function.
function recvMessage(message) {
    JSON.stringify(message);
	if($.trim(message.message) == '') {
		return false;
	}
	$('<li class="replies"><div><img src="' + LetterAvatar(String(message.user), 25) + '"><p>' + String(message.message) + '</p></li>' +
	'<p class="subtext-right">' + String(message.user) +'</p>' +
	'<p class="subtext-right">' + String(message.timestamp) + '</p>' +
	'</div>').appendTo($('.messages ul'));
	$('.message-input input').val(null);
	$('.contact.active .preview').html('<span>You: </span>' + message.message);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

function systemMessage(message) {
    $('<div><p class="subtext-center">' + message +'</p></div>').appendTo($('.messages ul'));
	$('.message-input input').val(null);
	$('.contact.active .preview').html('<span>You: </span>' + message.message);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");
}

(function(w, d){


    function LetterAvatar (name, size) {

        name  = name || '';
        size  = size || 60;

        var colours = [
                "#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#34495e", "#16a085", "#27ae60", "#2980b9", "#8e44ad", "#2164a8",
                "#f1c40f", "#e67e22", "#e74c3c", "#ecf0f1", "#95a5a6", "#f39c12", "#d35400", "#c0392b", "#bdc3c7", "#7f8c8d"
            ],

            nameSplit = String(name).toUpperCase().split(' '),
            initials, charIndex, colourIndex, canvas, context, dataURI;


        if (nameSplit.length == 1) {
            initials = nameSplit[0] ? nameSplit[0].charAt(0):'?';
        } else {
            initials = nameSplit[0].charAt(0) + nameSplit[1].charAt(0);
        }

        if (w.devicePixelRatio) {
            size = (size * w.devicePixelRatio);
        }

        charIndex     = (initials == '?' ? 72 : initials.charCodeAt(0)) - 64;
        colourIndex   = charIndex % 20;
        canvas        = d.createElement('canvas');
        canvas.width  = size;
        canvas.height = size;
        context       = canvas.getContext("2d");

        context.fillStyle = colours[colourIndex - 1];
        context.fillRect (0, 0, canvas.width, canvas.height);
        context.font = Math.round(canvas.width/2)+"px Arial";
        context.textAlign = "center";
        context.fillStyle = "#FFF";
        context.fillText(initials, size / 2, size / 1.5);

        dataURI = canvas.toDataURL();
        canvas  = null;

        return dataURI;
    }

    LetterAvatar.transform = function() {

        Array.prototype.forEach.call(d.querySelectorAll('img[avatar]'), function(img, name) {
            name = img.getAttribute('avatar');
            img.src = LetterAvatar(name, img.getAttribute('width'));
            img.removeAttribute('avatar');
            img.setAttribute('alt', name);
        });
    };


    // AMD support
    if (typeof define === 'function' && define.amd) {

        define(function () { return LetterAvatar; });

    // CommonJS and Node.js module support.
    } else if (typeof exports !== 'undefined') {

        // Support Node.js specific `module.exports` (which can be a function)
        if (typeof module != 'undefined' && module.exports) {
            exports = module.exports = LetterAvatar;
        }

        // But always support CommonJS module 1.1.1 spec (`exports` cannot be a function)
        exports.LetterAvatar = LetterAvatar;

    } else {
        window.LetterAvatar = LetterAvatar;

        d.addEventListener('DOMContentLoaded', function(event) {
            LetterAvatar.transform();
        });
    }

})(window, document);

function setText(id,newvalue) {
  var s= document.getElementById(id);
  s.innerHTML = newvalue;
}

// Show an element
var show = function (elem) {
	elem.style.display = 'block';
};

// Hide an element
var hide = function (elem) {
	elem.style.display = 'none';
};

function truncate(string){
   var number_of_chars = (Math.round(Number(document.getElementById("messages").clientWidth) / 11));

   if (string.length > number_of_chars)
      return string.substring(0, number_of_chars) + '...';
   else
      return string;
}

// Get the modal
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById("settings");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function hideModal() {
  document.getElementById("myModal").style.display = "none";
}

$(document).ready(function() {
    // In order to avoid using a DB to keep the front-end updated, I am using a web socket.
    // NOTE: This is only used for communication from already-recieved messages. All communications
    //       are still done in TCP and UDP sockets as foudn in ChatSocketListener and ChatSocketSender.
    var socket = io.connect('http://127.0.0.1:23946/chat_client');
    document.getElementById("profile-img").setAttribute("src", LetterAvatar("Anonymous", 100));

	$('#settings_submit').on('click', function(e) {

//        var group_name = $('#group_name').innerHTML;
//        var group_name = ctrl.getElementsByTagName('p')[0].innerHTML;
        var group_name = document.getElementById("group_name").textContent;
        console.log(group_name);
        if (group_name != "Disconnected") {
            $('#existing_connection_error').fadeIn(1000).fadeOut(5000);
            return
        }

        var name = $('#name').val();
        var host = $('#host').val();
        var port = $('#port').val();
        var chat_port = $('#chat_port').val();

        req = $.ajax({
            url : '/connect_to_mms',
            type : 'POST',
            data : { 'name' : name, 'host' : host, 'port' : port, 'chat_port' : chat_port }
        });

        req.done(function(data) {
            if (data.status == "Successfully connected!") {
                $('#success_connection_message').fadeIn(1000).fadeOut(5000);
                if (document.getElementById("people_in_group").value) {
                    var group_text = truncate(document.getElementById("chat_port").value + ", " +
                                              document.getElementById("name").value + ", " +
                                              document.getElementById("people_in_group").value)
                                  }
                else {
                    var group_text = truncate(document.getElementById("chat_port").value + ", " +
                                              document.getElementById("name").value)
                }

                setText("group_name", truncate(data.group_name))
                setText("screen_name", document.getElementById("name").value)
                document.getElementById("profile-img").setAttribute("src", LetterAvatar(String(name), 100));
            }
            else {
                if (data.status == "Failed to connect. Screen name already taken!") {
                    $('#fail_connection_message_screen_name').fadeIn(1000).fadeOut(5000);
                }
                else {
                    $('#fail_connection_message_bad_server').fadeIn(1000).fadeOut(5000);
                }
            }
        });
    });

    $('#exit_room').on('click', function() {
        req = $.ajax({
            url : '/exit_room',
            type : 'POST',
        });

        req.done(function(data) {
            if (data.status == "Successfully disconnected!") {
                $('#success_disconnection_message').fadeIn(1000).fadeOut(5000);

                setText("group_name", "Disconnected")
                setText("screen_name", "Anonymous")
            }
            else {
                $('#fail_disconnection_message').fadeIn(1000).fadeOut(5000);
            }
        });
    });

    function send_message_to_group() {
         var message = $(".message-input input").val();

        req = $.ajax({
            url : '/send_message',
            type : 'POST',
            data: { 'message': message },
        });

        req.done(function(data) {
            newMessage();
            var element = document.getElementById("messages");
            element.scrollTop = element.scrollHeight;
        });
    }

    $(window).on('keydown', function(e) {
      if (e.which == 13) {
        send_message_to_group();
      }
    });

    $('#send_message_button').on('click', send_message_to_group);

    socket.on('update_group_name', function(data) {
        if (data.group_name) {
            setText("group_name", truncate(data.group_name));
        }

        if (data.isEnter) {
            systemMessage(data.user + " has entered the room.");
        }
        else {
            systemMessage(data.user + " has exited the room.");
        }

    });

    socket.on('post_message', function(data) {
        recvMessage(data);
    });
});