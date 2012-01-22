$ = jQuery

MAX_VISIBLE = 3

main = ->
  init()

init = ->
  if window.location.pathname is '/' then window.location.assign('/list/')
  init_navigation_button()
  list_directory(window.location.pathname, $('#list_view'))

init_navigation_button = ->
  $('#back_button').click( ->
    if $('.hidden_left').length < 1 then return
    $('.hidden_left').last().removeClass('hidden_left').show()
    visible_panes = get_visible_panes()
    if visible_panes.length > MAX_VISIBLE
      visible_panes.last().addClass('hidden_right').hide()
  )

  $('#fwd_button').click( ->
    if $('.hidden_right') < 1 then return
    $('.hidden_right').first().removeClass('hidden_right').show()
    visible_panes = get_visible_panes()
    if visible_panes.length > MAX_VISIBLE
      visible_panes.first().addClass('hidden_left').hide()

   )

get_visible_panes = ->
  $('#list_view').children().filter(':visible')

list_directory = (dir, div) ->
  $.getJSON('/json' + dir, (data) ->
    list = $('<ul>')
    list_div = $('<div>').addClass('list')
    for item in data['content']
      list.append($('<li>').html(make_link(item, list_div)))
    visible_panes = get_visible_panes()
    if visible_panes.length >= MAX_VISIBLE
      visible_panes.first().fadeOut(100).addClass('hidden_left')
    $('#list_view').append(list_div.append(list).hide().fadeIn(100))
  )

make_link = (item, pane) ->
  link = $('<a>')
  a = if item['type'] is 'directory'
        make_directory_link(pane, link, item)
      else if item['type'] is 'file'
        make_file_link(pane, link, item)

  link.attr('href', a['href']).text(a['text']).click(a['click'])

make_directory_link = (pane, link, item) ->
    text : item['name']
    href : '/list/' + item['rel_path']
    click: (e) ->
      e.preventDefault()
      pane.nextAll().remove()
      list_directory('/list/' + item['rel_path'], pane)
      link.parent().parent().children().removeClass('hilight')
      link.parent().addClass('hilight')


make_file_link = (_pane, _link, item) ->
    text : item['name']
    href : '/file/' + item['rel_path']
    click: ->

$(document).ready(main)