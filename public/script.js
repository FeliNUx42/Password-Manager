const btnSubmit = document.getElementById("submit");
const btnMode = document.getElementById("mode");
const btnCopy = document.getElementById("copy");
const btnClear = document.getElementById("clear");
const rawResult = document.getElementById("raw");
const inputField = document.getElementById("input-field");
const inpDb = document.getElementById("db");
const inpDbPwd = document.getElementById("db_pwd");

const Parameter = {
  read: [
    { text: "Wesite: ", type: "text", id:"website" }
  ],
  add: [
    { text: "Wesite: " , type: "text", id: "website" },
    { text: "Username: ", type: "text", id: "user" },
    { text: "Password: ", type: "password", id: "pwd" },
    { text: "Repeate Password: ", type: "password", id: "rpwd" }
  ],
  addrandom: [
    { text: "Wesite: " , type: "text", id: "website" },
    { text: "Username: ", type: "text", id: "user" },
    { text: "Length (8-64): ", type: "number", id: "length", min: "8", max: "64"}
  ],
  updateuser: [
    { text: "Wesite: " , type: "text", id: "website" },
    { text: "Username: ", type: "text", id: "user" }
  ],
  updatepwd: [
    { text: "Wesite: " , type: "text", id: "website" },
    { text: "New Password: ", type: "password", id: "pwd" },
    { text: "Repeate new Pwd: ", type: "password", id: "rpwd" }
  ],
  delete: [
    { text: "Website: ", type: "text", id: "website"}
  ],
  readall: [ ]
}

btnSubmit.onclick = () => {
  console.log("submit");

  let page = btnMode.value;

  url = `http://localhost:5000/${page}`;

  let param = getParam();
  if (!param) return;

  let req = new XMLHttpRequest();

  req.onreadystatechange = () => {
    if (req.readyState == 4 && req.status == 200) {
      drawData(req.responseText);
    }
  }

  req.open("POST", url, true)
  req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  req.send(param);
}

btnMode.onchange = createParam = () => {
  console.log("change mode");

  inputField.innerHTML = "<h2>Parameter</h2>"

  Parameter[btnMode.value].forEach(elem => {
    let div = document.createElement("div");
    let inp = document.createElement("input");

    div.classList.add("inp");
    div.innerHTML = `<span>${elem.text}</span>`;
    
    Object.keys(elem).forEach(attr => {
      if (attr != "text") inp[attr] = elem[attr];
    });

    div.appendChild(inp);
    inputField.appendChild(div);

  });
}

btnCopy.onclick = () => {
  console.log("copy");

  if (rawResult.innerHTML == "Result...") return;

  navigator.clipboard.writeText(rawResult.innerHTML);
}

btnClear.onclick = () => {
  console.log("clear");

  rawResult.innerHTML = "Result...";
}

getParam = () => {
  let obj = {};
  let ret = "";

  Parameter[btnMode.value].forEach(elem => {
    obj[elem.id] = String(document.getElementById(elem.id).value);
  });

  obj.db = inpDb.value;
  obj.db_pwd = inpDbPwd.value;

  if (obj.pwd != obj.rpwd) {
    rawResult.innerHTML = "Passwords are not the same!";
    return;
  }
  delete obj.rpwd;

  Object.keys(obj).forEach(key => {
    ret += `&${key.replaceAll("=", "%3D").replaceAll("&", "%26")}=${obj[key].replaceAll("=", "%3D").replaceAll("&", "%26")}`; 
  });

  return encodeURI(ret.substring(1));
}

drawData = (data) => {
  data = JSON.parse(data);
  
  if (!data.data) {
    rawResult.innerHTML = data.error;
  } else if (typeof data.data == "string") {
    rawResult.innerHTML = data.data;
  } else if (data.data.length > 1) {
    rawResult.innerHTML = data.data.map(arr => arr.join(" - ")).join("<br>");
  } else {
    rawResult.innerHTML = data.data[0][2];
  }
}

createParam();