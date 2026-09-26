export const gameUI = {
    renderGames(games, gamesList) {
        if (games.length === 0) {
            gamesList.innerHTML = `
                <p class="a-text">
                    No hay videojuegos disponibles.
                </p>
            `;

            return;
        }

        gamesList.innerHTML = games
            .map(game => this.createGameCard(game))
            .join("");
    },

    createGameCard(game) {
        return `
            <article class="m-game-card">
                <h3 class="m-game-card__title">
                    ${this.escapeHtml(game.title)}
                </h3>

                <p class="m-game-card__data">
                    <strong>Desarrolladora:</strong>
                    ${this.escapeHtml(game.developer)}
                </p>

                <p class="m-game-card__data">
                    <strong>Año:</strong>
                    ${game.release_year}
                </p>

                <p class="m-game-card__data">
                    <strong>Precio:</strong>
                    ${Number(game.price).toFixed(2)} €
                </p>

                <p class="m-game-card__data">
                    <strong>Categoría:</strong>
                    ${this.escapeHtml(game.category.name)}
                </p>

                <div class="m-game-card__actions">
                    <button
                        class="a-button a-button--danger"
                        data-action="delete"
                        data-game-id="${game.id}"
                    >
                        Eliminar
                    </button>
                </div>
            </article>
        `;
    },

    escapeHtml(value) {
        const element = document.createElement("div");

        element.textContent = value;

        return element.innerHTML;
    }
};