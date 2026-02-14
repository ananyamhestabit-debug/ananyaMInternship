const input=document.getElementById("taskInput")
const addBtn=document.getElementById("addBtn")
const list=document.getElementById("taskList")
const msg=document.getElementById("msg")

let tasks=JSON.parse(localStorage.getItem("tasks"))||[]

function save(){
  localStorage.setItem("tasks",JSON.stringify(tasks))
}

function render(){
  list.innerHTML=""

  tasks.forEach((task,i)=>{
    const li=document.createElement("li")

    const check=document.createElement("input")
    check.type="checkbox"
    check.checked=task.done

    const text=document.createElement("span")
    text.textContent=task.text
    if(task.done) text.style.textDecoration="line-through"

    check.onchange=()=>{
      task.done=check.checked
      save()
      render()
    }

    const edit=document.createElement("button")
    edit.textContent="Edit"
    edit.className="smallBtn"
    edit.onclick=()=>{
      const t=prompt("Edit task",task.text)
      if(t){
        task.text=t
        save()
        render()
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

    li.append(check,text,edit,del)
    list.appendChild(li)
  })
}

function addTask(){
  const text=input.value.trim()

  if(!text){
    msg.textContent="Please enter task first !"
    return
  }

  msg.textContent=""

  tasks.push({text,done:false})
  input.value=""
  save()
  render()
}

addBtn.onclick=addTask

render()

document.querySelectorAll(".accHeader").forEach(h=>{
  h.onclick=()=>{
    const b=h.nextElementSibling
    b.style.display=b.style.display==="block"?"none":"block"
  }
})

document.querySelectorAll(".accBody p").forEach(p=>{
  p.onclick=()=>input.value=p.textContent
})
