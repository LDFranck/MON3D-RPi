function checkSSID() {
   var ssid = document.getElementById("ssid").value;
   var errorMessage = document.getElementById("error-message");

   if (ssid.trim() === "") {
       errorMessage.innerText = "Please enter a Wi-Fi SSID";
       return false;
   } else {
      errorMessage.innerText = "";
   }
}

function copyToClipboard(text) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
  
    var button = document.getElementById("copyButton");
    button.innerHTML = "Done!";
    button.disabled = true;
  
    setTimeout(function() {
      button.innerHTML = "Copy to Clipboard";
      button.disabled = false;
    }, 2000);
}
