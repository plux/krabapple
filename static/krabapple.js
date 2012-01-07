(function() {
  var $, init, list_directory, main, make_link;

  $ = jQuery;

  main = function() {
    return init();
  };

  init = function() {
    if (window.location.pathname === '/') window.location.assign('/list/');
    return list_directory(window.location.pathname, $('#list_view'));
  };

  list_directory = function(dir, div) {
    return $.getJSON('/json' + dir, function(data) {
      var item, list, list_div, _i, _len, _ref;
      list = $('<ul>');
      list_div = $('<div>').addClass('list');
      _ref = data['content'];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        item = _ref[_i];
        list.append($('<li>').html(make_link(item, list_div)));
      }
      return $('#list_view').append(list_div.append(list).hide().fadeIn(500));
    });
  };

  make_link = function(item, div) {
    if (item['type'] === 'directory') {
      return $('<a>').click(function() {
        div.nextAll().remove();
        list_directory('/list/' + item['rel_path'], div);
        $(this).parent().parent().children().removeClass('hilight');
        return $(this).parent().addClass('hilight');
      }).append(item['name']);
    } else {
      return item['name'];
    }
  };

  $(document).ready(main);

}).call(this);
