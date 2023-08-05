$(document).ready(function(){

        console.log('inside documet.read ()');
        
         var person='';
         console.log(' person : '+person);

         function myFunction() {
                console.log('inside myFunction()');

                person = prompt("Please enter your name", "nick");
                
                if (person==null){
                      console.log('person == null');
                      console.log('invoke myFunction() recursively again');
                      myFunction();
                      console.log('reutrning from myFunction()');
                    }

                else if (person==''){
                      console.log('person==empty');
                      console.log('invoke myFunction() recursively again');
                      myFunction();
                      console.log('returning from myFunction');
                      
                    }
                else if (person != null) {
                    console.log('person != null');
                    $('.welcome .welcomeLine').append($('<h2>').text('Welcome, '));
                     $('.welcome .welcomeLine').append($('<h3>').text(person+'.'));
                     $('.welcome').append($('<code>'));

                     console.log('text transformations done');
                     console.log('returning from myFunction');

                }
                
            }

        $(window).bind("load", function() {

                    console.log('inside window.bind load funtion ');
                    console.log('invokeing myFunction first time');
                    myFunction();
                    console.log('returning from window.bind load myFunction');

          });


        




        var conn = null;
        var multiplexer = null;
        var group= null;
        var private = null;
        var disconn = 0;

        console.log(' conn : '+conn);
        console.log('multiplexer : '+multiplexer);
        // function log(t,msg) {
          
        //   if (t=='g'){
        //     var control = $('.log #groupCB');
        //   }
        //   else{
        //     var control = $('.log #privateCB');
        //   }
        //   control.html(control.html() + msg + '<br/>');
        //   control.scrollTop(control.scrollTop() + 1000);
        // }

        


        function connect() {
                  console.log('inside connect()');
                  console.log('disconn before : '+disconn);
                  disconn=0;
                  console.log('disconn now : '+disconn);
                  console.log('invoking disconnect()');
                  disconnect();
                  console.log('disconnect() invoked successful');


                  var pipe = function(ws, el_name) {
                      console.log('inside pipe()');
                      var chatbox  = $(el_name + ' .chatbox');
                      var inp  = $(el_name + ' input');
                      var form = $(el_name + ' form');
                      console.log('chatbaox : '+chatbox+" inp : "+inp+" form : "+form);
                      var print = function(p) {
                          console.log('inside print()');
                          console.log('p before stringigy : '+p)
                          p = (p === undefined) ? '' : JSON.stringify(p);
                          console.log(' p : '+p);
                          var tm= new Date().toString("hh:mm tt");
                          console.log(" time : "+tm)
                          chatbox.append($("<code>").text('['+tm+']'));
                          chatbox.append($("<br>"));
                          chatbox.append($("<code>").text(p));
                          chatbox.append($("<br>"));
                          chatbox.append($("<br>"));
                          chatbox.scrollTop(chatbox.scrollTop() + 10000);
                          console.log('text transformations done ');
                          console.log('returnin from pipe()');
                      };

                      ws.onopen    = function()  { console.log('inside ws.onopen()');
                                                    var res ={'name':person,
                                                              'stage':'start'
                                                            };
                                                    console.log(' res : '+res);
                                                    res= JSON.stringify(res);
                                                    console.log(' res= json.stringfiy(res) : '+res);
                                                    ws.send(res);
                                                    console.log('returnin from ws.onopen');
                                                };
                      ws.onmessage = function(e) {  
                                                   console.log('inside ws.onmessage()');
                                                   console.log('invoking print(e.data)');
                                                    print( e.data);
                                                    console.log('print(e.data) invoke successfully');
                                                    console.log('disconn now : '+disconn);
                                                    if(disconn==1){
                                                            console.log('inside disconn==1');
                                                            console.log('invoking ws.close()');
                                                            ws.close();
                                                            console.log('ws.close() invoked successful');
                                                            console.log('invoking conn.close()');
                                                            conn.close()
                                                            //conn.close();
                                                            console.log('conn.close() invoked successful');
                                                            conn = null;
                                                            console.log('conn=null');
                                                            console.log(' conn : '+conn);
                                                            $('.welcome code').text('');
                                                            console.log('text.transformations done');
                                                    }
                                                    console.log('returnin from ws.onmessage');
                                                  };
                      ws.onclose   = function()  {
                                                    console.log('inside ws.onclose()');
                                                    print('[*]  close ');
                                                    console.log('returnin from ws.onclose');
                                                  };

                      form.submit(function() {
                          console.log('inside form.submit()');
                          // print('['+person+']', inp.val());
                          var res= {'name':person,
                                    'stage':'process',
                                      'message':inp.val()};
                          console.log(' res : '+res);
                          res= JSON.stringify(res);
                          console.log(' res= json.stringfiy(res) : '+res);
                          console.log('sending ws.send(res)');
                          ws.send(res);
                          console.log('ws.send(res) invoked successul');
                          
                          console.log('returning from form.submit');
                          return false;
                      });
                  };

                
                var transports = $('#protocols input:checked').map(function(){
                      return $(this).attr('id');
                  }).get();

                console.log('creating new sockjs connection ');
                conn = new SockJS('http://' + window.location.host + '/chat', transports);
                console.log(' conn created successful - conn : '+conn);
                console.log('creating new multiplexer object ');
               multiplexer = new MultiplexedWebSocket(conn);
               console.log('multiplexer object created successfully - multiplexer : '+multiplexer);

               
            

                $('.welcome code').text('Connecting...');
                console.log('welcome append code connecting...');

                conn.onopen = function() {
                  console.log('inside conn.onopen() ');
                  $('.welcome code').text('Connected');
                  console.log('text transformations done ');

                  console.log('invoke update_ui()');
                  update_ui();
                  console.log('update_ui() invoked successul')

                  console.log('group multiplexer creating ');
                  group  = multiplexer.channel('group');
                  console.log(' grou multiplexer : '+group);

                  console.log('invoke pipe(group');
                  pipe(group,  '.public');
                  console.log('pipe(group) invoked successfully');

                };

                

                conn.onclose = function() {
                  console.log('inside conn.onclose()');
                   $('.welcome code').text('');
                   console.log('text transformations done ');
                  conn = null;
                  console.log(' conn=null -> conn : '+conn);

                  console.log('invoke update_ui()');
                  update_ui();
                  console.log('update_ui() invoked successul')
                };



                


                
                




                // var private= multiplexer.channel('private');

                
                // pipe(private,  '.private');
        }


        $('.privateUser').click(function(e){
                      var v= $(this).children('p').text();
                      var private= multiplexer.channel(v);
                      pipe(private,  '.private')
                });



        function disconnect() {
          console.log('inside disconnect()');
          if (conn != null) {
                console.log('disconn before : '+disconn);
                disconn=1;
                console.log('disconn now : '+disconn);
                console.log('conn!=null');
                $('.welcome code').text('Diconnecting...');
                console.log('text transformations done');
                
                var res= {'name':person,
                          'stage':'end'
                           };
                console.log(' res : '+res);
                res= JSON.stringify(res);
                console.log(' res= json.stringfiy(res) : '+res);
                console.log('invoking group.send(res)');
                group.send(res)
                console.log('group.send(res) invoked successfully');
           
          }
        }

        function update_ui() {
          var msg = '';
          console.log('inside update_ui');
          if (conn == null || conn.readyState != SockJS.OPEN) {
            console.log('conn==null or conn.readyState !=SockJS.Open');
            $('#status').text('Offline').removeClass('active').addClass('inactive');
            $('#connect').text('Connect');
            console.log('text transformations done');
          } 
          else {
            console.log('conn != Null');
            $('#status').text('Online - ' + conn.protocol).removeClass('inactive').addClass('active');
            $('#connect').text('Disconnect');
            console.log('text transformations done');
          }
        }

        $('#connect').click(function() {
          console.log('clicked #connect');
          if (conn == null) {
              console.log('conn==null');
              console.log('invoking connect()');
            connect();
            console.log('invoked connect() successful');
          } 
          else {
            console.log('conn!= null');
            console.log('invoking disconnect()');
            disconnect();
            console.log('invoked disconnect() successful');
          }

          return false;
        });

        // $('form.publicSend').submit(function() {
        //   var text = $('#publictext').val();
        //   log('Sending: ' + text);
        //   conn.send(text);
        //   $('#text').val('').focus();
        //   return false;
        // });




      });