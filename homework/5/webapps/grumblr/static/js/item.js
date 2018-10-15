function populateList() {
    $.get("get_changes/" + "1970-01-01T00:00+00:00")
      .done(function(data) {
          var list = $("#item-list");
          list.data('max_time', data['max_time']);
          list.html('')
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
              var new_item = $(item.html);
              new_item.data("item-id", item.id);        
              for (var j = 0; j < item.comments.length; j++) {
                  var comment = item.comments[j];
                  var new_comment = $(comment);
                  new_item.append(new_comment);
              }
              list.prepend(new_item);
          }
      });
}

function addItem(){
    var itemField = $("#item-field");
    $.post("add_item", {"item": itemField.val()})
      .done(function(data) {
          getUpdates();
          itemField.val("").focus();
      });
}

function getComments(data) {
    var list = $("#item_" + data.item_pk)
    var new_comment = $(data.html)
    list.append(new_comment);
}

function getUpdates() {
    var list = $("#item-list")
    var max_time = list.data("max_time")
    $.post("get_changes/"+ max_time)
      .done(function(data) {
          list.data('max_time', data['max_time']);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
                  var new_item = $(item.html);
                  new_item.data("item-id", item.id);
              for (var j = 0; j < item.comments.length; j++) {
                  var comment = item.comments[j];
                  var new_comment = $(comment.html);
                  new_item.append(new_comment);
              }
              list.prepend(new_item);
          }
      });
}

$(document).ready(function () {
    var itemlist = document.getElementById("item-list");
    if (itemlist) {
        populateList();
        window.setInterval(getUpdates, 5000);
    } 
    $('#post-form').on('submit', function (event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            type: "POST",
            url: "add_item",
            data: form.serialize(),
            success: function (data) {
                $("#item-field").val("")
                getUpdates();
            }
        });
    });

    $(".item-list").on("click", ".comment-add", function (event) {
        event.preventDefault(); 
        var comment, item_pk;
        $(".comment").each(function(){
            if(this.value !=""){
                comment = this.value;
                item_pk = this.id;
            }
        })
        $.ajax({
            type: "POST",
            url: "/update_comment",
            data: { "item-pk": item_pk, "comment": comment},
            success: function (data) {
                $(".comment").val("")
                getComments(data);
            }
        });

    });

  // CSRF set-up copied from Django docs
  function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
