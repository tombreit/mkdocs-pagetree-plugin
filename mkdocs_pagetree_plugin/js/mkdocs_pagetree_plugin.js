document.addEventListener("DOMContentLoaded", function (event) {
    console.log("Hi, I'm mkdocs-pagetree-plugin.");

    // Plugin CSS
    const style = document.createElement('style');
    style.appendChild(document.createTextNode(`
    .pagetree details {
        margin: 0;
        padding: 0;
    }
    `));

    const head = document.getElementsByTagName('head')[0];
    head.appendChild(style);

    // Plugin JS
    // Collapse/expand all pagetree <details> sections
    const pagetreeElements = document.querySelectorAll('.pagetree-container');
    const toggleBtn = `<button class="pagetree-toggle btn btn-primary btn-sm my-2" type="button">Expand/Collapse</button>`;

    for (const pagetreeElement of pagetreeElements) {
        pagetreeElement.insertAdjacentHTML("afterbegin", toggleBtn);
    }

    document.querySelectorAll('.pagetree-toggle').forEach(button => {
        let btnClickCount = 0;
        button.addEventListener('click', (e) => {
            btnClickCount++;
            let localPagetrees = e.currentTarget.closest('.pagetree-container').querySelectorAll('.pagetree details')

            localPagetrees.forEach(pagetreeDetail => {
                if (btnClickCount % 2 == 1) {
                    pagetreeDetail.setAttribute('open', 'open');
                } else {
                    pagetreeDetail.removeAttribute('open');
                }
            });
        });
    });
});
