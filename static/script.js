// connect to server
let socket = io("https://game-01.onrender.com");

// global variables
let room = null;
let username = null;

// init function (HTML se call hoga)
function init(r, u){
    room = r;
    username = u;

    socket.emit("join", {room: room, username: username});
}

// number set karna
function sendNumber(){
    let n = document.getElementById("num").value;

    socket.emit("choose_number", {
        room: room,
        user: username,
        number: n
    });

    document.getElementById("status").innerText = "Number Locked 🔒";
}

// guess karna
function guess(){
    let g = document.getElementById("guess").value;

    socket.emit("guess", {
        room: room,
        user: username,
        guess: g
    });
}

// server se result
socket.on("result", (data)=>{
    document.getElementById("status").innerText =
        data.msg + " than " + data.num;
});

// win
socket.on("win", (user)=>{
    document.getElementById("status").innerText =
        user + " WON 🎉";
});

// player join
socket.on("status", (msg)=>{
    document.getElementById("status").innerText = msg;
});

// game start
socket.on("start", ()=>{
    document.getElementById("status").innerText =
        "Game Started 🚀 Choose your number";
});

// dono players ready
socket.on("both_ready", ()=>{
    document.getElementById("status").innerText =
        "Both players ready 🔥 Start guessing";
});
