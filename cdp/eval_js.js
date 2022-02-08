// eval_js.js
// caller has to write command to /tmp/evalCommand.txt'
const CDP = require('chrome-remote-interface');
const fs = require('fs');

async function evalCommand(command) {
  let client;
  try {
    // connect to endpoint
    client = await CDP();
    // extract domains
    const { Page, Runtime, DOM } = client;
    // enable events then start!
    await Promise.all([Page.enable(), Runtime.enable(), DOM.enable()]);

    const evalRes = await Runtime.evaluate({expression: command});
    console.log(evalRes.result.value);

  } catch (err) {
      console.error(err);
  } finally {
    if (client) {
      await client.close();
    }
  }
}

const argLength = process.argv.length;

if (argLength === 2) {
  evalCommand(fs.readFileSync('/tmp/evalCommand.txt').toString());
}