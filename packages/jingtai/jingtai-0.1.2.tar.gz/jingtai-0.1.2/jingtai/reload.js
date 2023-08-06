(function() {
  var ws = new WebSocket('ws://' + window.location.host + '/__reload__/')
  ws.onopen = function(evt) {
    console.log('Websocket opened')
  }
  ws.onmessage = function(evt) {
    if (evt.data === 'reload') {
      console.log('Reloading...')
      ws.close()
      document.location.reload()
    }
  }
})()
