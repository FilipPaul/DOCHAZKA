var slider = document.getElementById("myRange");
var output = document.getElementById("slider_value");
var button = document.getElementById("SENDbutton");
var cmdline = document.getElementById("cmdLine");
var date_time = document.getElementById("RTC_time_value")
var sync_button = document.getElementById("RTC_button");

output.innerHTML = slider.value; // Display the default slider value
var a = new Audio("http://" + location.hostname + "/sound");
var my_IP;
var my_Number;
var list = document.getElementById("dynList");
var port = 1337;

var url = 'ws://' + location.hostname + ':' + port;
MywebSocket = new WebSocket(url);


sync_button.onclick = function(){
  var today = new Date();
  var date = today.getFullYear()+'*'+(today.getMonth()+1)+'*'+today.getDate()+"*";
  date = date+today.getHours()+"*"+today.getMinutes()+"*"+today.getSeconds()+"*";
  console.log(date)
  MywebSocket.send("SETTIME*"+date);
}

function isOpen(ws) { return ws.readyState === ws.OPEN }

function IsJsonString(str) {
  try {
      JSON.parse(str);
  } catch (e) {
      return false;
  }
  return true;
}
function lowerCaseAllWordsExceptFirstLetters(string) {
  return string.replace(/\S*/g, function (word) {
      return word.charAt(0) + word.slice(1).toLowerCase();
  });
}

function update_MAIN(JSON_OBJECT){
  console.log("UPDATING MAIN PAGE:");
  list = document.getElementById("dynList");
  obj = JSON.parse(JSON_OBJECT);
  var length_of_list = list.children.length
  for (let index = 0; index < length_of_list-1; index++) {
    list.removeChild(list.lastChild);
  }

  
  //list.removeChild(list.lastChild());

  for (let index = 0; index < obj.employees.length; index++) {
    let a_link = document.createElement("a");
    let p_date_time = document.createElement("p");
    let p_val = document.createElement("p");
    a_link.setAttribute('href', "http://" + location.hostname + "/" + obj.employees[index].first_name + "_"+ obj.employees[index].second_name + ".txt");
    a_link.setAttribute("class","dynlist__links");
    a_link.setAttribute("id","created");
  
    //console.log(a_link);
    p_date_time.className = "dynlist__status";
    p_date_time.innerText = obj.employees[index].date_time;

    if (obj.employees[index].state == "Prichod"){
      p_val.className = "dynlist__value_green";
    }
    else if(obj.employees[index].state == "Obed"){
      p_val.className = "dynlist__value";
    }
    else{
      p_val.className = "dynlist__value_red";
    }
    
    p_val.innerText = obj.employees[index].state;

    //li.innerText = item;
    let li = document.createElement("li");
    li.className = "dynlist__item";
    a_link.text = obj.employees[index].first_name + " " + obj.employees[index].second_name;
    //li.innerText = data[index];
    a_link.innerText = obj.employees[index].first_name + " " + obj.employees[index].second_name;
    li.appendChild(a_link);
    li.appendChild(p_date_time);
    li.appendChild(p_val);
   // console.log(li);
    list.appendChild(li);
  }

  slider.value = obj.slider.value;
  output.innerHTML = obj.slider.value;
  date_time.innerText = obj.date_time.date + " " + obj.date_time.time;
}


MywebSocket.onopen = function (event) {
  console.log("Succesfully connected to WEBSOCKET");
}

MywebSocket.onmessage = function (event) {
  console.log("FROM SERVER: command: ["+event.data+"]")
  if(IsJsonString(event.data))
  {
    update_MAIN(event.data);
  }
  else{
    const cmd_array = event.data.split("*");
    if (cmd_array[0] == "SLIDERVALUE"){
      if(cmd_array[2] != my_Number){
      slider.value = cmd_array[1];
      output.innerHTML = cmd_array[1];
      }

    }
    else if (cmd_array[0] == "IP"){
      my_IP = cmd_array[1];
      }

    else if (cmd_array[0] == "CLIENT_NUMBER"){
      my_Number = cmd_array[1];
    }

    else if (cmd_array[0] == "CURRENT_TIME"){
      date_time.innerText= cmd_array[1];
    }

    else if (cmd_array[0] == "SOUND"){
      a.pause();
      a = new Audio("http://" + location.hostname + "/sound");
      a.play();
    }
};


MywebSocket.onclose = function (event) {
  console.log("CLOSING WEBSOCKET connection");
  MywebSocket.close();
};

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  if (!isOpen(MywebSocket)){
    console.log("Cannot open the webserver, refreshing page");
    location.reload();
    return;
  } 
  output.innerHTML = this.value;
  console.log("TO SERVER ["+ "SLIDER*" + this.value + "*"+"]")
  MywebSocket.send("SLIDER*" + this.value + "*");
};

button.onclick = function(){

  if (!isOpen(MywebSocket)){
    console.log("Cannot open the webserver, refreshing page");
    location.reload();
    return;
  } 
  MywebSocket.send(cmdline.value);
}
};
