// coords.js
// https://chromedevtools.github.io/devtools-protocol/

const CDP = require('chrome-remote-interface');

const random = (min, max) => Math.floor(Math.random() * (max - min)) + min;

// given a selector or node_id returns x and y *relative* coordinates
// coordinates are relative to the viewport
// The x relative coordinate is the same as the absolute coordiante, as the browser is maximed
// The y coordinate is less, because the browser has the address bar / header
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

    // given a selector or node_id returns x and y *relative* coordinates
    // coordinates are relative to the viewport

    // The x relative coordinate is the same as the absolute coordiante, as the browser is maximed
    // The y coordinate is less, because the browser has the address bar / header

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

function getFrameExecId(frame) {
  var frameId = frameNameToFrameId[frame];
  if (!frameId)
      throw Error(`Frame ${frame} is unknown`);
  var execId = frameIdToContextId[frameId];
  if (!execId)
      throw Error(`Frame ${frame} (${frameId}) has no executionContextId`);
  return execId;
}

function expectLoadFrame(name, timeout) {
  return new Promise((resolve, reject) => {
      let tm = setTimeout( () => reject("timed out waiting for frame load"), timeout );

      // we can only have one Page.frameNavigated() handler, so let our handler above resolve this promise
      frameWaitName = name;
      new Promise((fwpResolve, fwpReject) => { frameWaitPromiseResolve = fwpResolve })
          .then(() => {
              // For the frame to be fully valid for queries, it also needs the corresponding
              // executionContextCreated() signal. This might happen before or after frameNavigated(), so wait in case
              // it happens afterwards.
             function pollExecId() {
                  if (frameIdToContextId[frameNameToFrameId[name]]) {
                      clearTimeout(tm);
                      resolve();
                  } else {
                      setTimeout(pollExecId, 100);
                  }
              }
              pollExecId();
          });
  });
}


async function getCoordsIframe(css_selector, iframe) {
  let client;
  try {
    // connect to endpoint
    client = await CDP();
    // extract domains
    const { Page, Runtime, DOM } = client;
    // enable events then start!
    await Promise.all([Page.enable(), Runtime.enable(), DOM.enable()]);

    var frameIdToContextId = {};
    var frameNameToFrameId = {};
    // set these to wait for a frame to be loaded
    var frameWaitName = null;
    var frameWaitPromiseResolve = null;

    // map frame names to frame IDs; root frame has no name, no need to track that
    await Page.frameNavigated(info => {
      if (info.frame.name)
          frameNameToFrameId[info.frame.name] = info.frame.id;

      // were we waiting for this frame to be loaded?
      if (frameWaitPromiseResolve && frameWaitName === info.frame.name) {
          frameWaitPromiseResolve();
          frameWaitPromiseResolve = null;
      }
    });

    // track execution contexts so that we can map between context and frame IDs
    await Runtime.executionContextCreated(info => {
      frameIdToContextId[info.context.auxData.frameId] = info.context.id;
    });

    await Runtime.executionContextDestroyed(info => {
      for (let frameId in frameIdToContextId) {
        if (frameIdToContextId[frameId] == info.executionContextId) {
            delete frameIdToContextId[frameId];
            break;
        }
      }
    });

    let result = null;
    let clientRectCmd = `var targetCoordEl = document.querySelector('${css_selector}'); if (targetCoordEl) { JSON.stringify(targetCoordEl.getClientRects()); }`;

    await expectLoadFrame(iframe, 2000).then(async (res) => {
      let frameId = getFrameExecId(iframe);
      result = await Runtime.evaluate({
        expression: clientRectCmd,
        contextId: frameId,
      });
      console.log(result)
    });

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

async function getCoords(css_selector) {
  let client;
  try {
    // connect to endpoint
    client = await CDP();
    // extract domains
    const { Page, Runtime, DOM } = client;
    // enable events then start!
    await Promise.all([Runtime.enable()]);

    let result = null;
    let clientRectCmd = `var targetCoordEl = document.querySelector('${css_selector}'); if (targetCoordEl) { JSON.stringify(targetCoordEl.getClientRects()); }`;

    result = await Runtime.evaluate({
      expression: clientRectCmd,
    });

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

const argLength = process.argv.length;

if (argLength === 3) {
  getCoords(process.argv[2]);
} else if (argLength === 4) {
  getCoordsIframe(process.argv[2], process.argv[3]);
}
