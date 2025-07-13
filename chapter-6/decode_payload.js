#!/usr/bin/node

var data = 'QI6V2AAAYQLFjpI2BNXVB++QDezmSzUVss8wurdFA+/0zfTzDvI='
var payload = new Buffer.from(data, 'base64')
console.log(payload.toString('hex'))
