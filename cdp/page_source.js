// page_source.js
const CDP = require('chrome-remote-interface');

async function getPageSource() {
  let client;
  try {
    // connect to endpoint
    client = await CDP();
    // extract domains
    const { Page, Runtime, DOM } = client;
    // enable events then start!
    await Promise.all([Page.enable(), Runtime.enable(), DOM.enable()]);

    // get the page source
    const rootNode = await DOM.getDocument({ depth: -1 });
    const pageSource = await DOM.getOuterHTML({
      nodeId: rootNode.root.nodeId
    });
    return pageSource.outerHTML;
  } catch (err) {
      console.error(err);
  } finally {
    if (client) {
      await client.close();
    }
  }
}

getPageSource().then((pageSource) => {
  console.log(pageSource);
})