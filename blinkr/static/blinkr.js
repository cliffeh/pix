function render_pis() {
    d3.json('/pis', (pis) => {
        pis.forEach((pi) => {
            console.log(pi);
        });
    });
}
