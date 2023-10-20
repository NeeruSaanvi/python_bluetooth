const express = require('express');
var app = express();
const bodyParser=require('body-parser');
var fs = require('fs');
const axios = require('axios').default;
var getRawBody = require('raw-body');
var contentType = require('content-type')
var cors = require('cors')
app.use(cors('*'));

var options = {
  inflate: true,
  limit: '1000kb',
  type: 'application/json'
};
app.use(bodyParser.raw(options));

// app.use(bodyParser.json());
var http = require('http').Server(app);
var io = require('socket.io')(http, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});
var port = process.env.PORT || 3000;

var urlencodedParser = bodyParser.urlencoded({ extended: false });




// get spo2 
app.post('/sendSPo2', urlencodedParser,function(req, res) {

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('content-type', 'text/javascript');
  //console.log("sendSPo2");
  //console.log(req.body);
  if(connectedUsers["socket"] != null)
  connectedUsers["socket"].emit('spo2',{
				"data":req.body
			});
      res.send({
      status: 200,
      message: 'send'
    });

});

// get spo2 graph 
app.get('/sendSPo2Graph', urlencodedParser,function(req, res) {

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('content-type', 'text/javascript');
  if(connectedUsers["socket"] != null)
    connectedUsers["socket"].emit('spo2Graph',{
				"spo2Graph":"ssss"
			});
      
  res.send({
      status: 200,
      message: 'send'
    });


});


// get ekg graph 
app.get('/sendekg', urlencodedParser,function(req, res) {

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('content-type', 'text/javascript');
  if(connectedUsers["socket"] != null)
  connectedUsers["socket"].emit('ekg',{
				"ekg":"ssss"
			});
      res.send({
      status: 200,
      message: 'send'
    });

});

// save user into of socket 
var connectedUsers = {};
// io.origins('*:*');
io.on('connection', function(socket){
   console.log("dddd");
  socket.on('register',function(){
        //socket.username = tempwallet;
        //var dic = {'socket':socket};
        //console.log(dic);
        connectedUsers["socket"]= socket;
        
    });

  
  socket.on('disconnect', function () {
    if(socket.username != null && socket.username != undefined){
      // console.log(connectedUsers1[socket.username]);
      delete connectedUsers["socket"];     
    }
  });
  
});



http.listen(port, function() {
  console.log(port);
});
