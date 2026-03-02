const express = require("express");
const router = express.Router();

const productController = require("../controllers/product.controller");
const { validateProduct } = require("../middlewares/validate");

router.post("/", validateProduct, productController.createProduct);
router.get("/", productController.getProducts);
router.delete("/:id", productController.deleteProduct);

module.exports = router;