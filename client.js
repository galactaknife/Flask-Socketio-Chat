function scroll() {
  $("#messages").animate({
    scrollTop: $("#messages").get(0).scrollHeight
  });
}

function urlify(text) {
  return text.replace(/(https?:\/\/[^\s]+)/g, function(url) {
    return "<a href='" + url + "' target='_blank'>" + url + "</a>";
  });
}

function stripTags(val) {
  return val.replace(/<details/ig, '').replace(/<\/details>/ig, '').replace(/<br>/ig, '').replace(/<br \/>/ig, '').replace(/<br\/>/ig, '').replace(/<body>/ig, '').replace(/<\/body>/ig, '').replace(/<table>/ig, '').replace(/<\/table>/ig, '').replace(/<form/ig, '').replace(/<\/form>/ig, '').replace(/<button class="command">/ig, '').replace(/<\/button>/ig, '').replace(/<script/ig, '').replace(/<\/script/ig, '').replace(/onclick/ig, '').replace(/<style>/ig, '').replace(/<\/style>/ig, '').replace(/<div/ig, '').replace(/<\/div>/ig, '').replace(/<span/ig, '').replace(/<\/span>/ig, '').replace(/<p/ig, '').replace(/<\/p>/ig, '').replace(/ class=/ig, '').replace(/<meta/ig, '');
}

function openFileUpload() {
  document.getElementById('fileToUpload').click();
}


$(document).ready(function() {
  var socket = io.connect('/', { transport : ["websocket"] });

  socket.on("connect", function() {
    var user = $("#nameArea").html();
    socket.emit("login", user);
  });

  socket.on("alert", function(data) {
    alert(data);
  });

  socket.on("users", function(data) {
    var users = data[0];
    $("#users").html('');

    for (var i = 0; i < users.length; i++) {
      var user = users[i];
      $("#users").append("<p><span class='name' style='background-color:" + JSON.parse(data[1])[user] + "; color: white;'>" + user + "</span></p>");
    }
  });

  socket.on("message", function(data) {
    if (data.length == 5) {
      $("#messages").append("<p><span class='info' style='background-color: gainsboro; color: darkred;'>private</span><span class='name' style='background-color: " + data[0] + "'>" + data[1] + "</span><span class='info' style='background-color: gainsboro; color: darkred; font-size: 10px;'>from " + data[4] + "</span>"+data[2]+"</p>");
    }
    else if (data.length == 4) {
      $("#messages").append("<p>"+"<span class='info' style='background-color: gainsboro; color: darkred;'>private</span><span class='name' style='background-color: " + data[0] + "'>"+data[1]+"</span>" + data[2] + "</p>");
    }
    else if (data.length == 3) {
      $("#messages").append("<p><span class='name' style='background-color: " + data[0] + "'>"+data[1] + "</span>" + data[2] + "</p>");
    }
    else if (data.length == 2) {
      $("#messages").append("<p><span class='name' style='background-color: darkslategray'>" + data[0] +"</span>" + data[1] + "</p>");
    }
    else {
      $("#messages").append("<p>" + data + "</p>");
    }
    scroll();
  });

  socket.on("imageBrodcast", function(data) {
    if (data) {
      $("#messages").append("<p><span class='name' style='background-color: " + data[0] + "'>" + data[1] + "</span><img class='image' src='" + data[2] + "'></p>");
      scroll();
    }
  });

  $("#submitForm").submit(function(e) {
    e.preventDefault();
    try {
      if ($("#sendArea").val().includes("clear") > 0 && $("#sendArea").val().includes("//") > 0 && $("#sendArea").val().includes("bans") <= 0) {
        $("#messages").html("<p><span class='name' style='background-color: darkslategray'>chatbot</span>Chat cleared</p>");
        $("#sendArea").val('');
        scroll();
      }
      else if ($("#sendArea").val().replace(' ', '') != '') {
        $("#sendArea").val().slice(0, 2) == "//" ? socket.emit("message", stripTags($("#sendArea").val())) : socket.emit("message", urlify(stripTags($("#sendArea").val())));
        $("#sendArea").val('');
      }
      $("#uploadImage").css("opacity", 0.5)
    }
    catch(err) {
      $("#logout").click();
    }
  });

  $("#imageUpload").submit(function(e) {
    try {
      e.preventDefault();
      var file = document.querySelector('input[type=file]').files[0];
      $(this)[0].reset();
      if (file.size > 1800000) {
        alert("File is too big!  Max file size is 1.8 MB");
      }
      else {
        var reader  = new FileReader();
        reader.addEventListener("load", function() {
          socket.emit("image", reader.result);
        }, false);
        if (file) {
          reader.readAsDataURL(file);
        }
      }
    }
    catch(err) {
      return;
    }
  });

  $("#uploadImage").click(function() {
    if ($("#sendArea").val().length == 0) {
      openFileUpload();
    }
  });

  $("#fileToUpload").change(function() {
    $("#imageUpload").submit();
  });

  $("#logout").click(function() {
    socket.disconnect();
  });

  $("#sendArea").keyup(function() {
    $(this).val().length > 0 ? $("#uploadImage").css("opacity", 0) : $("#uploadImage").css("opacity", 0.5);
  });
});

$(window).bind('beforeunload', function() {
  socket.disconnect();
});

$(document).on("click", ".name", function() {
  if ($("#sendArea").val()[$("#sendArea").val().length-1] == ' ' || $("#sendArea").val()[$("#sendArea").val().length-1] == null) {
    $("#sendArea").val($("#sendArea").val() + '@' + event.target.innerHTML + ' ');
  }
  else {
    $("#sendArea").val($("#sendArea").val() + " @" + event.target.innerHTML + ' ');
  }
  $("#sendArea").val().length > 0 ? $("#uploadImage").css("opacity", 0) : $("#uploadImage").css("opacity", 0.5);
});

$(document).on("click", ".command", function() {
  if ($("#sendArea").val()[$("#sendArea").val().length-1] == ' ' || $("#sendArea").val()[$("#sendArea").val().length-1] == null) {
    $("#sendArea").val($("#sendArea").val() + event.target.innerHTML.replace("&amp;", '&') + ' ');
  }
  else {
    $("#sendArea").val($("#sendArea").val() + ' ' + event.target.innerHTML.replace("&amp;", '&') + ' ');
  }
});
