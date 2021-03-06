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
    var data = JSON.parse(message.data);
    var clone = $('#tweet-template').clone(true).attr('id', '').removeClass("hide");
    clone.find('img').attr('src', data.img);
    clone.find('img').attr('alt', data.username);
    clone.find('.text').html(data.text);
    clone.find('.username').html(data.username);
    clone.prependTo('#tweets ul').hide().slideDown();
  }

  slack_socket.onmessage = function(message) {
    var data = JSON.parse(message.data);
    var clone = $('#slack-template').clone(true).attr('id', '').removeClass("hide");
    clone.find('img').attr('src', data.img);
    clone.find('img').attr('alt', data.username);
    clone.find('.text').html(data.text);
    clone.find('.username').html(data.username);
    clone.prependTo('#slack ul').hide().slideDown();
  }

});
