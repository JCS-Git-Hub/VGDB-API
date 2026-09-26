const API_URL = "http://127.0.0.1:8000/api";

export const api = {
    async getCategories() {
        const response = await axios.get(
            `${API_URL}/categories`
        );

        return response.data;
    },

    async getGames(params = {}) {
        const response = await axios.get(
            `${API_URL}/games`,
            { params }
        );

        return response.data;
    },

    async createGame(game) {
        const response = await axios.post(
            `${API_URL}/games`,
            game
        );

        return response.data;
    },

    async deleteGame(id) {
        await axios.delete(
            `${API_URL}/games/${id}`
        );
    }
};