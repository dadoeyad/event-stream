$(function() {

  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var tweets_url = ws_scheme + '://' + window.location.host + window.location.pathname + "tweets";
  var slack_url = ws_scheme + '://' + window.location.host + window.location.pathname + "slack";
  var options = {'automaticOpen': false};
  var tweets_socket = new ReconnectingWebSocket(tweets_url, null, options);
  var slack_socket = new ReconnectingWebSocket(slack_url, null, options);

  $('#connect').click(function(){
    tab = $('.nav-tabs .active').text().toLowerCase();
    tab = $.trim(tab);

    if (tab == 'tweets'){
        tweets_socket.open();
    } else {
        slack_socket.open();
    }
  })

  $('#disconnect').click(function(){
    tweets_socket.close();
    slack_socket.close();
  })

  tweets_socket.onmessage = function(message) {
    $('<li class="list-group-item">'
        + message.data
    + '</li>').prependTo('#tweets ul').hide().slideDown();
  }

  slack_socket.onmessage = function(message) {
    console.log(message);
    $('<li class="list-group-item">'
        + message.data
    + '</li>').prependTo('#slack ul').hide().slideDown();
  }

});
