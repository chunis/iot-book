#!/usr/bin/node


const WebSocket = require('ws');
const wss = new WebSocket.WebSocketServer({ port: 3454 });

wss.on('connection', function connection(ws) {
  ws.on('message', function message(data, isBinary) {
    console.log('received: %s', data);
    wss.clients.forEach(function each(client) {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(data, { binary: isBinary });
      }
    });
  });
});
