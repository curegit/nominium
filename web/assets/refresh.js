var t = document.getElementById("auto-update");
var s = document.getElementById("auto-update-interval");
var intid = null;
//t.checked = true;
//s.selectedIndex = 0;

function appenditems(newdocument) {
  const newdivs = newdocument.getElementsByClassName("items");
  if (!newdivs.length) return;
  const newdiv = newdivs[0];
  const divs = document.getElementsByClassName("nothing");
  if (divs.length) {
    const div = divs[0];
    div.insertAdjacentElement("beforebegin", newdiv);
    div.remove();
  } else {
    const divs = document.getElementsByClassName("items");
    if (!divs.length) return;
    const div = divs[0];
    const incomings = [];
    let hrefs = [...div.children].map(e => e.getElementsByTagName("a")[0].href);
    for (let i = 0; i < newdiv.children.length; i++) {
      let href = newdiv.children[i].getElementsByTagName("a")[0].href;
      if (!hrefs.includes(href)) {
        incomings.push(newdiv.children[i]);
      }
    }
    div.prepend(...incomings);
  }
}

function refresh() {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "./");
  xhr.responseType = "document";
  xhr.timeout = 10000;
  xhr.onload = event => {
    if (xhr.status === 200) {
      const doc = xhr.response;
      appenditems(doc);
    } else {
    }
  };
  xhr.onerror = event => {

  };
  xhr.ontimeout = event => {

  };
  xhr.send();
}

function sc(n) {
  refresh();
  setTimeout(sc, n * 1000, n);
}

n = 30;
setTimeout(sc, n * 1000, n);
