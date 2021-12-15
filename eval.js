// page_source.js
const CDP = require('chrome-remote-interface');

async function evalCommand(command) {
  let client;
  try {
    // connect to endpoint
    client = await CDP();
    // extract domains
    const { Page, Runtime, DOM } = client;
    // enable events then start!
    await Promise.all([Page.enable(), Runtime.enable(), DOM.enable()]);

    console.log(command)

    const evalRes = await Runtime.evaluate({expression: command});
    console.log(evalRes)
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

if (argLength === 3) {
  evalCommand(process.argv[2]);
}