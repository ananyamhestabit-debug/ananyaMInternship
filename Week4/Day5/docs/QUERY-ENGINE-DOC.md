# QUERY ENGINE DOCUMENTATION — DAY 3

## Overview

This document explains the dynamic query system implemented for the Product API.

The API supports filtering, sorting, pagination, soft deletion, and unified error handling.

Architecture follows:

Route → Controller → Service → Repository → Database

---

## Product API Endpoint

GET /products

This endpoint supports multiple dynamic query parameters.

---

## 1. Search (Regex Based)

Example:

/products?search=phone

- Performs case-insensitive search.
- Searches in:
  - name field
  - tags field
- Uses MongoDB regex with OR condition.

---

## 2. Price Filtering

Example:

/products?minPrice=100&maxPrice=500

- Filters products within a price range.
- Uses $gte and $lte operators.

---

## 3. Tags Filtering

Example:

/products?tags=apple,samsung

- Returns products that contain any of the specified tags.
- Uses $in operator.

---

## 4. Sorting

Example:

/products?sort=price:desc

Format:
field:order

Examples:
price:asc
price:desc

Default sorting:
createdAt descending.

---

## 5. Pagination

Example:

/products?page=1&limit=5

- page → page number
- limit → number of results per page
- Uses skip and limit strategy.

---

## 6. Soft Delete

DELETE /products/:id

- Does NOT remove document.
- Sets deletedAt timestamp.

Active products:
deletedAt = null

---

## 7. Include Deleted Records

/products?includeDeleted=true

- Returns both active and soft-deleted products.
- Default behavior excludes deleted records.

---

## 8. Error Handling Format

All errors follow unified structure:

{
  success: false,
  message,
  code,
  timestamp,
  path
}

Typed errors are implemented using custom AppError class.

---

## Conclusion

Day 3 implements a failure-safe, production-oriented query engine with strict separation of concerns and dynamic filtering capability.