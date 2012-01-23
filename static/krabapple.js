(function() {
  var $, MAX_VISIBLE, get_visible_panes, init, init_navigation_button, list_directory, main, make_directory_link, make_file_link, make_link;

  $ = jQuery;

  MAX_VISIBLE = 3;

  main = function() {
    return init();
  };

  init = function() {
    if (window.location.pathname === '/') window.location.assign('/list/');
    init_navigation_button();
    return list_directory(window.location.pathname, $('#list_view'));
  };

  init_navigation_button = function() {
    $('#back_button').click(function() {
      var visible_panes;
      if ($('.hidden_left').length < 1) return;
      $('.hidden_left').last().removeClass('hidden_left').show();
      visible_panes = get_visible_panes();
      if (visible_panes.length > MAX_VISIBLE) {
        return visible_panes.last().addClass('hidden_right').hide();
      }
    });
    return $('#fwd_button').click(function() {
      var visible_panes;
      if ($('.hidden_right') < 1) return;
      $('.hidden_right').first().removeClass('hidden_right').show();
      visible_panes = get_visible_panes();
      if (visible_panes.length > MAX_VISIBLE) {
        return visible_panes.first().addClass('hidden_left').hide();
      }
    });
  };

  get_visible_panes = function() {
    return $('#list_view').children().filter(':visible');
  };

  list_directory = function(dir, div) {
    return $.getJSON('/json' + dir, function(data) {
      var item, list, list_div, visible_panes, _i, _len, _ref;
      list = $('<ul>');
      list_div = $('<div>').addClass('list');
      _ref = data['content'];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        item = _ref[_i];
        list.append($('<li>').html(make_link(item, list_div)));
      }
      visible_panes = get_visible_panes();
      if (visible_panes.length >= MAX_VISIBLE) {
        visible_panes.first().fadeOut(100).addClass('hidden_left');
      }
      return $('#list_view').append(list_div.append(list).hide().fadeIn(100));
    });
  };

  make_link = function(item, pane) {
    var a, link;
    link = $('<a>');
    a = item['type'] === 'directory' ? make_directory_link(pane, link, item) : item['type'] === 'file' ? make_file_link(pane, link, item) : void 0;
    return link.attr('href', a['href']).text(a['text']).click(a['click']);
  };

  make_directory_link = function(pane, link, item) {
    return {
      text: item['name'],
      href: '/list/' + item['rel_path'],
      click: function(e) {
        e.preventDefault();
        pane.nextAll().remove();
        list_directory('/list/' + item['rel_path'], pane);
        link.parent().parent().children().removeClass('hilight');
        return link.parent().addClass('hilight');
      }
    };
  };

  make_file_link = function(_pane, _link, item) {
    return {
      text: item['name'],
      href: '/file/' + item['rel_path']
    };
  };

  $(document).ready(main);

}).call(this);
