const API_URL = "http://127.0.0.1:5000/api/products";

// ✅ Добавление продукта
document.getElementById("addProductForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const productData = {
        name: document.getElementById("productName").value,
        price: parseFloat(document.getElementById("productPrice").value),
        description: document.getElementById("productDescription").value,
        category: document.getElementById("productCategory").value,
        stock: parseInt(document.getElementById("productStock").value)
    };

    console.log("Sending product data:", productData);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(productData)
        });

        if (!response.ok) throw new Error("Failed to add product");

        alert("Product added successfully!");
        await fetchProducts(); // ✅ Добавлен `await` для обновления списка
    } catch (error) {
        console.error("Error adding product:", error);
        alert("Error adding product.");
    }
});

// ✅ Получение списка продуктов
async function fetchProducts() {
    console.log("Fetching products...");
    
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Failed to fetch products");

        const products = await response.json();
        console.log("Products received:", products);

        const productList = document.getElementById("productList");
        productList.innerHTML = "";

        products.forEach(product => {
            const li = document.createElement("li");
            li.innerHTML = `
                ${product.name} - $${product.price} 
                <button onclick="deleteProduct('${product._id}')">❌</button>
            `;
            productList.appendChild(li);
        });

    } catch (error) {
        console.error("Error fetching products:", error);
        alert("Error fetching products.");
    }
}

// ✅ Удаление продукта
async function deleteProduct(productId) {
    console.log(`Deleting product: ${productId}`);

    try {
        const response = await fetch(`${API_URL}/${productId}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error("Failed to delete product");

        alert("Product deleted!");
        await fetchProducts(); // ✅ Добавлен `await`
    } catch (error) {
        console.error("Error deleting product:", error);
        alert("Error deleting product.");
    }
}

// ✅ Загрузить продукты при старте
fetchProducts();
