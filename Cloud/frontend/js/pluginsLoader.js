import makeApiCall from "./lib/api.module.js";

const pluginsListEl = document.getElementById("plugins-list");

function createListEl(data){
    const domEl = document.createElement("a");
    domEl.classList.add("dropdown-item");
    domEl.href = `/plugin/${data.name}/index`;
    domEl.innerHTML = `<i class="fa fa-${data.fa_icon}"></i> ${data.display_name}`;
    return domEl;
}

async function load(){
    const list = await makeApiCall({
        route: "info/plugins-list"
    });
    list.forEach(element => {
        pluginsListEl.appendChild(createListEl(element));
    });
}

load();
