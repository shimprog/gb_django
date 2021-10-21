// window.onload = function () {
//     let basket_list = document.querySelector('.basket_list')
//     basket_list.addEventListener('change', (e) => {
//         fetch("/basket/edit/" + e.target.name + "/" + e.target.value + "/", {
//             method: 'GET',
//             headers: { 'X-Requested-With': 'XMLHttpRequest' },
//         }).then(response => response.json())
//             .then(data => {
//                 basket_list.innerHTML = data.result
//             })
//     })
// }

window.onload = function () {
    async function fetch_product(e) {
        const response = await fetch("/basket/edit/" + e.target.name + "/" + e.target.value + "/",
            {
                method: 'GET',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            }
        );
        return await response.json()
    }
    let basket_list = document.querySelector('.basket_list')
    basket_list.addEventListener('change', (e) => {
        fetch_product(e).then(
            data => basket_list.innerHTML = data.result
        )
    })
}
