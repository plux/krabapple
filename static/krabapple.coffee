$ = jQuery

main = ->
#  $('#hello').html(window.location.pathname)
  init()

init = ->
  if window.location.pathname is '/' then window.location.assign('/list/')
  list_directory(window.location.pathname, $('#list_view'))

list_directory = (dir, div) ->
  $.getJSON('/json' + dir, (data) ->
    list = $('<ul>')
    list_div = $('<div>').addClass('list')
    for item in data['content']
      list.append($('<li>').html(make_link(item, list_div)))
    $('#list_view').append(list_div.append(list).hide().fadeIn(500))
  )

make_link = (item, div) ->
  if item['type'] is 'directory'
    $('<a>')
      .click( ->
        div.nextAll().remove()
        list_directory('/list/' + item['rel_path'], div)
        $(this).parent().parent().children().removeClass('hilight')
        $(this).parent().addClass('hilight')
      ).append(item['name'])
  else
    item['name']

test = ->
  $('#list_view').append($('<div>').html('hej'))


$(document).ready(main)