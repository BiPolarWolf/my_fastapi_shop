# Руководство по тестированию FastAPI Shop в Postman

## Содержание
1. [Настройка окружения](#настройка-окружения)
2. [Тестирование Categories](#тестирование-categories)
3. [Тестирование Products](#тестирование-products)
4. [Тестирование Cart](#тестирование-cart)
5. [Автоматизация тестов](#автоматизация-тестов)

---

## Настройка окружения

### Создание Environment в Postman

1. Откройте Postman и перейдите в **Environments**
2. Нажмите **Create Environment**
3. Назовите его `FastAPI Shop Local`
4. Добавьте переменные:

| Variable | Initial Value | Current Value |
|----------|--------------|---------------|
| `base_url` | `http://localhost:8000` | `http://localhost:8000` |
| `api_url` | `{{base_url}}/api` | `{{base_url}}/api` |

5. Сохраните и активируйте окружение

---

## Тестирование Categories

### 1. Получить все категории

**Метод:** `GET`  
**URL:** `{{api_url}}/categories/`

**Ожидаемый результат (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "slug": "electronics"
  },
  {
    "id": 2,
    "name": "Clothing",
    "slug": "clothing"
  }
]
```

**Tests для Postman:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is an array", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});

pm.test("Categories have required fields", function () {
    const jsonData = pm.response.json();
    if (jsonData.length > 0) {
        pm.expect(jsonData[0]).to.have.property('id');
        pm.expect(jsonData[0]).to.have.property('name');
        pm.expect(jsonData[0]).to.have.property('slug');
    }
});
```

---

### 2. Получить категорию по ID

**Метод:** `GET`  
**URL:** `{{api_url}}/categories/1/`

**Ожидаемый результат (200 OK):**
```json
{
  "id": 1,
  "name": "Electronics",
  "slug": "electronics"
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has correct structure", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData).to.have.property('name');
    pm.expect(jsonData).to.have.property('slug');
});
```

**Тест на несуществующую категорию:**

**URL:** `{{api_url}}/categories/999/`

**Ожидаемый результат (404 NOT FOUND):**
```json
{
  "detail": "Category not found"
}
```

---

## Тестирование Products

### 1. Получить все продукты

**Метод:** `GET`  
**URL:** `{{api_url}}/products/`

**Ожидаемый результат (200 OK):**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Wireless Headphones",
      "description": "High-quality wireless headphones...",
      "price": 299.99,
      "category_id": 1,
      "category": {
        "id": 1,
        "name": "Electronics",
        "slug": "electronics"
      },
      "image_url": "https://images.unsplash.com/..."
    }
  ],
  "total": 13
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has products array and total", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('products');
    pm.expect(jsonData).to.have.property('total');
    pm.expect(jsonData.products).to.be.an('array');
});

pm.test("Products have category information", function () {
    const jsonData = pm.response.json();
    if (jsonData.products.length > 0) {
        const product = jsonData.products[0];
        pm.expect(product).to.have.property('category');
        pm.expect(product.category).to.have.property('id');
        pm.expect(product.category).to.have.property('name');
    }
});
```

---

### 2. Получить продукт по ID

**Метод:** `GET`  
**URL:** `{{api_url}}/products/1/`

**Ожидаемый результат (200 OK):**
```json
{
  "id": 1,
  "name": "Wireless Headphones",
  "description": "High-quality wireless headphones...",
  "price": 299.99,
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "Electronics",
    "slug": "electronics"
  },
  "image_url": "https://images.unsplash.com/..."
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Product has all required fields", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData).to.have.property('name');
    pm.expect(jsonData).to.have.property('price');
    pm.expect(jsonData).to.have.property('category');
});
```

---

### 3. Получить продукты по категории

**Метод:** `GET`  
**URL:** `{{api_url}}/products/category/1/`

**Ожидаемый результат (200 OK):**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Wireless Headphones",
      "category_id": 1,
      ...
    }
  ],
  "total": 5
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("All products belong to the same category", function () {
    const jsonData = pm.response.json();
    const categoryId = 1; // Замените на нужный ID
    
    jsonData.products.forEach(product => {
        pm.expect(product.category_id).to.equal(categoryId);
    });
});
```

---

## Тестирование Cart

### 1. Добавить товар в корзину

**Метод:** `POST`  
**URL:** `{{api_url}}/cart/add/`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "product_id": 1,
  "quantity": 2,
  "cart_data": {}
}
```

**Ожидаемый результат (200 OK):**
```json
{
  "cart": {
    "1": 2
  }
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Cart contains added product", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('cart');
    pm.expect(jsonData.cart).to.have.property('1');
    pm.expect(jsonData.cart['1']).to.equal(2);
});

