import json
import pprint

from behavior.sst_utils import *

parse_listings = """var res = [];
document.querySelectorAll(".result-list__listing").forEach((el) => {
let title = el.querySelector(".result-list-entry__brand-title");
let details = el.querySelector(".result-list-entry__criteria");

if (title) {
  let obj = {
    title: title.textContent,
    url: el.querySelector("a.result-list-entry__brand-title-container").getAttribute("href"),
  };
  if (details) {
    obj.price = details.querySelector("dl.grid-item:nth-child(1)").textContent;
    obj.area = details.querySelector("dl.grid-item:nth-child(2)").textContent;
    obj.rooms = details.querySelector("dl.grid-item:nth-child(3)").textContent;
  }
  res.push(obj);
}
});
JSON.stringify(res);"""

listings = eval_js(parse_listings)
pprint.pprint(json.loads(listings))
