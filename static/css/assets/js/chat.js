const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
let messages = [];
let history = [];

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "Mixtral-8x7B";
const PERSON_NAME = "You";

msgerForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
  messages.push({
    'text': msgText,
    'user': true
  })
    
  botResponse(msgText);
});

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse(userInput) {
  let r = "";
  const apiEndpoint = "http://127.0.0.1:5000/generate_text";

  const data = {
    user_message: userInput,
    chatbot: Object.values(messages),
    history: history,
  };

  fetch(apiEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // Specify the content type as JSON
    },
    body: JSON.stringify(data), // Stringify the data object
  })
    .then((response) => response.json())
    .then((responseData) => {
      // Handle the response here
      console.log(responseData);
      history = responseData[1]
      r = responseData[1][responseData[1].length - 1];
      messages.push(
        {
            'text': r,
            'user': false,
        }
      )

      appendMessage(BOT_NAME, BOT_IMG, "left", r);
    })
    .catch((error) => {
      // Handle errors here
      console.error("Error:", error);
    });

}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