// Сохраняем корзину для следующих тестов
pm.environment.set("cart_data", JSON.stringify(pm.response.json().cart));
```

---

### 2. Добавить еще один товар к существующему

**Метод:** `POST`  
**URL:** `{{api_url}}/cart/add/`

**Body (raw JSON):**
```json
{
  "product_id": 1,
  "quantity": 3,
  "cart_data": {
    "1": 2
  }
}
```

**Ожидаемый результат (200 OK):**
```json
{
  "cart": {
    "1": 5
  }
}
```

**Tests:**
```javascript
pm.test("Quantity increased correctly", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.cart['1']).to.equal(5);
});
```

---

### 3. Обновить количество товара

**Метод:** `POST`  
**URL:** `{{api_url}}/cart/update/`

**Body (raw JSON):**
```json
{
  "product_id": 1,
  "quantity": 10,
  "cart_data": {
    "1": 5
  }
}
```

**Ожидаемый результат (200 OK):**
```json
{
  "cart": {
    "1": 10
  }
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Quantity updated correctly", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.cart['1']).to.equal(10);
});
```

---

### 4. Удалить товар из корзины

**Метод:** `POST`  
**URL:** `{{api_url}}/cart/remove/`

**Body (raw JSON):**
```json
{
  "product_id": 1,
  "cart_data": {
    "1": 10
  }
}
```

**Ожидаемый результат (200 OK):**
```json
{
  "cart": {}
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Product removed from cart", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.cart).to.not.have.property('1');
});
```

---

### 5. Получить детали корзины

**Метод:** `POST`  
**URL:** `{{api_url}}/cart/`

**Body (raw JSON):**
```json
{
  "1": 2,
  "2": 1
}
```

**Ожидаемый результат (200 OK):**
```json
{
  "items": [
    {
      "product_id": 1,
      "name": "Wireless Headphones",
      "price": 299.99,
      "quantity": 2,
      "subtotal": 599.98,
      "image_url": "https://..."
    },
    {
      "product_id": 2,
      "name": "Smart Watch Pro",
      "price": 399.99,
      "quantity": 1,
      "subtotal": 399.99,
      "image_url": "https://..."
    }
  ],
  "total": 999.97,
  "items_count": 2
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Cart has items, total and items_count", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('items');
    pm.expect(jsonData).to.have.property('total');
    pm.expect(jsonData).to.have.property('items_count');
});

pm.test("Subtotals calculated correctly", function () {
    const jsonData = pm.response.json();
    jsonData.items.forEach(item => {
        const expectedSubtotal = item.price * item.quantity;
        pm.expect(item.subtotal).to.equal(expectedSubtotal);
    });
});

pm.test("Total price calculated correctly", function () {
    const jsonData = pm.response.json();
    const calculatedTotal = jsonData.items.reduce((sum, item) => sum + item.subtotal, 0);
    pm.expect(jsonData.total).to.be.closeTo(calculatedTotal, 0.01);
});
```

---

## Автоматизация тестов

### Создание Collection Runner

1. Создайте новую коллекцию `FastAPI Shop Tests`
2. Добавьте все запросы в следующем порядке:
   - Health Check
   - Get All Categories
   - Get All Products
   - Add to Cart
   - Get Cart Details
   - Update Cart
   - Remove from Cart

3. Запустите Collection Runner:
   - Нажмите на коллекцию → **Run**
   - Выберите окружение `FastAPI Shop Local`
   - Нажмите **Run FastAPI Shop Tests**

---

## Проверка здоровья API

### Health Check

**Метод:** `GET`  
**URL:** `{{base_url}}/health`

**Ожидаемый результат (200 OK):**
```json
{
  "status": "ok"
}
```

**Tests:**
```javascript
pm.test("API is healthy", function () {
    pm.response.to.have.status(200);
    const jsonData = pm.response.json();
    pm.expect(jsonData.status).to.equal("ok");
});
```

---

## Типичные ошибки и их коды

| Код | Описание | Когда возникает |
|-----|----------|------------------|
| 200 | OK | Успешный запрос |
| 404 | Not Found | Продукт/категория не найдены |
| 422 | Validation Error | Неверный формат данных |
| 500 | Internal Server Error | Ошибка сервера |

---

## Советы по тестированию

1. **Всегда проверяйте статус-код** перед проверкой данных
2. **Используйте переменные окружения** для ID продуктов и категорий
3. **Сохраняйте состояние корзины** между запросами
4. **Проверяйте математические расчеты** (subtotal, total)
5. **Тестируйте граничные случаи** (пустая корзина, несуществующие ID)
6. **Запускайте тесты последовательно** через Collection Runner

---

## Экспорт и импорт коллекции

### Экспорт:
1. Нажмите на коллекцию → **Export**
2. Выберите **Collection v2.1**
3. Сохраните JSON файл

### Импорт:
1. **Import** → **Choose Files**
2. Выберите сохраненный JSON файл
3. Коллекция готова к использованию

---

## Заключение

Это руководство покрывает все основные эндпоинты вашего API. Для более глубокого тестирования рекомендуется:

- Добавить тесты на ошибки валидации
- Проверить CORS headers
- Тестировать одновременные запросы
- Добавить нагрузочное тестирование

Удачного тестирования! 🚀
