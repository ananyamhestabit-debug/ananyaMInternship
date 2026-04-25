const express = require("express");
const router = express.Router();

const { validateProduct } = require("../middlewares/validate");
const productController = require("../controllers/product.controller");
const auth = require("../middlewares/auth.middleware");


router.post("/", auth, validateProduct, productController.createProduct);

router.get("/", auth, productController.getProducts);
router.delete("/:id", auth, productController.deleteProduct);

module.exports = router;