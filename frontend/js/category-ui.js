import { dom } from "./dom.js";

export const categoryUI = {
    renderSelectOptions(categories) {
        dom.categorySelect.innerHTML = `
            <option value="">
                Selecciona una categoría
            </option>
        `;

        dom.filterCategory.innerHTML = `
            <option value="">
                Todas las categorías
            </option>
        `;

        categories.forEach(category => {
            const categoryOption =
                document.createElement("option");

            categoryOption.value = category.id;
            categoryOption.textContent = category.name;

            const filterOption =
                categoryOption.cloneNode(true);

            dom.categorySelect.appendChild(
                categoryOption
            );

            dom.filterCategory.appendChild(
                filterOption
            );
        });
    }
};