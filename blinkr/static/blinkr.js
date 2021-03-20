const pixel_radius = 20;
const margin = 5;

// current color
const cc = { r: 0, g: 0, b: 0}

const wrapper = d3.select('body').append('div').attr('class', 'wrapper');
const pi_wrapper = wrapper.append('div').attr('class', 'pi-wrapper');
const color_picker_wrapper = wrapper.append('div').attr('class', 'color-picker-wrapper');

function render_pis() {
    d3.json('/pis').then((pis) => {
        const pi_container = pi_wrapper.selectAll('.pi-container')
            .data(pis)
            .enter()
            .append('div')
                .attr('class', 'pi-container')
                .attr('id', (d) => d.name + '-container');

        const pi_name = pi_container.append('div')
            .attr('class', 'pi-name')
            .text((d) => d.name);

        const pixel_container = pi_container.append('div')
            .attr('class', 'pixel-container');

        const pixel = pixel_container.selectAll('.pixel-svg')
            .data((d, i) => {
                // right-to-left pixel addressing convention
                return d.pixels.reverse().map((rgb, i, arr) => {
                    return { name: d.name, pos: (arr.length-1)-i, r: rgb[0], g: rgb[1], b: rgb[2] };
                });
            })
            .enter()
            .append('svg')
                .attr('class', 'pixel-svg')
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

function render_color_picker() {
    const color_picker_container = color_picker_wrapper.append('div')
        .attr('class', 'color-picker-container');

    const color_picker_preview = color_picker_container.append('svg')
        .attr('width', (pixel_radius+margin)*2)
        .attr('height', (pixel_radius+margin)*2)
        .append('circle')
            .attr('class', 'color-picker-preview')
            .attr('cx', pixel_radius + margin)
            .attr('cy', pixel_radius + margin)
            .attr('r', pixel_radius)
            .style('fill', `rgb(${cc.r},${cc.g},${cc.b})`);

    color_picker_container.selectAll('.color-picker-input')
        .data(['r', 'g', 'b'])
        .enter()
        .append('label')
            .attr('for', (d) => `${d}-input`)
            .text((d) => d)
        .append('input')
            .attr('id', (d) => `${d}-input`)
            .attr('class', 'color-picker-input')
            .attr('type', 'text')
            .attr('value', (d) => cc[d])
            .attr('size', 3)
            .attr('maxlength', 3)
            .on('change', change_color_picker);
}

function click_pixel(event, d) {
    const circle = d3.select(this);
    // TODO color picker instead of all green
    d3.json(`/pis/${d.name}/pixels/${d.pos}/${cc.r}/${cc.g}/${cc.b}`, {method:"POST"})
        .then(rgb => {
            circle.style('fill', `rgb(${rgb[0]},${rgb[1]},${rgb[2]}`);
        });
}

function change_color_picker(event, d) {
    const val = +event.target.value;
    event.target.value = (isNaN(val) || val < 0) ? 0 : (val > 255) ? 255 : val;
    cc[d] = event.target.value;
    d3.selectAll('.color-picker-preview')
        .style('fill', `rgb(${cc.r},${cc.g},${cc.b})`)
}