import { loadElementsIn, showFolderContent } from "./lib/folderView.module.js";
import ContextMenu from "./lib/contextmenu.module.js";
import setupModal from "./lib/modal.module.js";
import makeApiCall from "./lib/api.module.js";
import showCurrentPath from "./lib/currentPath.module.js";
import checkFileSize from "./lib/security/fileSizeValidation.module.js";

const fileContextMenu = new ContextMenu();
const createFolderTriggerBtn = document.getElementById("create-folder-trigger-btn");
const fileUploadEl = document.getElementById("file");

async function loadAndRepresent(){
    const folderContent = await loadElementsIn(CURRENT_PATH);
    showFolderContent(folderContent, fileContextMenu);
}

loadAndRepresent();
showCurrentPath();

createFolderTriggerBtn.addEventListener("click", () => {
    setupModal({
        title: "Create folder",
        text: "Type the name of the new folder",
        inputs: [
            {
                type: "text",
                id: "new-folder-name",
                placeholder: "New folder"
            }
        ],
        onconfirm: async () => {
            const folderPath = `${CURRENT_PATH}/${document.getElementById('new-folder-name').value}`;
            const res = await makeApiCall({
                route: "storage/create/folder",
                body: {
                    user: USERNAME,
                    path: folderPath
                },
            });
            loadAndRepresent();
        }
    });
});

fileUploadEl.addEventListener("change", () => {
    checkFileSize(fileUploadEl);
});
