import { api } from "./api.js";
import { dom } from "./dom.js";
import { ui } from "./ui.js";
import { categoryUI } from "./category-ui.js";
import { gameUI } from "./game-ui.js";

export const app = {
    games: [],
    editingGameId: null,

    async loadCategories() {
        try {
            const categories = await api.getCategories();

            categoryUI.renderSelectOptions(categories);
        } catch (error) {
            ui.showMessage(
                "No se pudieron cargar los géneros.",
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

            this.games = games;

            gameUI.renderGames(
                games,
                dom.gamesList
            );

            const count = games.length;
            const noun = count === 1
                ? "videojuego"
                : "videojuegos";

            const adjective = count === 1
                ? "encontrado"
                : "encontrados";

            ui.showMessage(
                `${count} ${noun} ${adjective}.`,
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

            category_id: Number(
                dom.categorySelect.value
            )
        };

        const isEditing =
            this.editingGameId !== null;

        try {
            if (isEditing) {
                await api.editGame(
                    this.editingGameId,
                    game
                );

                ui.showMessage(
                    "Videojuego actualizado correctamente.",
                    "success"
                );
            } else {
                await api.createGame(game);

                ui.showMessage(
                    "Videojuego creado correctamente.",
                    "success"
                );
            }

            this.editingGameId = null;

            dom.gameForm.reset();

            this.updateSubmitButton();

            await this.loadGames();
        } catch (error) {
            this.handleError(
                error,
                isEditing
                    ? "No se pudo actualizar el videojuego."
                    : "No se pudo crear el videojuego."
            );
        }
    },

    async handleEditGame(id) {
        const game = this.games.find(
            game => String(game.id) === String(id)
        );

        if (!game) {
            ui.showMessage(
                "No se encontró el videojuego.",
                "error"
            );

            return;
        }

        this.editingGameId = game.id;

        dom.titleInput.value = game.title;
        dom.developerInput.value = game.developer;
        dom.releaseYearInput.value = game.release_year;

        dom.categorySelect.value =
            game.category_id ?? game.category?.id ?? "";

        this.updateSubmitButton();

        dom.titleInput.focus();
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

    cancelEdit() {
        this.editingGameId = null;

        dom.gameForm.reset();

        this.updateSubmitButton();
    },

    updateSubmitButton() {
        const isEditing =
            this.editingGameId !== null;

        const submitButton =
            dom.gameForm.querySelector(
                'button[type="submit"]'
            );

        const cancelButton =
            dom.gameForm.querySelector(
                '[data-action="cancel-edit"]'
            );

        const formTitle = document.querySelector(
            "#game-form-title"
        );

        if (formTitle) {
            formTitle.textContent = isEditing
                ? "Editar videojuego"
                : "Añadir videojuego";
        }

        if (submitButton) {
            submitButton.textContent = isEditing
                ? "Guardar cambios"
                : "Guardar videojuego";
        }

        if (cancelButton) {
            cancelButton.hidden = !isEditing;
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

    const cancelButton =
        dom.gameForm.querySelector(
            '[data-action="cancel-edit"]'
        );

    if (cancelButton) {
        cancelButton.addEventListener(
            "click",
            () => app.cancelEdit()
        );
    }

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
                "button[data-action]"
            );

            if (!button) {
                return;
            }

            const gameId = button.dataset.gameId;
            const action = button.dataset.action;

            if (action === "edit") {
                app.handleEditGame(gameId);
            }

            if (action === "delete") {
                app.handleDeleteGame(gameId);
            }
        }
    );
}

export async function initializeApp() {
    registerEvents();

    await app.loadCategories();
    await app.loadGames();
}