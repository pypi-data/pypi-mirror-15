========================
sockjsChat
========================

A sockJS based Chat-Server/Chat-System primary using the SockJS protocol.

-------
Details
-------

:Author: Anirban Roy Das
:Email: anirban.nick@gmail.com
:Copyright(C): 2016, Anirban Roy Das <anirban.nick@gmail.com>

Check sockjsChat/LICENSE file for full Copyright notice.

--------
Overview
--------

sockjsChat is a very basic Chat Server which can be set up locally to chat in your LAN. It supports both **Public Chat** among all participants connected simultaneously at a particulartime and also **Private Chat** between those individual participants.

It uses the **sockjs** protocol to implement the real time message passing system. **SockJS** is implemented in many languages, primarily javascript to talk to servers in real time using its protocol, which tries to create a duplex bi-directional connectin between the **Client(browser)** and the **Server**. The server should also implement the **sockjs** protocol. Thus, using the **sockjs-tornado** library which exposes the **sockjs** protocol in **tornado** server.  It first tries to create a **Websocket**  connection, and if it fails then it fallbacks to other transport mechanisms, such as **ajax**, **long polling**, etc.

You can read more about **sockjs** `here <https://github.com/sockjs/sockjs-client>`_

---------------
Technical Specs
---------------

:sockjs-client:  Advance Websocket Javascript Client
:Tornado: async python web server
:sockjs-tornado: sockjs websocket server implementation for Tornado


         
------------
Installation
------------


Prerequisites
`````````````

1. python 2.7+
2. tornado
3. sockjs-tornado
4. sockjs-client


Install
```````

::
        
        pip install sockjsChat

If the above dependencies do not get installed by the above command, then use the below steps to install them one by one.

 **Step 1 - Install pip**
 
 Follow the below methods for installing pip. One of them may help you to install pip in your system.

 * **Method 1 -**  https://pip.pypa.io/en/stable/installing/
 * **Method 2 -** http://ask.xmodulo.com/install-pip-linux.html
 * **Method 3 -** If you installed python on MAC OS X via ``brew install python``, then pip is already installed along with python.


 **Step 2 - Install tornado**
 ::

        pip install tornado 
        

 **Step 3 - Install sockjs-tornado**
 ::

        pip install sockjs-tornado
 
------        
Usage
------

After having installed sockjsChat, just run the following command to use it :

* **Start Server**
  ::
          
          $ sockjsChat [options]



* **Options**
  
  :--port: Port number where the chat server will start

* **Example**
  ::

          $ sockjsChat --port=8765


* **Stop Server**
  
  Click ``Ctrl+C`` to stop the server.


----
TODO
----

1. Add Private Chat functionality.
2. Manage Presence Management, sent, delivered acknowledgements.
3. Message Persistence and delivery of messages to offline clients.
4. Add Blog post regarding this topic.
