var info=document.querySelector("#info")

info.onmouseover = function() {
  document.getElementById('popup').style.display = 'block';
}

info.onmouseout = function() {
  document.getElementById('popup').style.display = 'none';
}