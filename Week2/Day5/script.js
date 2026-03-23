let allProducts=[]; //to store api data
const box=document.getElementById("productBox");
const searchInput=document.getElementById("searchInput");
const sortSelect=document.getElementById("sortSelect");


// api(server) ->data aya-> allProducts me store hua-> ui bna
fetch("https://dummyjson.com/products").then(function(res){return res.json();}) //res=server's raw response and res.json()->data object bna and  data=json converted response 
.then(function(data){
allProducts=data.products; //allProducts has the whole product array from json response (object properties)
showProducts(allProducts);
});

function showProducts(products){
    box.innerHTML=""; //deletes old ui
    products.forEach(function(product,index){ 

    //made new div+added class
        const card=document.createElement("div");
        card.className="card";

        const img=document.createElement("img"); //api se image lagayi
        img.src=product.thumbnail;

        const title=document.createElement("h3");
        title.textContent=product.title; //name of product added

        const price=document.createElement("p");
        price.className="price"; 
        price.textContent="$ "+product.price; //added price of product 

        const iconBox=document.createElement("div"); //div for all three icons stroing
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

        iconBox.append(cart,wishlist,view); //adding multiple children


        //tag-->
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

    //search-->
searchInput.onkeyup=function(){
    const text=searchInput.value.toLowerCase(); //case-insensitive search

    //fetch matching items from array--> 
    const filtered=allProducts.filter(function(p){
    return p.title.toLowerCase().includes(text);
    });
    showProducts(filtered);
};

    //sort -->
sortSelect.onchange=function(){
    let value=sortSelect.value;
    let sorted=[...allProducts]; //makes copy of the product array

    //high -> low:b-a
    if(value==="high"){
    sorted.sort(function(a,b){return b.price-a.price;}); //positive means b comes first : des=b.price-a.price is positive 
    }

    //low -> high:a-b
    if(value==="low"){
    sorted.sort(function(a,b){return a.price-b.price;}); //negative means a comes first : asc=a.price-b.price is negative
    }

showProducts(sorted);
};


//navbar items pe click event--> navbar logic : reset all -> set current
document.querySelectorAll("nav li").forEach(function(item){ //navbar ke har item pe 
    item.addEventListener("click",function(){
    document.querySelectorAll("nav li").forEach(function(li){ 
    li.classList.remove("active"); //removes active from every item in navbar
    });
    this.classList.add("active");  // add active to current item(jispe click event hua)
    });
});


//
