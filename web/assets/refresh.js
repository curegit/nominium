var updatetimer = null;

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
    const hrefs = [...div.children].map(e => e.getElementsByTagName("a")[0].href);
    for (let i = 0; i < newdiv.children.length; i++) {
      const href = newdiv.children[i].getElementsByTagName("a")[0].href;
      if (!hrefs.includes(href)) {
        incomings.push(newdiv.children[i]);
      }
    }
    div.prepend(...incomings);
  }
}

function update(callback, timeout = 10000) {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "./");
  xhr.responseType = "document";
  xhr.timeout = timeout;
  xhr.onload = event => {
    if (xhr.status === 200) {
      appenditems(xhr.response);
    }
    callback();
  };
  xhr.onerror = event => {
    callback();
  };
  xhr.ontimeout = event => {
    callback();
  };
  xhr.send();
}

function reschedule(enabled, delay) {
  if (updatetimer !== null) {
    clearTimeout(updatetimer);
    updatetimer = null;
  }
  if (enabled) {
    updatetimer = setTimeout(update, delay, setschedule);
  }
}

function setschedule() {
  const enabled = document.getElementById("auto-update-enabled").checked;
  const delay = +document.getElementById("auto-update-interval").value;
  reschedule(enabled, delay);
}

function initschedule() {
  setschedule();
}

initschedule();
