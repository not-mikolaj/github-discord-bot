const fs = require('fs');
const axios = require("axios");

const eventPath = process.env.GITHUB_EVENT_PATH;
const event = JSON.parse(fs.readFileSync(eventPath, 'utf8'));

async function sendToDiscord(message) {
    await axios.post(process.env.DISCORD_WEBHOOK_URL, {
        content: message
    });
}

(async () => {
    await sendToDiscord(`Event: ${process.env.GITHUB_EVENT_NAME}`);
})();