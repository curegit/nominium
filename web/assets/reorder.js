var dragsource = null;

function dragstart(event) {
  dragsource = event.currentTarget;
  event.dataTransfer.effectAllowed = "move";
  const children = dragsource.parentElement.children;
  for (let i = 0, above = true; i < children.length; i++) {
    if (children[i] === dragsource) {
      above = false;
      children[i].classList.remove("above", "below");
    } else {
      if (above) {
        children[i].classList.add("above");
        children[i].classList.remove("below");
      } else {
        children[i].classList.add("below");
        children[i].classList.remove("above");
      }
    }
  }
}

function dragend(event) {
  const children = event.currentTarget.parentElement.children;
  for (let i = 0; i < children.length; i++) {
    children[i].classList.remove("over", "above", "below");
  }
}

function dragover(event) {
  event.preventDefault();
  if (event.currentTarget !== dragsource) {
    event.dataTransfer.dropEffect = "move";
    event.currentTarget.classList.add("over");
  } else {
    event.dataTransfer.dropEffect = "none";
  }
}

function dragleave(event) {
  event.currentTarget.classList.remove("over");
}

function drop(event) {
  event.preventDefault();
  event.stopPropagation();
  const target = event.currentTarget;
  const parent = target.parentElement;
  const children = [...parent.children];
  for (let i = 0; i < children.length; i++) {
    if (children[i] === target) {
      if (children[i].classList.contains("above")) {
        parent.appendChild(dragsource);
        parent.appendChild(children[i]);
      } else if (children[i].classList.contains("below")) {
        parent.appendChild(children[i]);
        parent.appendChild(dragsource);
      } else {
        parent.appendChild(children[i]);
      }
    } else if (children[i] !== dragsource) {
      parent.appendChild(children[i]);
    }
  }
  for (let i = 0; i < children.length; i++) {
    children[i].classList.remove("over", "above", "below");
  }
}
