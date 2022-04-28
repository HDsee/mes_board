const main = document.querySelector('main');
const sendBtn = document.getElementById('send-btn')

function render(message, imageUrl){ 
    let messageText = document.createTextNode(message);
    let messageDiv = document.createElement('div');
    messageDiv.setAttribute('class', 'message-css')
    messageDiv.appendChild(messageText);
    let image = document.createElement('img');
    image.setAttribute('src', imageUrl)
    image.setAttribute('class', 'image-css')
    let hr = document.createElement('hr');
    main.appendChild(messageDiv);
    main.appendChild(image)
    main.appendChild(hr)
}

window.addEventListener('load', () => { 
    fetch("/api/message", {
        method:"GET"
    })
    .then(res => res.json())
    .then((data) => {
        console.log(data);
        data.data.forEach( data => render(data.message, data.image) );
    })
})

let messageData = new FormData();
let image = "";
const file = document.getElementById('select-file');
file.addEventListener('change', (e) => {
    image = e.target.files[0];
});   

sendBtn.addEventListener('click', () => {
    const message = document.getElementById('message-content').value
    if(message !== "" && image !== ""){
        console.log(image);
        messageData.append('message', message);
        messageData.append('file', image);
        
        fetch("/api/message", {
            method:"POST",
            body: messageData
        })
        .then(res => res.json())
        .then(data => {
                console.log(data);
                document.getElementById('message-content').value = "";
                document.getElementById('select-file').value = "";
                window.location.reload()
        })
        .catch( error => console.log('錯誤', error) )
    }else{
        alert("輸入留言或選擇圖片");
    }
})
