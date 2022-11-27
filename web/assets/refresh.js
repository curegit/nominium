(function () {
  let updatetimer = null;
  const checkbox = document.getElementById("auto-update-enabled");
  const select = document.getElementById("auto-update-interval");

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
    xhr.onload = () => {
      if (xhr.status === 200) {
        appenditems(xhr.response);
      }
      callback();
    };
    xhr.onerror = () => {
      callback();
    };
    xhr.ontimeout = () => {
      callback();
    };
    xhr.send();
  }

  function reschedule() {
    const enabled = checkbox.checked;
    const delaysec = +select.value;
    if (updatetimer !== null) {
      clearTimeout(updatetimer);
      updatetimer = null;
    }
    if (enabled) {
      updatetimer = setTimeout(update, delaysec * 1000, reschedule);
    }
  }

  function changeschedule() {
    reschedule();
    try {
      const enabled = checkbox.checked;
      const delaysec = +select.value;
      localStorage.setItem("auto-update-enabled", enabled ? 1 : 0);
      localStorage.setItem("auto-update-interval", delaysec);
    } catch {

    }
  }

  checkbox.addEventListener("change", changeschedule);
  select.addEventListener("change", changeschedule);

  try {
    const autoupdate = localStorage.getItem("auto-update-enabled");
    if (autoupdate !== null) {
      checkbox.checked = +autoupdate ? true : false;
    }
    const updateinterval = localStorage.getItem("auto-update-interval");
    if (updateinterval !== null) {
      select.value = +updateinterval;
    }
  } catch {

  }
  reschedule();
})();
