function populateList() {
    console.log("populate!");
    // $.get("get_items")
    $.get("get_changes/" + "1970-01-01T00:00+00:00")
      .done(function(data) {
          console.log("populate max_time");
          console.log(data['max_time']);
          var list = $("#item-list");
          list.data('max_time', data['max_time']);
          list.html('')
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
              var new_item = $(item.html);
              new_item.data("item-id", item.id);
              list.append(new_item);
              for (var j = 0; j < item.comments.length; j++) {
                  var comment = item.comments[j];
                  var new_comment = $(comment.html);
                  new_item.append(new_comment);
              }
          }
      });
}

function addItem(){
    var itemField = $("#item-field");
    $.post("add_item", {"item": itemField.val()})
      .done(function(data) {
          console.log("add item!");
          getUpdates();
          itemField.val("").focus();
      });
}
function addcomment() {
    var item_pk = $("#item-pk");
    var comment = $("#comment-field");
    console.log("comment");
    $.post("update_comment", {"item-pk": item_pk.val(), "comment": comment.val()})
        .done(function (data) {
            console.log("add item!");
            getUpdates();
            itemField.val("").focus();
        });
}

function getUpdates() {
    var list = $("#item-list")
    var max_time = list.data("max_time")
    console.log("update max_time");
    console.log(max_time);
    $.post("get_changes/"+ max_time)
      .done(function(data) {
          list.data('max_time', data['max_time']);
          console.log(data.items);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
                //   console.log(item);
                  var new_item = $(item.html);
                  new_item.data("item-id", item.id);
                  list.append(new_item);
                  console.log(new_item);
                  console.log(item.comments);
              for (var j = 0; j < item.comments.length; j++) {
                  var comment = item.comments[j];
                  var new_comment = $(comment.html);
                  new_item.append(new_comment);
              }
          }
      });
}

$(document).ready(function () {
  // Add event-handlers
//   $("#add-btn").click(addItem);
//   $("#item-field").keypress(function (e) { if (e.which == 13) addItem(); } );

//   $(".comment-add").click(addcomment);
//   $(".comment-field").keypress(function (e) { if (e.which == 13) addcomment(); } );

  populateList();
//   $(".comment-field").focus();

  window.setInterval(getUpdates, 10000);

    $('#post-form').on('submit', function (event) {
        event.preventDefault(); // Prevent form from being submitted
        var form = $(this);
        $.ajax({
            type: "POST",
            url: "add_item",
            data: form.serialize(), // serializes the form's elements.
            success: function (data) {
                console.log("add item!");
                getUpdates();
            }
        });
    });

    $(".container").on("click", ".comment-add", function (event) {
        event.preventDefault();
        console.log("comment");
        var item_pk = $(".item-pk");
        var comment = $(".comment-field");
        $.ajax({
            type: "POST",
            url: "update_comment",
            data: { "item-pk": item_pk.val(), "comment": comment.val() },
            success: function (data) {
                console.log("add comment!");
                getUpdates();
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
