const pixel_radius = 20;
const margin = 5;

function render_pis() {
    d3.json('/pis').then((pis) => {
        var wrapper = d3.select('body').append('div')
            .attr('class', 'wrapper');

        var pi_container = wrapper.selectAll('div')
            .data(pis)
            .enter()
            .append('div')
                .attr('class', 'pi-container')
                .attr('id', (d) => d.name + '-container');

        var pi_name = pi_container.append('div')
            .attr('class', 'pi-name')
            .text((d) => d.name);

        var pixel_container = pi_container.append('div')
            .attr('class', 'pixel-container');

        var pixel = pixel_container.selectAll('svg')
            .data((d, i) => {
                // right-to-left pixel addressing convention
                return d.pixels.reverse().map((rgb, i, arr) => {
                    return { name: d.name, pos: (arr.length-1)-i, r: rgb[0], g: rgb[1], b: rgb[2] };
                });
            })
            .enter()
            .append('svg')
                .attr('width', (pixel_radius+margin)*2)
                .attr('height', (pixel_radius+margin)*2)
            .append('circle')
                .attr('class', 'pixel')
                .attr('cx', pixel_radius + margin)
                .attr('cy', pixel_radius + margin)
                .attr('r', pixel_radius)
                .style('fill', (d) => `rgb(${d.r},${d.g},${d.b})`)
                .on('click', click_pixel);
    });
}

function click_pixel(event, d) {
    const circle = d3.select(this);
    // TODO color picker instead of all green
    d3.json(`/pis/${d.name}/pixels/${d.pos}/0/128/0`, {method:"POST"})
        .then(rgb => {
            console.log(rgb);
            circle.style('fill', `rgb(${rgb[0]},${rgb[1]},${rgb[2]}`);
        });
}
