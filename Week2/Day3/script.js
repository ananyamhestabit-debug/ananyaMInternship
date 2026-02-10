const items = document.querySelectorAll(".faq-item");
items.forEach(item=>{

  const head=item.querySelector(".faq-head");
  const icon=item.querySelector("span");
  head.addEventListener("click", ()=>{
    const isOpen = item.classList.contains("active");

    items.forEach(el => {
      el.classList.remove("active");
      el.querySelector("span").textContent="+";
    });

    if(!isOpen){
      item.classList.add("active");
      icon.textContent="-";
    }
  });
});
