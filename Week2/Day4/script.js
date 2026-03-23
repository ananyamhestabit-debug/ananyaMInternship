const input=document.getElementById("taskInput")
const addBtn=document.getElementById("addBtn")
const list=document.getElementById("taskList")
const msg=document.getElementById("msg")

//->try catch: safe load(jab jab refresh hoga browser)
let tasks=[]  //first we will take an empty array
try{
  tasks=JSON.parse(localStorage.getItem("tasks"))||[] //we load the data from local stroage to tasks array an di fnothing found then we get empty tasks array
}catch(e){
  console.error("Load error:",e)
  tasks=[]
}

 //>try catch: safe save(updates storage)
function save(){
  try{
    localStorage.setItem("tasks",JSON.stringify(tasks)) //saves task array in perma. storage
  }catch(e){
    console.error("Save error:",e)
  }
}

//this updates the ui:dom ko dubara bnata 
function render(){
  list.innerHTML=""

  tasks.forEach((task,i)=>{
    const li=document.createElement("li") //makes a new element <li> in memory not screen

    const check=document.createElement("input")// make s a new element <input>
    check.type="checkbox"
    check.checked=task.done //if task.done is true-->checkbox tick :user ke click se -> toh done:true ho jaega and checkbox false se true ho gya(tick ho jaega)

    const text=document.createElement("span") //text ke liye ek span element naya bnaya 
    text.textContent=task.text //span me text daal denge
    if(task.done) 
      text.style.textDecoration="line-through"

//when checkbox changes-->
    check.onchange=()=>{
      task.done=check.checked //if check.checked=true browser ne hi update krdiya khud if tick hoga checkbox and that true value will go to task.done(task.done=true ho jaega)
      save()
      render()
    }


    const edit=document.createElement("button")
    edit.textContent="Edit"
    edit.className="smallBtn"
    edit.onclick=()=>{
      try{
        const t=prompt("Edit task",task.text) //popup opens
        if(t){
          task.text=t
          save()
          render()
        }
      }catch(e){
        console.error("Edit error:",e)
      }
    }

    const del=document.createElement("button")
    del.textContent="Delete"
    del.className="smallBtn"
    del.onclick=()=>{
      tasks.splice(i,1)
      save()
      render()
    }

    li.append(check,text,edit,del) //added all elements to li
    list.appendChild(li) //li ko ul me dala
  })
}

//task add krna:runs on add button clicking
function addTask(){
  const text=input.value.trim() //trim()  to remove extra spaces from input

// for empty input:it shows error
  if(!text){
    msg.textContent="Please enter task first !"
    return
  }

//if input is valid : purana error clear krta hai
  msg.textContent="" 

//by default jo add hoga task woh false hoga
  tasks.push({text,done:false}) //array me new object added
  input.value="" //input clear
  save()
  render()
}

addBtn.onclick=addTask //click pe ye function run

render()

//-->accordian
document.querySelectorAll(".accHeader").forEach(h=>{
  h.onclick=()=>{
    const b=h.nextElementSibling
    b.style.display=b.style.display==="block"?"none":"block"
  }
})

document.querySelectorAll(".accBody p").forEach(p=>{
  p.onclick=()=>input.value=p.textContent //on clicking on p:p tag ka text chala jaeg a input me  
})