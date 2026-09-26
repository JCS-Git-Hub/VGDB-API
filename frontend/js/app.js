import { api } from "./api.js";
import { dom } from "./dom.js";
import { ui } from "./ui.js";
import { categoryUI } from "./category-ui.js";
import { gameUI } from "./game-ui.js";

export const app = {
    async loadCategories() {
        try {
            const categories = await api.getCategories();

            categoryUI.renderSelectOptions(categories);
        } catch (error) {
            ui.showMessage(
                "No se pudieron cargar las categorías.",
                "error"
            );
        }
    },

    async loadGames() {
        try {
            ui.showMessage(
                "Cargando videojuegos...",
                "loading"
            );

            const params = {
                search: dom.searchInput.value.trim(),
                category_id: (
                    dom.filterCategory.value || undefined
                ),
                skip: 0,
                limit: 10
            };

            const games = await api.getGames(params);

            gameUI.renderGames(
                games,
                dom.gamesList
            );

            ui.showMessage(
                `${games.length} videojuegos cargados.`,
                "success"
            );
        } catch (error) {
            this.handleError(
                error,
                "No se pudieron cargar los videojuegos."
            );
        }
    },

    async handleGameSubmit(event) {
        event.preventDefault();

        const game = {
            title: dom.titleInput.value.trim(),
            developer: dom.developerInput.value.trim(),
            release_year: Number(
                dom.releaseYearInput.value
            ),
            price: Number(
                dom.priceInput.value
            ),
            category_id: Number(
                dom.categorySelect.value
            )
        };

        try {
            await api.createGame(game);

            dom.gameForm.reset();

            ui.showMessage(
                "Videojuego creado correctamente.",
                "success"
            );

            await this.loadGames();
        } catch (error) {
            this.handleError(
                error,
                "No se pudo crear el videojuego."
            );
        }
    },

    async handleDeleteGame(id) {
        const confirmed = window.confirm(
            "¿Quieres eliminar este videojuego?"
        );

        if (!confirmed) {
            return;
        }

        try {
            await api.deleteGame(id);

            ui.showMessage(
                "Videojuego eliminado correctamente.",
                "success"
            );

            await this.loadGames();
        } catch (error) {
            this.handleError(
                error,
                "No se pudo eliminar el videojuego."
            );
        }
    },

    handleError(error, defaultMessage) {
        const detail = error.response?.data?.detail;

        ui.showMessage(
            detail || defaultMessage,
            "error"
        );
    }
};

export function registerEvents() {
    dom.gameForm.addEventListener(
        "submit",
        event => app.handleGameSubmit(event)
    );

    dom.searchInput.addEventListener(
        "input",
        () => app.loadGames()
    );

    dom.filterCategory.addEventListener(
        "change",
        () => app.loadGames()
    );

    dom.gamesList.addEventListener(
        "click",
        event => {
            const button = event.target.closest(
                '[data-action="delete"]'
            );

            if (!button) {
                return;
            }

            const gameId = button.dataset.gameId;

            app.handleDeleteGame(gameId);
        }
    );
}

export async function initializeApp() {
    registerEvents();

    await app.loadCategories();
    await app.loadGames();
}