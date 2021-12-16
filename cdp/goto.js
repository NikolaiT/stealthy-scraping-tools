// page_source.js
const CDP = require('chrome-remote-interface');

async function pageNav(url) {
  let client;
  try {
    // connect to endpoint
    client = await CDP();
    // extract domains
    const { Page, Runtime, DOM } = client;
    // enable events then start!
    await Promise.all([Page.enable(), Runtime.enable(), DOM.enable()]);

    // get the page source
    await Page.navigate({url: url});
    return 'ok';
  } catch (err) {
      console.error(err);
  } finally {
    if (client) {
      await client.close();
    }
  }
}

pageNav().then((res) => {
  console.log(res);
})