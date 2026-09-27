import { dom } from "./dom.js";

export const categoryUI = {
    renderSelectOptions(categories) {
        dom.categorySelect.innerHTML = `
            <option value="">
                Selecciona un género
            </option>
        `;

        dom.filterCategory.innerHTML = `
            <option value="">
                Todos los géneros
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