// coords.js
// https://chromedevtools.github.io/devtools-protocol/

const CDP = require('chrome-remote-interface');

const random = (min, max) => Math.floor(Math.random() * (max - min)) + min;

// node coords.js '#oss-form'
// node coords.js '#oss-location'
async function getCoordsAlt(css_selector) {
  let client;
  try {
    // connect to endpoint
    client = await CDP();
    // extract domains
    const { Page, Runtime, DOM } = client;
    // enable events then start!
    await Promise.all([Page.enable(), Runtime.enable(), DOM.enable()]);

    const {root: {nodeId: documentNodeId}} = await DOM.getDocument();

    console.log(documentNodeId)

    const result = await DOM.querySelector({
        selector: css_selector,
        nodeId: documentNodeId,
    });

    console.log(result)

    const retval = await DOM.getBoxModel({"nodeId": result.nodeId});

    var box_model = retval.model;
    console.log(box_model)

    content_w = Math.abs(box_model["content"][2] - box_model["content"][0])
    center_x = box_model["content"][0] + random(content_w / 4.0, 3 * content_w / 4.0)

    content_h = Math.abs(box_model["content"][5] - box_model["content"][1])
    center_y = box_model["content"][1] + random(content_h / 4.0, 3 * content_h / 4.0)

    const coords = {"x": center_x, "y": center_y, "node_id": result.nodeId, "root_node": documentNodeId};
    console.log(JSON.stringify(coords))
    return coords;
  } catch (err) {
    console.error(err);
  } finally {
    if (client) {
      await client.close();
    }
  }
}


async function getCoords(css_selector) {
  let client;
  try {
    // connect to endpoint
    client = await CDP();
    // extract domains
    const { Page, Runtime, DOM } = client;
    // enable events then start!
    await Promise.all([Page.enable(), Runtime.enable(), DOM.enable()]);

    // get clientRect of links
    const result = await Runtime.evaluate({
      expression: `var targetCoordEl = document.querySelector('${css_selector}'); if (targetCoordEl) { JSON.stringify(targetCoordEl.getClientRects()); }`
    });

    // console.log(css_selector, result)

    // get offset screen positioning
    const screenPos = await Runtime.evaluate({
      expression: "JSON.stringify({offsetY: window.screen.height - window.innerHeight, offsetX: window.screen.width - window.innerWidth})"
    });

    let offset = JSON.parse(screenPos.result.value);
    let clientRect = null;

    try {
      clientRect = JSON.parse(result.result.value)["0"];
    } catch(err) {
      return null;
    }

    let retVal =  {
      x: offset.offsetX + clientRect.x,
      y: offset.offsetY + clientRect.y,
      width: clientRect.width,
      height: clientRect.height,
    };
    console.log(JSON.stringify(retVal));
    return retVal;
  } catch (err) {
    console.error(err);
  } finally {
    if (client) {
      await client.close();
    }
  }
}

getCoordsAlt(process.argv[2]);