import { dom } from "./dom.js";

export const ui = {
    showMessage(text, type = "") {
        dom.message.textContent = text;

        dom.message.className = type
            ? `a-message a-message--${type}`
            : "a-message";
    },

    clearMessage() {
        dom.message.textContent = "";
        dom.message.className = "a-message";
    }
};