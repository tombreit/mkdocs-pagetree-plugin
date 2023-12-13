// SPDX-FileCopyrightText: 2023 Thomas Breitner
//
// SPDX-License-Identifier: MIT

document.addEventListener("DOMContentLoaded", function (event) {
    console.log("Hi, I'm mkdocs-pagetree-plugin.");

    // Plugin CSS
    const style = document.createElement('style');
    style.appendChild(document.createTextNode(`
    /* Reset some default MkDocs styles */
    .pagetree details {
        margin: 0;
        padding: 0;
    }
    /* Reset some Material for MkDocs styles */
    .md-typeset .pagetree details {
        background-color: transparent;
        border: none;
        box-shadow: none;
        margin-top: 0;
        margin-bottom: 0;
    }
    .md-typeset .pagetree summary {
        padding-left: 3em;
        padding-top: 0;
        padding-bottom: 0;
        background-color: transparent;
    }
    .md-typeset .pagetree summary::after {
        display: none;
    }
    .md-typeset .pagetree summary::before {
        background-color: currentcolor;
        content: "";
        height: 1rem;
        -webkit-mask-image: var(--md-details-icon);
        mask-image: var(--md-details-icon);
        -webkit-mask-position: center;
        mask-position: center;
        -webkit-mask-repeat: no-repeat;
        mask-repeat: no-repeat;
        -webkit-mask-size: contain;
        mask-size: contain;
        position: absolute;
        top: .1em;
        left: 1.3em;
        transform: rotate(0deg);
        transition: transform .25s;
        width: 1rem;
      }
      .md-typeset .pagetree details[open] > summary::before {
        transform: rotate(90deg);
      }
      .md-typeset .pagetree-container ul li {
        margin-bottom: 0;
      }
    `));

    const head = document.getElementsByTagName('head')[0];
    head.appendChild(style);

    // Plugin JS
    // Collapse/expand all pagetree <details> sections
    const pagetreeElements = document.querySelectorAll('.pagetree-container');
    const toggleBtn = `<button class="pagetree-toggle md-button btn btn-primary btn-sm my-2" type="button">Expand/Collapse</button>`;

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
