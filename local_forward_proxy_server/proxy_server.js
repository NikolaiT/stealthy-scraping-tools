const ProxyChain = require('proxy-chain');

async function startProxyServer(proxy) {
  return new Promise(function(resolve, reject) {
    const server = new ProxyChain.Server({
      // Port where the server will listen. By default 8947.
      port: 8947,
      // Enables verbose logging
      verbose: false,
      prepareRequestFunction: function (params) {
        var {request, username, password, hostname, port, isHttp, connectionId} = params;
        console.log('isHttp: ' + isHttp);
        console.log('port: ' + port);
        console.log('hostname: ' + hostname);
        console.log('headers: ' + JSON.stringify(request.headers));
        return {
          requestAuthentication: false,
          // http://username:password@proxy.example.com:3128
          upstreamProxyUrl: proxy,
        };
      },
    });

    // Emitted when HTTP connection is closed
    server.on('connectionClosed', (params) => {
      var {connectionId, stats} = params;
      console.log(`Connection ${connectionId} closed`);
    });

    // Emitted when HTTP request fails
    server.on('requestFailed', (params) => {
      var {request, error} = params;
      console.error(`Request ${request.url} failed`);
      console.error(error);
    });

    server.listen(() => {
      console.log(`ProxyServer listening on port ${server.port}`);
      resolve(server);
    });
  });
}


// Start local forwarding server with: node proxy_server.js http://username:password@proxy.example.com:3128
// Use the local forwarding proxy server with google-chrome:
// google-chrome --proxy-server="localhost:8947"

if (process.argv.length === 3) {
  (async () => {
    await startProxyServer(process.argv[2]);
  })();
}
