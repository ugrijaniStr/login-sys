getRole = () => {
    let role = document.getElementById('role');

    if(role.textContent == 'str') {
        role.innerHTML = `<b id = "owner"><b id = "userColor">${role.textContent}</b> <b>[</b>Owner<b>]</b></b> `
    } else {
        role.innerHTML = `<b id = "user"><b id = "userColor">${role.textContent}</b> <b>[</b>User<b>]</b></b> `
    }
}