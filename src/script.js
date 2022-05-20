function openTab(evt, tabName) {
  let tabcontent = document.getElementsByClassName("tabcontent");
  for (let i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  let tablinks = document.getElementsByClassName("tablinks");
  for (let i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

document.getElementById('transitions').style.display = "block";

let choice = config;

let TOGGLE = true;
let RANDOM = false;
let TINT = false;
let HUGE_TINT = false;
let W = 640
let H = 480
let f = 0
let i = 0
let images_array = []
let from = choice.from;
let to = choice.to;
let frame_cnt = to - from;

let frame_id = document.getElementById('frame');
let transitions = [];
let transitions_container = document.getElementById('transitionsContainer')
let file_name = choice['filename'] + '.txt';
let img_file_name = choice['filename'] + '.png';

document.getElementById("transitionMatrix").src = img_file_name;

let similarityMatricesName =  choice['filename'] + '/0_';
similarityMatricesName += to < 100 ? to : 100;
similarityMatricesName += '.png';
document.getElementById("similarityMatrices").src = similarityMatricesName;

let SpeedElement = document.getElementById("speed")
let SpeedValue = document.getElementById("speedValue");
let speed = 50;
let speedVal = 4;
SpeedValue.innerHTML = speed;
const MAX_SPEED = 20;
const MIN_SPEED = 1;

SpeedElement.oninput = function() {
  speed = this.value;
  SpeedValue.innerHTML = speed;
  speedVal =  Math.floor(map(speed, 0, 100, MIN_SPEED, MAX_SPEED));
  speedVal = MAX_SPEED - speedVal + MIN_SPEED;
}

let ProbabilityElement = document.getElementById("probability")
let ProbabilityValue = document.getElementById("probabilityValue");
let probability = 0;
let probabilityVal = 0;
ProbabilityValue.innerHTML = probability;

ProbabilityElement.oninput = function() {
  probability = this.value;
  ProbabilityValue.innerHTML = probability;
  probabilityVal =  map(probability, 0, 100, 0, 1);
}

let Tint = document.getElementById("Tint")
let HugeTint = document.getElementById("HugeTint")
let NoTint = document.getElementById("NoTint")

Tint.onclick = (e=>{ TINT = true; HUGE_TINT = false; })
HugeTint.onclick = (e=>{ TINT = false; HUGE_TINT = true; })
NoTint.onclick = (e=>{ TINT = false; HUGE_TINT = false; })

function readTextFile(file) {
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", file, false);
  rawFile.onreadystatechange = function () {
    if(rawFile.readyState === 4) {
      if(rawFile.status === 200 || rawFile.status == 0) {
      var allText = rawFile.responseText.split("\n")

      // slicing means not taking all frames from folder
      if(choice.slice) allText = allText.slice(from, to)

      // loop list of transitions
      allText.forEach((t,i) => {

        // appending to list
        let li = document.createElement('li')
        li.innerHTML = i + ":\t";
        li.id = i;
        transitions_container.appendChild(li)

        // loop transitions
        t = t.slice(1, t.length - 1)
        if(!t) {
          transitions.push([])
        } else {
          transitions.push(

            (choice.slice) ?
              t.split(",")
              .map(x => { return (x >= from && x <= to) ?  x - from : undefined})
              .filter(x => x !== undefined)
            :
              t.split(",")
              .map(x => { return parseInt(x) })
            );

            transitions[i].forEach(e => {
              if(e)
                li.innerHTML += e + " "
            });
          }
        });
      }
    }
  }
  rawFile.send(null);
}

readTextFile(file_name);

function preload() {
  // load images
  for(let i = from; i < to; i++){
    let id = i;
    if (id < 10) { id = '000' + id;
    } else if (id < 100) { id = '00' + id;
    } else if (id < 1000) { id = '0' + id; }
    let image_name = choice['folder'] +"/" + id + "." + choice['extension'];
    images_array.push(loadImage(image_name));
  }
}

let previousLi;
function setup() {
  W = images_array[0].width;
  if(W > 400) {
    W = 400;
    H = images_array[0].height * 400 / images_array[0].width;
  } else {
    H = images_array[0].height > 400 ? 400 : images_array[0].height ;
  }

  let canvas = createCanvas(W, H);
  canvas.parent("canvasContainer");
  document.getElementById("Loading").style.display = "none";
  previousLi = document.getElementById("0");
}

function draw() {
  // video is playing based on frame count and given speed
  if(frameCount % speedVal == 0) {
    let len = transitions[i].length;

    // increment frame based on probability,
    // or if there is no jump alternative in list
    if(Math.random() > probabilityVal || len == 0) {
      tint(255, 255); // reset cross-fade
      i++;
      i %= frame_cnt

    // jump to random frame from list
    } else  {
      if(TINT)           { tint(255, 67);  }
      else if(HUGE_TINT) { tint(255, 27);  }
      else               { tint(255, 255); }
      i = transitions[i][Math.floor(Math.random() * len)];
    }

    // drawing loop is still running and 'i' is defined on user input
    // that can cause 'i' to be undefined for short time
    if(i != undefined) {

      // color current frame
      frame_id.innerHTML = i;
      li = document.getElementById(i);
      previousLi. style.backgroundColor = 'white';
      li. style.backgroundColor = 'cyan';
      previousLi = li;

      // draw image in center
      push();
      translate(W/2, H/2);
      if(images_array)
      if(images_array[0])
      image(images_array[i], -images_array[0].width/2, -images_array[0].height/2);
      pop();
    }
  }
}