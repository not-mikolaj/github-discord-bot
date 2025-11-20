    const axios = require("axios");

const webhookUrl = process.env.DISCORD_WEBHOOK_URL;

const eventName = process.argv[2] || "unknown event";
const actor = process.argv[3] || "unknown user";

const message = `🔔 GitHub event: **${eventName}** triggered by **${actor}**`;

axios.post(webhookUrl, { content: message })
    .then(() => console.log("Message sent to Discord"))
    .catch((err) => console.error("Error:", err.response ? err.response.data : err.message));
