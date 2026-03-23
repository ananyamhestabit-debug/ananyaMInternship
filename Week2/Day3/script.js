const accordItems = document.querySelectorAll(".faq-item");
accordItems.forEach(accordItem=>{

  const head=accordItem.querySelector(".faq-head");
  const sign=accordItem.querySelector("span");
  
  head.addEventListener("click", ()=>{
    const openAccor = accordItem.classList.contains("active");
    accordItems.forEach(element => {
      element.classList.remove("active");
      element.querySelector("span").textContent="+";
    });
    if(!openAccor){
      accordItem.classList.add("active");
      sign.textContent="-";
    }
  });
});
