document.addEventListener("DOMContentLoaded", async () => {
    const data = await fetch("http://localhost:8069/natacion/pagarcuota").then(r => r.json);
    console.log(data);

    for(let club of data) {

        document.querySelector("#clubs").innerHTML+= club.name
    }

    document.querySelector("#pagar").addEventListener
    ("click", async ()=> {
        const response = await fetch("http://localhost:8069/natacion/pagarcuota", {
            method: "POST",
            body: JSON.stringify({
                id: "1111"
            })
        }).then(r=> r.json());
        console.log(response);
    })
});