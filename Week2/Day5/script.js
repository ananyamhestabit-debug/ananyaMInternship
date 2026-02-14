let allProducts=[];
const box=document.getElementById("productBox");
const searchInput=document.getElementById("searchInput");
const sortSelect=document.getElementById("sortSelect");

fetch("https://dummyjson.com/products")
.then(function(res){return res.json();})
.then(function(data){
allProducts=data.products;
showProducts(allProducts);
});

function showProducts(products){
box.innerHTML="";
products.forEach(function(product,index){

const card=document.createElement("div");
card.className="card";

const img=document.createElement("img");
img.src=product.thumbnail;

const title=document.createElement("h3");
title.textContent=product.title;

const price=document.createElement("p");
price.className="price";
price.textContent="$ "+product.price;

const iconBox=document.createElement("div");
iconBox.className="hoverIcons";

const cart=document.createElement("div");
cart.className="icon";
cart.textContent="🛒";

const wishlist=document.createElement("div");
wishlist.className="icon";
wishlist.textContent="⭐";

const view=document.createElement("div");
view.className="icon";
view.textContent="🔍";

iconBox.append(cart,wishlist,view);

if(index%3===0){
const tag=document.createElement("div");
tag.className="tag sale";
tag.textContent="SALE";
card.appendChild(tag);
}
else if(index%3===1){
const tag2=document.createElement("div");
tag2.className="tag out";
tag2.textContent="OUT OF STOCK";
card.appendChild(tag2);
}

card.append(img,iconBox,title,price);
box.appendChild(card);
});
}

searchInput.onkeyup=function(){
const text=searchInput.value.toLowerCase();
const filtered=allProducts.filter(function(p){
return p.title.toLowerCase().includes(text);
});
showProducts(filtered);
};

sortSelect.onchange=function(){
let value=sortSelect.value;
let sorted=[...allProducts];

if(value==="high"){
sorted.sort(function(a,b){return b.price-a.price;});
}

if(value==="low"){
sorted.sort(function(a,b){return a.price-b.price;});
}

showProducts(sorted);
};

document.querySelectorAll("nav li").forEach(function(item){
item.addEventListener("click",function(){
document.querySelectorAll("nav li").forEach(function(li){
li.classList.remove("active");
});
this.classList.add("active");
});
});
